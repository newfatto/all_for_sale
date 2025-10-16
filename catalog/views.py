from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Contact, Product, Category


def home(request):
    latest_products = Product.objects.order_by("-created_at")[:5]

    for product in latest_products:
        print(f"{product.name} — {product.price} руб.")

    products = Product.objects.all()

    context = {"products": products}

    return render(request, "home.html", context)


def contacts(request):
    contact = Contact.objects.order_by("-updated_at").first()
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"Имя:{name} Телефон:{phone} Сообщение: {message}")
        return HttpResponse(f"Спасибо, {name}. Сообщение получено.")

    return render(request, "contacts.html", {"contact": contact})


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {"product": product}
    return render(request, "product.html", context=context)

def user_add_product(request):

    categories = Category.objects.all()
    context = {'categories': categories}

    if request.method == 'POST':
        name = request.POST.get("name")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        category_id = request.POST.get("category")
        price = request.POST.get("price")
        category = Category.objects.get(id=category_id)
        Product.objects.create(name=name, description=description, image=image, category=category, price=price)
        return HttpResponse(f"Спасибо. Товар {name} добавлен.")

    return render(request, 'user_add_product.html', context=context)

