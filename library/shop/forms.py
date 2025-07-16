from django import forms
from shop.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "email", "address", "city", "postal_code"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ФИО"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Электронная почта"}
            ),
            "address": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Адрес"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Город"}
            ),
            "postal_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Почтовый индекс"}
            ),
        }
