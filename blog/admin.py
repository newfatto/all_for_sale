from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at", "is_published", "views")
    list_filter = ("is_published", "created_at", "updated_at", "views")
    search_fields = (
        "title",
        "content",
    )
