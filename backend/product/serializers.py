from rest_framework import serializers

from .models import Category, Product


class ProducSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "get_absolute_url",
            "get_image",
            "get_thumbnail",
        )
