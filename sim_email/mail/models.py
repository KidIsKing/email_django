from django.db import models


class Email(models.Model):
    """Модель для хранения писем"""
    
    # Выбор папок
    FOLDER_CHOICES = [
        ('inbox', 'Входящие'),
        ('sent', 'Отправленные'),
        ('read', 'Прочитанные'),
        ('unread', 'Непрочитанные'),
        ('archive', 'Архив'),
        ('trash', 'Корзина'),
    ]
    
    sender = models.CharField('Отправитель', max_length=100)
    recipient = models.CharField('Получатель', max_length=100)
    subject = models.CharField('Тема', max_length=200)
    body = models.TextField('Текст письма')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_read = models.BooleanField('Прочитано', default=False)
    folder = models.CharField('Папка', max_length=20, default='inbox', choices=FOLDER_CHOICES)

    def __str__(self):
        return f'{self.subject} - {self.sender}'