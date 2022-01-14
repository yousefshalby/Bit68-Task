from django.test import TestCase
from task.models import Product


class TestProduct(TestCase):
    def test_it_stringify_product_name(self):
        product = Product.objects.create(name='book')
        new_product = Product.objects.get(pk=1)
        self.assertEqual(str(new_product), product.name)
