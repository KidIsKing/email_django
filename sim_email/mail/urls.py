from django.urls import path
from . import views

app_name = "mail"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("compose/", views.compose, name="compose"),
    path("email/<int:email_id>/", views.view_email, name="view_email"),
]
