from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
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
    emails = Email.objects.filter(
        recipient_user=request.user, folder="unread"
    ).order_by("-created_at")
    paginator = Paginator(emails, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "active_tab": "inbox",
        "page_title": "📬 Непрочитанные письма",
        "card_class": "card-unread",
        "show_archive_btn": True,
        "show_trash_btn": True,
        "empty_message": "Нет непрочитанных писем",
    }
    return render(request, "mail/email_list.html", context)


@login_required
def read_emails(request):
    emails = Email.objects.filter(recipient_user=request.user, folder="read").order_by(
        "-created_at"
    )
    paginator = Paginator(emails, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "active_tab": "read",
        "page_title": "✓ Прочитанные письма",
        "card_class": "",
        "show_archive_btn": True,
        "show_trash_btn": True,
        "empty_message": "Нет прочитанных писем",
    }
    return render(request, "mail/email_list.html", context)


@login_required
def sent_emails(request):
    emails = Email.objects.filter(sender_user=request.user, folder="sent").order_by(
        "-created_at"
    )
    paginator = Paginator(emails, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "active_tab": "sent",
        "page_title": "📤 Отправленные письма",
        "card_class": "",
        "show_archive_btn": True,
        "show_trash_btn": True,
        "empty_message": "Нет отправленных писем",
    }
    return render(request, "mail/email_list.html", context)


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


@login_required
def archive_emails(request):
    emails = (
        Email.objects.filter(folder="archive")
        .filter(
            models.Q(recipient_user=request.user) | models.Q(sender_user=request.user)
        )
        .order_by("-created_at")
    )
    paginator = Paginator(emails, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "active_tab": "archive",
        "page_title": "📦 Архив",
        "card_class": "card-archive",
        "show_restore_archive_btn": True,
        "show_trash_btn": True,
        "empty_message": "Архив пуст",
    }
    return render(request, "mail/email_list.html", context)


@login_required
def move_to_archive(request, email_id):
    """Переместить письмо в архив (для текущего пользователя)"""
    email = get_object_or_404(Email, id=email_id)
    if email.recipient_user == request.user or email.sender_user == request.user:
        if email.folder != "archive":
            email.folder = "archive"
            email.save()
            messages.success(request, "Письмо перемещено в архив")
        else:
            messages.info(request, "Письмо уже в архиве")
    else:
        messages.error(request, "Вы не можете архивировать это письмо")
    next_url = request.META.get("HTTP_REFERER", "mail:inbox")
    return redirect(next_url)


@login_required
def restore_from_archive(request, email_id):
    """Восстановить письмо из архива"""
    email = get_object_or_404(Email, id=email_id, folder="archive")
    if email.recipient_user == request.user or email.sender_user == request.user:
        if email.recipient_user == request.user:
            email.folder = "read"  # для получателя – в прочитанные
            email.is_read = True
        elif email.sender_user == request.user:
            email.folder = "sent"  # для отправителя – в отправленные
            email.is_read = True
        email.save()
        messages.success(request, "Письмо восстановлено из архива")
    else:
        messages.error(request, "Вы не можете восстановить это письмо")
    return redirect("mail:archive")


@login_required
def trash_emails(request):
    emails = (
        Email.objects.filter(folder="trash")
        .filter(
            models.Q(recipient_user=request.user) | models.Q(sender_user=request.user)
        )
        .order_by("-created_at")
    )
    paginator = Paginator(emails, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "active_tab": "trash",
        "page_title": "🗑️ Корзина",
        "card_class": "card-trash",
        "show_restore_trash_btn": True,
        "show_delete_forever_btn": True,
        "empty_message": "Корзина пуста",
    }
    return render(request, "mail/email_list.html", context)


@login_required
def move_to_trash(request, email_id):
    """Переместить письмо в корзину (для текущего пользователя)"""
    email = get_object_or_404(Email, id=email_id)
    # Проверяем, что пользователь владеет этим письмом
    if email.recipient_user == request.user or email.sender_user == request.user:
        if email.folder != "trash":
            email.folder = "trash"
            email.save()
            messages.success(request, "Письмо перемещено в корзину")
        else:
            messages.info(request, "Письмо уже в корзине")
    else:
        messages.error(request, "Вы не можете удалить это письмо")

    next_url = request.META.get("HTTP_REFERER", "mail:inbox")
    return redirect(next_url)


@login_required
def restore_from_trash(request, email_id):
    """Восстановить письмо из корзины"""
    email = get_object_or_404(Email, id=email_id, folder="trash")
    if email.recipient_user == request.user or email.sender_user == request.user:
        # Восстанавливаем в прочитанные (если письмо было для получателя)
        # или в отправленные (если письмо было отправителя)
        if email.recipient_user == request.user:
            email.folder = "read"
            email.is_read = True
        elif email.sender_user == request.user:
            email.folder = "sent"
            email.is_read = True
        email.save()
        messages.success(request, "Письмо восстановлено")
    else:
        messages.error(request, "Вы не можете восстановить это письмо")
    return redirect("mail:trash")


@login_required
def delete_forever(request, email_id):
    """Удалить письмо навсегда"""
    email = get_object_or_404(Email, id=email_id)
    if email.recipient_user == request.user or email.sender_user == request.user:
        email.delete()
        messages.success(request, "Письмо удалено навсегда")
    else:
        messages.error(request, "Вы не можете удалить это письмо")

    next_url = request.META.get("HTTP_REFERER", "mail:inbox")
    return redirect(next_url)
