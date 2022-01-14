from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from task.models import Product
from task.serializers import UserSerializer, ProductSerializer, UserLoginSerializer


class UserSignupAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={'is_created': False})
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserLoginAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data, context={'is_created': True})
        if serializer.is_valid():
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ProductListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(Q(seller=request.user)).order_by('price')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
