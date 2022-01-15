from django.urls import path, include
from task.views import ProductListView, ProductCreateView

app_name = "task"

urlpatterns = [

    path('create/', ProductCreateView.as_view(), name='create'),
    path('', ProductListView.as_view(), name='listing'),
]
