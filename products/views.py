from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Product
from .serializers import ProductSerializer


class ProductViewset(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter, )
    filter_fields = ('id', 'name',)
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        """ Allow partial updates without mandatory fields """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
