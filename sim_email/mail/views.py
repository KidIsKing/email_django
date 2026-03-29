from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Email
from .forms import EmailForm

User = get_user_model()


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def inbox(request):
    """Непрочитанные письма (письма, где пользователь - получатель)"""
    emails = Email.objects.filter(
        recipient_user=request.user, folder="unread"
    ).order_by("-created_at")
    paginator = Paginator(emails, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "mail/inbox.html", {"page_obj": page_obj, "active_tab": "inbox"}
    )


@login_required
def read_emails(request):
    """Прочитанные письма (письма, где пользователь - получатель)"""
    emails = Email.objects.filter(recipient_user=request.user, folder="read").order_by(
        "-created_at"
    )
    paginator = Paginator(emails, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "mail/read.html", {"page_obj": page_obj, "active_tab": "read"}
    )


@login_required
def sent_emails(request):
    """Отправленные письма (письма, где пользователь - отправитель)"""
    emails = Email.objects.filter(sender_user=request.user, folder="sent").order_by(
        "-created_at"
    )
    paginator = Paginator(emails, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "mail/sent.html", {"page_obj": page_obj, "active_tab": "sent"}
    )


@login_required
def compose(request):
    """Страница создания нового письма"""
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data["recipient"]
            recipient_user = User.objects.get(username=recipient_username)

            # Письмо для отправителя (в папку "Отправленные")
            sent_email = Email(
                sender=request.user.username,
                recipient=recipient_username,
                subject=form.cleaned_data["subject"],
                body=form.cleaned_data["body"],
                sender_user=request.user,
                recipient_user=recipient_user,
                folder="sent",
                is_read=True,
            )
            sent_email.save()

            # Письмо для получателя (в папку "Непрочитанные")
            received_email = Email(
                sender=request.user.username,
                recipient=recipient_username,
                subject=form.cleaned_data["subject"],
                body=form.cleaned_data["body"],
                sender_user=request.user,
                recipient_user=recipient_user,
                folder="unread",
                is_read=False,
            )
            received_email.save()

            messages.success(
                request, f"Письмо отправлено пользователю {recipient_username}!"
            )
            return redirect("mail:sent")
    else:
        form = EmailForm()

    return render(request, "mail/compose.html", {"form": form})


@login_required
def view_email(request, email_id):
    """Просмотр конкретного письма"""
    email = get_object_or_404(Email, id=email_id)

    # Если текущий пользователь - получатель и письмо ещё не прочитано
    if (
        email.recipient_user == request.user
        and email.folder == "unread"
        and not email.is_read
    ):
        email.folder = "read"
        email.is_read = True
        email.save()
        messages.success(request, "Письмо отмечено как прочитанное")

    return render(request, "mail/view_email.html", {"email": email})
