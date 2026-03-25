from django.shortcuts import render, redirect, get_object_or_404

# from django import get_object_or_404
from django.contrib import messages
from .models import Email
from .forms import EmailForm


def inbox(request):
    """Главная страница - список входящих писем"""
    emails = Email.objects.all()
    return render(request, "mail/inbox.html", {"emails": emails})


def compose(request):
    """Страница создания нового письма"""
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.folder = "sent"
            email.save()
            messages.success(request, "Письмо отправлено!")
            return redirect("mail:inbox")
    else:
        form = EmailForm()

    return render(request, "mail/compose.html", {"form": form})


def view_email(request, email_id):
    email = get_object_or_404(Email, id=email_id)
    if not email.is_read:
        email.is_read = True
        email.save()
    return render(request, "mail/view_email.html", {"email": email})
