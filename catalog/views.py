from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
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

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Страница обновления информации о продукте пользователем"""

    model = Product
    form_class = ProductForm
    template_name = "product_edit.html"
    context_object_name = "product"

    def get_success_url(self):
        return reverse("catalog:product", args=[self.kwargs.get("pk")])

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
    context_object_name = "product"
