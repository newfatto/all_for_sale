from django.db import models


class Article(models.Model):
    """Класс для создания статьи блога"""

    title = models.CharField(max_length=100, verbose_name="Заголовок")  # заголовок
    content = models.TextField(null=True, verbose_name="Содержимое")  # содержимое
    preview = models.ImageField(upload_to="blog/", blank=True, null=True, verbose_name="Превью")  # превью(изображение)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # дата создания
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")  # признак публикации(булево поле)
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")  # количество просмотров

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]
