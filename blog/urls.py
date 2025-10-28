from django.urls import path

from blog.apps import BlogConfig
# from blog.views import ArticleListView, ArticleDetailView, ArticleCreateView

app_name = BlogConfig.name

urlpatterns = [
    # path("blog/", ArticleListView.as_view(), name="home"),
    # path("blog/<int:pk>/", ArticleDetailView.as_view(), name="article"),
    # path("blog/<int:pk>/edit", ArticleCreateView.as_view(), name='article_edit'),
]
