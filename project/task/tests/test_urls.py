from django.test import TestCase
from django.urls import reverse, resolve
from task.views import UserRegistrationAPIView, UserLoginAPIView, ProductListView, ProductCreateView


class ProductUrlsTestCase(TestCase):
    def test_listing_url_resolves(self):
        """
                  set Up : we are the url list all product url

                result : returning the correct view for the url
        """
        url = reverse('task:listing')
        self.assertEquals(resolve(url).func.view_class, ProductListView)

    def test_create_product_url_resolves(self):
        """
                set Up : we are the url create product url

                result : returning the correct view for the url
        """
        url = reverse('task:create')
        self.assertEquals(resolve(url).func.view_class, ProductCreateView)

    def test_user_login_url_resolves(self):
        """
                set Up : we are the url login url

                result : returning the correct view for the url
        """
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, UserLoginAPIView)

    def test_user_sign_up_url_resolves(self):
        """
                set Up : we are the url signup url

                result : returning the correct view for the url
        """
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, UserRegistrationAPIView)
