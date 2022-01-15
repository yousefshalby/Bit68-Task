from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from task.factories import UserFactory, ProductFactory
from task.models import Product
from task.serializers import UserSerializer, ProductSerializer


class UserSignupAPITestCase(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.data = {
            'username': "test",
            "email": "test@test.com",
            "password": "secret",
            "confirm_password": "secret",
        }
        self.client = APIClient()
        self.url = reverse('signup')

    def test_it_create_user_successfully(self):
        self.client.post(self.url, self.data)
        user = self.UserModel.objects.filter(username=self.data['username'], email=self.data['email'])
        self.assertTrue(user.exists())

    def test_it_returns_422_when_data_is_invalid(self):
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, 422)

    def test_it_returns_201_when_user_created_successfully(self):
        response = self.client.post(self.url, self.data)
        self.assertEquals(response.status_code, 201)

    def test_it_returns_user_data_after_created(self):
        response = self.client.post(self.url, self.data)
        self.assertIn('user', response.data)


class ProductListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.product = ProductFactory()
        self.client.login(username=self.user.email, password='secret')
        self.url = reverse('task:listing')

    def test_it_returns_401_when_user_is_not_authenticated(self):
        client = APIClient()
        response = client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_it_returns_all_products_by_user(self):
        response = self.client.get(self.url)
        words = Product.objects.filter(seller=self.user)
        serializer = ProductSerializer(instance=words, many=True)
        self.assertEquals(list(response.data), list(serializer.data))

    def test_it_returns_200_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class ProductCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.product = ProductFactory()
        self.client.login(username=self.user.email, password='secret')
        self.url = reverse('task:create')
        self.data = {
            'name': 'car',
            'price': 10,
        }

    def test_it_returns_401_when_user_is_not_authenticated(self):
        client = APIClient()
        response = client.post(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_it_returns_422_when_insert_invalid_data(self):
        response = self.client.post(self.url, data={})
        self.assertEquals(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_it_adds_user_to_created_by(self):
        response = self.client.post(self.url, self.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.product = ProductFactory()
        self.client.login(username=self.user.email, password='secret')
        self.url = reverse('login')
        self.data = {
            "email": "test@test.com",
            "password": "secret",
            "confirm_password": "secret",
        }

    def test_it_returns_200_status_code_when_updated_successfully(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(data=self.data)
        serializer.is_valid()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
