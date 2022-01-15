from django.contrib import admin
from django.urls import path, include
from task.views import UserSignupAPIView, UserLoginAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', UserSignupAPIView.as_view(), name='signup'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('task/', include('task.urls', namespace='task')),

]
