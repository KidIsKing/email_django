from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Email
from .forms import EmailForm


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def inbox(request):
    emails = Email.objects.filter(folder='unread').order_by('-created_at')
    return render(request, 'mail/inbox.html', {'emails': emails, 'active_tab': 'inbox'})


@login_required
def read_emails(request):
    emails = Email.objects.filter(folder='read').order_by('-created_at')
    return render(request, 'mail/read.html', {'emails': emails, 'active_tab': 'read'})


@login_required
def sent_emails(request):
    emails = Email.objects.filter(folder='sent').order_by('-created_at')
    return render(request, 'mail/sent.html', {'emails': emails, 'active_tab': 'sent'})


@login_required
def compose(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.folder = 'sent'
            email.is_read = True
            email.save()
            messages.success(request, 'Письмо отправлено!')
            return redirect('mail:sent')
    else:
        form = EmailForm()
    
    return render(request, 'mail/compose.html', {'form': form})


@login_required
def view_email(request, email_id):
    email = get_object_or_404(Email, id=email_id)
    
    if not email.is_read:
        email.is_read = True
        email.folder = 'read'
        email.save()
        messages.success(request, 'Письмо отмечено как прочитанное')
    
    return render(request, 'mail/view_email.html', {'email': email})