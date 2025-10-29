from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleDeleteView, ArticleUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path("", ArticleListView.as_view(), name="blog"),
    path("new/", ArticleCreateView.as_view(), name='new_article'),
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/edit/", ArticleUpdateView.as_view(), name='article_edit'),
    path("<int:pk>/confirm_delete/", ArticleDeleteView.as_view(), name='article_delete')
]
