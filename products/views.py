from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from .models import Product
from .serializers import ProductSerializer


class ProductViewset(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter, )
    pagination_class = LimitOffsetPagination
    filter_fields = ('id', 'name',)
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    # authentication_classes = (authentication.TokenAuthentication, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
