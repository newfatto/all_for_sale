from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleDeleteView, ArticleUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path("blog/", ArticleListView.as_view(), name="blog"),
    path("blog/new/", ArticleCreateView.as_view(), name='new_article'),
    path("blog/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("blog/<int:pk>/edit/", ArticleUpdateView.as_view(), name='article_edit'),
    path("blog/<int:pk>/confirm_delete", ArticleDeleteView.as_view(), name='article_delete')
]
