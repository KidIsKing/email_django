from django.db import models


class Email(models.Model):
    """Модель для хранения писем"""
    sender = models.CharField('Отправитель', max_length=100)
    recipient = models.CharField('Получатель', max_length=100)
    subject = models.CharField('Тема', max_length=200)
    body = models.TextField('Текст письма')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)  # установка времени создания письма
    is_read = models.BooleanField('Прочитано', default=False)
    folder = models.CharField(
        'Папка',
        max_length=20,
        default='inbox'
    )

    def __str__(self):
        return f'{self.subject} - {self.sender}'