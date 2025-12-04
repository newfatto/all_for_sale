from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")

    phone = models.CharField(
        max_length=15, null=True, blank=True, verbose_name="Телефон", help_text="Введите номер телефона"
    )
    country = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Страна", help_text="Укажите страну проживания"
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите свой аватар"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
