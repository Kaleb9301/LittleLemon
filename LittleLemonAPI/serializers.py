from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal
from rest_framework.validators import UniqueTogetherValidator

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only=True)  # Read-only nested serializer
    category_id = serializers.IntegerField(write_only=True)  # Write-only for input

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        extra_kwargs = {
            'price': {'min_value': 2},
            'stock': {'source': 'inventory', 'min_value': 0},
        }

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')  # Get category_id from input
        category = Category.objects.get(id=category_id)  # Fetch the related Category
        menu_item = MenuItem.objects.create(category=category, **validated_data)
        return menu_item

    def calculate_tax(self, product: MenuItem):
        tax_rate = Decimal('1.1')
        return product.price * tax_rate
