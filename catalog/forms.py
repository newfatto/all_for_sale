from django import forms
from .models import Product
from .constants import BANNED_WORDS
from django.core.exceptions import ValidationError


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(bad_word in name.lower() for bad_word in BANNED_WORDS):
            raise ValidationError(f"Вы использовали запрещённое слово. Не делайте так больше.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if any(bad_word in description.lower() for bad_word in BANNED_WORDS):
            raise ValidationError(f"Вы использовали запрещённое слово. Не делайте так больше.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price


