from django.test import TestCase
from django.urls import reverse, resolve
from task.views import UserSignupAPIView, UserLoginAPIView, ProductListView, ProductCreateView


class ProductUrlsTestCase(TestCase):
    def test_listing_url_resolves(self):
        url = reverse('task:listing')
        self.assertEquals(resolve(url).func.view_class, ProductListView)

    def test_create_product_url_resolves(self):
        url = reverse('task:create')
        self.assertEquals(resolve(url).func.view_class, ProductCreateView)

    def test_user_login_url_resolves(self):
        url = reverse('task:login')
        self.assertEquals(resolve(url).func.view_class, UserLoginAPIView)

    def test_user_sign_up_url_resolves(self):
        url = reverse('task:signup')
        self.assertEquals(resolve(url).func.view_class, UserSignupAPIView)
