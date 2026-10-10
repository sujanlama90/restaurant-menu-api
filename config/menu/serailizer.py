from rest_framework import serializers
from decimal import Decimal
from .models import Category,FoodItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ='__all__'
        read_only_fields =['id','created_at','updated_at']
    def validate_price(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Category name cannot be empty.")

        queryset = Category.objects.filter(name__iexact=value)

        # Exclude the current category during updates
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value
    
    def validate_slug(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Slug cannot be empty."
            )

        queryset = Category.objects.filter(slug__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A category with this slug already exists.")

        return value
    
    def validate_image(self, value):
        if value and hasattr(value, 'size'):
            max_size = 5 * 1024 * 1024  # 5 MB

            if value.size > max_size:
                raise serializers.ValidationError("Image size must not exceed 5 MB.")
        return value

    def validate_is_active(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("Active state must be true or false.")
        return value
        
class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields ='__all__'

    def validate_price(self, value):
            if value <= Decimal("0.00"):
                raise serializers.ValidationError("Price must be greater than zero.")
            return value

    def validate_food_type(self, value):
        allowed_types = ['VEGETARIAN', 'NON_VEGETARIAN']

        if value not in allowed_types:
            raise serializers.ValidationError(f"Food type must be one of {allowed_types}.")
        return value

    def validate_category(self, value):
        if not Category.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Selected category does not exist.")
        return value

    def validate_image(self, value):
        if value and hasattr(value, 'size'):
            max_size = 5 * 1024 * 1024  # 5 MB
            if value.size > max_size:
                raise serializers.ValidationError("Image size must not exceed 5 MB.")
        return value

    def validate_preparation_time(self, value):
        if value < 0:
            raise serializers.ValidationError("Preparation time cannot be negative.")
        return value