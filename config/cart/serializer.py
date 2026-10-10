
from rest_framework import serializers
from decimal import Decimal

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(
        source="food_item.name",
        read_only=True
    )

    price = serializers.DecimalField(
        source="food_item.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "food_item",
            "food_name",
            "price",
            "quantity",
            "line_total",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "food_name",
            "price",
            "line_total",
            "created_at",
            "updated_at",
        ]

    def get_line_total(self, obj):
        return obj.food_item.price * obj.quantity

    def validate_quantity(self, value):
        if not 1 <= value <= 99:
            raise serializers.ValidationError(
                "Quantity must be between 1 and 99."
            )
        return value

    def validate_food_item(self, food_item):
        if not food_item.is_available:
            raise serializers.ValidationError(
                "This food item is currently unavailable."
            )

        if not food_item.category.is_active:
            raise serializers.ValidationError(
                "This food item's category is inactive."
            )

        return food_item


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    total_items = serializers.SerializerMethodField()
    cart_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_items",
            "cart_total",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_cart_total(self, obj):
        total = sum(
            (
                item.food_item.price * item.quantity
                for item in obj.items.all()
            ),
            Decimal("0.00")
        )
        return total.quantize(Decimal("0.01"))
