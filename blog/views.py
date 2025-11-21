from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from blog.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "blog.html"
    context_object_name = "articles"


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    template_name = "article_edit.html"
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:blog")
    permission_required = "blog.add_article"


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=["views"])
        return obj


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "content", "preview", "is_published"]
    template_name = "article_edit.html"
    permission_required = "blog.change_article"

    def get_success_url(self):
        return reverse("blog:article_detail", args=[self.kwargs.get("pk")])


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = "article_confirm_delete.html"
    success_url = reverse_lazy("blog:blog")
    permission_required = "blog.delete_article"
