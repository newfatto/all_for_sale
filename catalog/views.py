from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

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


class ProductDetailView(DetailView):
    model = Product
    template_name = "product.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Страница добавления нового продукта пользователем"""

    model = Product
    template_name = "user_add_product.html"
    fields = ["name", "description", "image", "price", "category"]
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст (как было в FBV)"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
