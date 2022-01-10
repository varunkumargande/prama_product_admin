from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    """Serializers for Case Study Instances"""

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related()
        return queryset

    def create(self, validated_data):
        instance = Product.objects.create(**validated_data)
        return instance

    class Meta:
        model = Product
        fields = '__all__'