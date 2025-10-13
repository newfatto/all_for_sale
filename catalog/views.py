from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Contact, Product


def home(request):
    latest_products = Product.objects.order_by("-created_at")[:5]

    for product in latest_products:
        print(f"{product.name} — {product.price} руб.")

    return render(request, "home.html")


def contacts(request):
    contact = Contact.objects.order_by("-updated_at").first()
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"Имя:{name} Телефон:{phone} Сообщение: {message}")
        return HttpResponse(f"Спасибо, {name}. Сообщение получено.")

    return render(request, "contacts.html", {"contact": contact})
