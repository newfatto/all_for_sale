import os

from django import forms
from django.core.exceptions import ValidationError

from .constants import BANNED_WORDS
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Форма создания/редактирования продукта.

    Поле is_published отображается только для пользователей,
    у которых есть право catalog.can_unpublish_product.
    """

    MAX_IMAGE_SIZE = 5 * 1024 * 1024

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы. Поле is_published доступно только обладателю права 'can_unpublish_product'
        """
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Название продукта"})

        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Описание продукта",
                "rows": 4,
            }
        )

        self.fields["image"].widget.attrs.update(
            {
                "class": "form-control-file",
                "accept": "image/png, image/jpeg, image/pjpeg, image/x-png",
                "title": "Допустимые форматы: JPEG, PNG. Размер не более 5 МБ.",
            }
        )

        self.fields["category"].widget.attrs.update(
            {
                "class": "form-select",
            }
        )

        self.fields["price"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите цену",
                "min": "0",
                "step": "0.01",
                "type": "number",
            }
        )

        if not (self.user and self.user.has_perm("catalog.can_unpublish_product")):
            self.fields.pop("is_published", None)

        self.fields["is_published"].label = "Продукт опубликован"

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price", "is_published"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if any(bad_word in name.lower() for bad_word in BANNED_WORDS):
            raise ValidationError("Вы использовали запрещённое слово. Не делайте так больше.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if any(bad_word in description.lower() for bad_word in BANNED_WORDS):
            raise ValidationError("Вы использовали запрещённое слово. Не делайте так больше.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image

        if image.size > self.MAX_IMAGE_SIZE:
            raise ValidationError("Размер изображения не должен превышать 5 мб.")

        valid_types = ["image/jpeg", "image/pjpeg", "image/png", "image/x-png"]
        content_type = getattr(image, "content_type", "").lower()
        if content_type not in valid_types:
            raise ValidationError("Допустимые форматы изображений: JPEG или PNG.")

        ext = os.path.splitext(image.name)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png"]:
            raise ValidationError("Допустимые расширения файлов: .jpg, .jpeg, .png.")

        return image
