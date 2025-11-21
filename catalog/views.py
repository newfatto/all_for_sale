from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, UpdateView
from django.views.generic.edit import CreateView

from catalog.forms import ProductForm
from catalog.models import Category, Contact, Product


class ProductListView(ListView):
    """Главная страница: формируем список продуктов с пагинатором"""

    model = Product
    template_name = "home.html"
    context_object_name = "products"
    paginate_by = 4
    ordering = ["id"]

    def get_queryset(self):
        """Фильтруем продукты по статусу публикации.

        Обычный пользователь видит только опубликованные,
        модератор (с правом can_unpublish_product) и суперпользователь — все.
        """
        qs = super().get_queryset().order_by("id")
        user = self.request.user

        if user.is_authenticated and (user.is_superuser or user.has_perm("catalog.can_unpublish_product")):
            return qs

        return qs.filter(is_published=True)


class ContactsTemplateView(TemplateView):
    """Страница контактов: отображение и обработка формы"""

    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact = Contact.objects.order_by("-updated_at").first()
        context["contact"] = contact
        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Обрабатываем POST-запрос с формы контактов"""
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print(f"Имя: {name}, Телефон: {phone}, Сообщение: {message}")

        return HttpResponse(f"Спасибо, {name}. Сообщение получено.")


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Страница добавления нового продукта пользователем"""

    model = Product
    form_class = ProductForm
    template_name = "product_create.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # ← важно
        return kwargs


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Страница обновления информации о продукте пользователем"""

    model = Product
    template_name = "product_edit.html"
    context_object_name = "product"

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.has_perm("update_product"):
            return ProductForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse("catalog:product", args=[self.kwargs.get("pk")])

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # ← важно
        return kwargs


class UnpublishProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.is_published = False
        product.save()
        return redirect("catalog:product", pk=product.id)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
    context_object_name = "product"

    def dispatch(self, request, *args, **kwargs):
        """
        Удалять продукт могут:
        - владелец продукта
        - модератор (имеющий право catalog.delete_product)
        """
        product = self.get_object()
        user = request.user

        if product.owner == user or user.has_perm("catalog.delete_product"):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("У вас нет прав на удаление этого продукта.")
