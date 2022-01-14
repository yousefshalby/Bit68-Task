from django.contrib.auth import get_user_model
from django.test import TestCase
from task.factories import UserFactory, ProductFactory
from task.models import Product
from task.serializers import UserSerializer, ProductSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.user = UserFactory()
        self.serializer = UserSerializer(instance=self.user)
        self.data = {
            'username': "test",
            "email": "test@test.com",
            "password": "secret",
            "confirm_password": "secret"
        }

    def test_it_contains_all_expected_fields(self):
        data = self.serializer.data
        self.assertEquals(set(data.keys()), {'username', 'email'})

    def test_username_field_equals_user_in_user_object(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user.username)

    def test_email_field_equals_email_in_user_object(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user.email)

    def test_email_is_required(self):
        self.data.pop('email')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), {'email'})

    def test_it_return_validation_error_when_email_does_not_correct(self):
        self.data['email'] = 'bad email'
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), {'email'})

    def test_username_is_required(self):
        self.data.pop('username')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'username'})

    def test_it_returns_validation_error_when_password_does_not_provided(self):
        self.data.pop('password')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'password'})

    def test_confirm_password_is_required(self):
        self.data.pop('confirm_password')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'confirm_password'})

    def test_it_returns_validation_error_when_confirm_password_does_not_match_password(self):
        self.data['confirm_password'] = 'unmatching'
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'confirm_password'})

    def test_it_remove_confirm_password_from_validated_data_when_create(self):
        serializer = UserSerializer(data=self.data, context={'is_created': True})
        serializer.is_valid()
        instance = serializer.save()
        self.assertIsInstance(instance, self.UserModel)

    def test_it_returns_validation_errors_when_password_and_confirm_password_does_not_exist_on_create(self):
        self.data.pop('password')
        self.data.pop('confirm_password')
        serializer = UserSerializer(data=self.data, context={'is_created': False})
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'password', 'confirm_password'})

    def test_it_remove_confirm_password_from_validated_data_when_update(self):
        user = UserFactory()
        serializer = UserSerializer(data=self.data, instance=user, context={'is_created': True})
        serializer.is_valid()
        instance = serializer.save()
        self.assertEquals(serializer.data['username'], instance.username)

    def test_it_returns_validation_errors_when_password_and_confirm_password_does_not_exist_on_update(self):
        self.data.pop('password')
        self.data.pop('confirm_password')
        user = UserFactory()
        serializer = UserSerializer(data=self.data, instance=user, context={'is_created': True})
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.username, self.data['username'])

    def test_it_raise_error_when_context_does_not_has_is_created(self):
        serializer = UserSerializer(data=self.data, instance=self.user)
        serializer.is_valid()
        with self.assertRaises(ValueError, msg='is_created does not exist'):
            serializer.save()


class ProductSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory()
        self.serializer = ProductSerializer(instance=self.product)
        self.data = {
            'name': 'car',
            'price': 10.00,
            'seller': self.user.pk,
        }

    def test_if_returns_expected_field(self):
        data = self.serializer.data
        self.assertEquals(set(data.keys()), {'name', 'price', 'seller'})

    def test_product_not_accept_payload_without_is_favorite(self):
        self.data.pop('name')
        serializer = ProductSerializer(instance=self.product, data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_product_not_accept_payload_without_product(self):
        self.data.pop('price')
        serializer = ProductSerializer(instance=self.product, data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_it_returns_error_when_no_data(self):
        serializer = ProductSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)

    def test_author_foreignkey_is_null(self):
        data = ProductSerializer(instance=Product.objects.create()).data
        self.assertEquals(None, data['seller'])

    def test_it_creates_product(self):
        serializer = ProductSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_it_updates_product(self):
        serializer = ProductSerializer(instance=self.product, data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEquals(ProductSerializer(instance=self.product).data, serializer.data)

