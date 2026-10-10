
from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.username",read_only=True,)
    food_name = serializers.CharField(
        source="food_item.name",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "customer",
            "customer_name",
            "food_item",
            "food_name",
            "rating",
            "comment",
            "is_approved",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer",
            "customer_name",
            "food_name",
            "is_approved",
            "created_at",
            "updated_at",
        ]

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )
        return value

    def validate_food_item(self, food_item):
        if not food_item:
            raise serializers.ValidationError(
                "A valid food item is required."
            )
        return food_item

    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return attrs

        food_item = attrs.get(
            "food_item",
            getattr(self.instance, "food_item", None),
        )

        if food_item:
            existing_reviews = Review.objects.filter(
                customer=request.user,
                food_item=food_item,
            )

            # Exclude the current review when updating it.
            if self.instance:
                existing_reviews = existing_reviews.exclude(
                    pk=self.instance.pk
                )

            if existing_reviews.exists():
                raise serializers.ValidationError({
                    "food_item": (
                        "You have already reviewed this food item."
                    )
                })

        return attrs
