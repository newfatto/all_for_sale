from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product, user_add_product

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("product/<int:product_id>/", product, name="product"),
    path("user_add_product/", user_add_product, name='user_add_product')
]
