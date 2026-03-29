from django import forms
from django.contrib.auth import get_user_model
from .models import Email

User = get_user_model()


class EmailForm(forms.ModelForm):
    """Форма для создания нового письма"""

    recipient = forms.CharField(
        label="Кому", max_length=100, help_text="Введите имя пользователя получателя"
    )

    class Meta:
        model = Email
        fields = ("recipient", "subject", "body")
        widgets = {
            "body": forms.Textarea(attrs={"rows": 6}),
        }
        labels = {
            "recipient": "Кому",
            "subject": "Тема",
            "body": "Текст письма",
        }

    def clean_recipient(self):
        recipient_username = self.cleaned_data.get("recipient")

        if not recipient_username:
            raise forms.ValidationError("Укажите получателя")

        try:
            recipient_user = User.objects.get(username=recipient_username)
            return recipient_username
        except User.DoesNotExist:
            raise forms.ValidationError(
                f'Пользователь "{recipient_username}" не найден'
            )
