from django.conf import settings
from django.core.cache import cache

from .models import Product


def get_products_from_cache():
    """
    Возвращает список продуктов из кэша, если кэш включён.
    Если записи нет — сохраняет queryset в кэш.
    """
    if not getattr( settings, 'CACHE_ENABLED', False):
        return list(Product.objects.all().order_by("id"))

    key: str = 'product_list'
    products: list[Product] | None = cache.get(key)

    if products is None:
        products = list(Product.objects.all().order_by('id'))
        cache.set(key, products)

    return products
