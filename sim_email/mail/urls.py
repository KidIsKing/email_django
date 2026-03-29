from django.urls import path
from . import views

app_name = "mail"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("read/", views.read_emails, name="read"),
    path("sent/", views.sent_emails, name="sent"),
    path("trash/", views.trash_emails, name="trash"),  # корзина
    path("compose/", views.compose, name="compose"),
    path("email/<int:email_id>/", views.view_email, name="view_email"),
    path(
        "email/<int:email_id>/trash/", views.move_to_trash, name="move_to_trash"
    ),  # в корзину
    path(
        "email/<int:email_id>/restore/", views.restore_from_trash, name="restore"
    ),  # восстановить
    path(
        "email/<int:email_id>/delete/", views.delete_forever, name="delete_forever"
    ),  # удалить навсегда
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("archive/", views.archive_emails, name="archive"),  # страница архива
    path(
        "email/<int:email_id>/archive/", views.move_to_archive, name="move_to_archive"
    ),  # в архив
    path(
        "email/<int:email_id>/unarchive/",
        views.restore_from_archive,
        name="restore_from_archive",
    ),  # из архива
]
