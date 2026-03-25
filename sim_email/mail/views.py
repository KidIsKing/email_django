from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Email
from .forms import EmailForm


def inbox(request):
    """Непрочитанные письма"""
    emails = Email.objects.filter(folder='unread').order_by('-created_at')
    return render(request, 'mail/inbox.html', {'emails': emails, 'active_tab': 'inbox'})


def read_emails(request):
    """Прочитанные письма"""
    emails = Email.objects.filter(folder='read').order_by('-created_at')
    return render(request, 'mail/read.html', {'emails': emails, 'active_tab': 'read'})


def sent_emails(request):
    """Отправленные письма"""
    emails = Email.objects.filter(folder='sent').order_by('-created_at')
    return render(request, 'mail/sent.html', {'emails': emails, 'active_tab': 'sent'})


def compose(request):
    """Страница создания нового письма"""
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.folder = 'sent'
            email.is_read = True  # Отправленные считаем прочитанными
            email.save()
            messages.success(request, 'Письмо отправлено!')
            return redirect('mail:sent')
    else:
        form = EmailForm()
    
    return render(request, 'mail/compose.html', {'form': form})


def view_email(request, email_id):
    """Просмотр конкретного письма"""
    email = get_object_or_404(Email, id=email_id)
    
    # Если письмо не прочитано, перемещаем в прочитанные
    if not email.is_read:
        email.is_read = True
        email.folder = 'read'
        email.save()
        messages.success(request, 'Письмо отмечено как прочитанное')
    
    return render(request, 'mail/view_email.html', {'email': email})