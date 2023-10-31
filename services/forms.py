from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Email


class ContactForm(forms.Form):
    name = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={"placeholder": "Jméno", "class": "mail_text"}),
    )

    number = PhoneNumberField(
        region="CZ",
        widget=forms.TextInput(
            attrs={"placeholder": "Mobilní číslo", "class": "mail_text"}
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "mail_text"})
    )

    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Zpráva (není povinná)", "class": "mail_text"}
        ),
    )


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "Enter_text",
                    "placeholder": "Email",
                    "label": "",
                }
            )
        }
        labels = {"email": ""}
