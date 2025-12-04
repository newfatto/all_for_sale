from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import CustomUser


class StyleFormMixin:
    """
    Миксин автоматически добавляет Bootstrap-класс 'form-control'
    ко всем полям формы.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = "Ваш email"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Подтверждение пароля"

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите email"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password1",
            "password2",
        )


class CustomUserAuthenticationForm(AuthenticationForm):
    """
    Форма входа по email вместо username.
    """

    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Ваш email"
        self.fields["password"].label = "Пароль"
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Введите email"})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})

    class Meta:
        model = CustomUser
        fields = ("username", "password")


class UserUpdateForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = "Ваш email"
        self.fields["first_name"].label = "Имя"
        self.fields["last_name"].label = "Фамилия"
        self.fields["phone"].label = "Номер телефона"
        self.fields["country"].label = "Страна проживания"
        self.fields["avatar"].label = "Аватар"

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone",
            "country",
            "avatar",
        )
