from django.urls import reverse_lazy

from blog.models import Article
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class ArticleListView(ListView):
    model = Article
    template_name = 'blog.html'
    context_object_name = 'articles'


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_edit.html'
    fields = ['title', 'content', 'preview', ]
    success_url = reverse_lazy('blog:blog')


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'content', 'preview', ]
    template_name = 'article_edit.html'
    success_url = reverse_lazy('blog:blog')


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('blog:blog')
