from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("product/<int:product_id>/", product, name="product"),
]
