from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """Перезагрузка тестовых категорий и продуктов из фикстур."""

    help = "Add test products to the database from fixture"

    def handle(self, *args, **kwargs):

        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command("loaddata", "category_fixture.json")
        call_command("loaddata", "product_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
