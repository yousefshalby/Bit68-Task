import factory
import random
from task.models import Product, User


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('name')
    price = factory.LazyAttribute(lambda x: random.randrange(0, 10000))


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.lazy_attribute(
        lambda obj: '{}.{}.{}'.format(obj.first_name, obj.last_name, random.randrange(1, 1000)))
    email = factory.lazy_attribute(lambda obj: '{}@advance.com'.format(obj.username))
    password = factory.PostGenerationMethodCall('set_password', 'secret')
    is_superuser = True
