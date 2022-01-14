from django.urls import path, include
from task.views import UserSignupAPIView, UserLoginAPIView, ProductListView, ProductCreateView

app_name = "task"

urlpatterns = [
    path('sign_up/', UserSignupAPIView.as_view(), name='signup'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('', ProductListView.as_view(), name='listing'),
]
