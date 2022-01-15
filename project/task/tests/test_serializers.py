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
        """
             result : returning the correct fields for the serializer
        """
        data = self.serializer.data
        self.assertEquals(set(data.keys()), {'username', 'email'})

    def test_email_is_required(self):
        """
              set Up :
                - we are removing the email value and check if serializer will be valid

              result : returning serializer not valid
        """
        self.data.pop('email')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), {'email'})

    def test_it_return_validation_error_when_email_does_not_correct(self):
        """
              set Up :
                - we are updating email value with invalid data and check if serializer will be valid

              result : returning serializer not valid
        """
        self.data['email'] = 'bad email'
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), {'email'})

    def test_username_is_required(self):
        """
              set Up :
                - we are removing the username value and check if serializer will be valid

              result : returning serializer not valid
        """
        self.data.pop('username')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'username'})

    def test_it_returns_validation_error_when_password_does_not_provided(self):
        """
              set Up :
                - we are removing the password value and check if serializer will be valid

              result : returning serializer not valid
        """
        self.data.pop('password')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'password'})

    def test_confirm_password_is_required(self):
        """
              set Up :
                - we are removing the confirm_password value and check if serializer will be valid

              result : returning serializer not valid
        """
        self.data.pop('confirm_password')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'confirm_password'})

    def test_it_returns_validation_error_when_confirm_password_does_not_match_password(self):
        """
              set Up :
                - we are updating confirm_password value with no match password data and check if serializer will be valid

              result : returning serializer not valid
        """
        self.data['confirm_password'] = 'no matching'
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'confirm_password'})

    def test_it_returns_validation_errors_when_password_and_confirm_password_does_not_exist_on_create(self):
        """
              set Up :
                - we are removing the password and confirm_password value and check if serializer will be valid

              result : returning serializer not valid
        """
        self.data.pop('password')
        self.data.pop('confirm_password')
        serializer = UserSerializer(data=self.data, context={'is_created': False})
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'password', 'confirm_password'})

    def test_it_remove_confirm_password_from_validated_data_when_update(self):
        """
              set Up :
                - we are removing the is created context and check if serializer will be valid

              result : returning serializer not valid
        """
        user = UserFactory()
        serializer = UserSerializer(data=self.data, instance=user, context={'is_created': True})
        serializer.is_valid()
        instance = serializer.save()
        self.assertEquals(serializer.data['username'], instance.username)

    def test_it_raise_error_when_context_does_not_has_is_created(self):
        """
              set Up :
                - we are removing the is created context and check if serializer will be valid

              result : returning serializer not valid
        """
        serializer = UserSerializer(data=self.data, instance=self.user)
        serializer.is_valid()
        with self.assertRaises(ValueError, msg='is_created does not exist'):
            serializer.save()

    def test_username_field_equals_user_in_user_object(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user.username)

    def test_email_field_equals_email_in_user_object(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user.email)

    def test_it_remove_confirm_password_from_validated_data_when_create(self):
        serializer = UserSerializer(data=self.data, context={'is_created': True})
        serializer.is_valid()
        instance = serializer.save()
        self.assertIsInstance(instance, self.UserModel)


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
        """
              result : returning the correct fields for the serializer
        """
        data = self.serializer.data
        self.assertEquals(set(data.keys()), {'name', 'price', 'seller'})

    def test_product_not_accept_payload_without_name(self):
        """
              set Up :
                - we are removing the name value and check if serializer will be valid

              result : returning serializer not valid
        """
        self.data.pop('name')
        serializer = ProductSerializer(instance=self.product, data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_product_not_accept_payload_without_price(self):
        """
              set Up :
                - we are removing the price value and check if serializer will be valid

              result : returning serializer is valid
        """
        self.data.pop('price')
        serializer = ProductSerializer(instance=self.product, data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_it_returns_error_when_no_data(self):
        """
              set Up :
                  - we are removing all serializer

              result : returning serializer not valid and number of errors
        """
        serializer = ProductSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)

    def test_author_foreignkey_is_null(self):
        """
              set Up :
                - we are removing all serializer data

              result : seller return None
        """
        data = ProductSerializer(instance=Product.objects.create()).data
        self.assertEquals(None, data['seller'])

    def test_it_creates_product(self):
        """
              set Up :
                - we are giving the right date to the serializer

              result : serializer obj is created successfully
        """
        serializer = ProductSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_it_updates_product(self):
        """
              set Up :
                - we are creating obj from serializer
                - we are giving the right date to the serializer

              result : serializer obj data will be updated successfully
        """
        serializer = ProductSerializer(instance=self.product, data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEquals(ProductSerializer(instance=self.product).data, serializer.data)

