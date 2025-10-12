from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Название категории')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f'Категория:{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Название продукта')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images/', blank=True, default=None, null=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'Продукт:{self.name} Цена:{self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name', 'price', 'created_at']
