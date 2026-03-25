from django import forms
from .models import Email


class EmailForm(forms.ModelForm):
    """Форма для создания нового письма"""

    class Meta:
        model = Email
        fields = ("sender", "recipient", "subject", "body")
        widgets = {
            "body": forms.Textarea(attrs={"rows": 6}),
        }
