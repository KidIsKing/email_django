from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('read/', views.read_emails, name='read'),
    path('sent/', views.sent_emails, name='sent'),
    path('compose/', views.compose, name='compose'),
    path('email/<int:email_id>/', views.view_email, name='view_email'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]