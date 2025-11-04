from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactsTemplateView, ProductCreateView, ProductDetailView, ProductListView, \
    ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product"),
    path("product/new/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/edit", ProductUpdateView.as_view(), name="product_edit"),
    path("product/<int:pk>/confirm_delete", ProductDeleteView.as_view(), name="product_confirm_delete"),
]
