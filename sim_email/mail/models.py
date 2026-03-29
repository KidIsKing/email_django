from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Email(models.Model):
    """Модель для хранения писем"""

    FOLDER_CHOICES = [
        ("inbox", "Входящие"),
        ("sent", "Отправленные"),
        ("read", "Прочитанные"),
        ("unread", "Непрочитанные"),
        ("archive", "Архив"),
        ("trash", "Корзина"),
    ]

    sender = models.CharField("Отправитель (текст)", max_length=100)
    recipient = models.CharField("Получатель (текст)", max_length=100)
    subject = models.CharField("Тема", max_length=200)
    body = models.TextField("Текст письма")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_read = models.BooleanField("Прочитано", default=False)
    folder = models.CharField(
        "Папка", max_length=20, default="inbox", choices=FOLDER_CHOICES
    )

    sender_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_emails",
        verbose_name="Отправитель (пользователь)",
        null=True,
        blank=True,
    )

    recipient_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_emails",
        verbose_name="Получатель (пользователь)",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.subject} - {self.sender} -> {self.recipient}"
