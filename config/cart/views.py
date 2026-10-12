from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import ScopedRateThrottle

from django.db import transaction
from .models import Cart, CartItem
from .serializer import CartSerializer, CartItemSerializer

class CartView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope ='cart' #for custom thottle 
    throttle_classes=[ScopedRateThrottle]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return Cart.objects.filter(
            customer=self.request.user
        ).prefetch_related("items__food_item")

    def get_user_cart(self):
        cart, _ = Cart.objects.get_or_create(
            customer=self.request.user
        )
        return cart

    def list(self, request, *args, **kwargs):
        cart = self.get_user_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(
            customer=request.user
        )
        serializer = self.get_serializer(cart)

        return Response(
            serializer.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )

    def retrieve(self, request, *args, **kwargs):
        cart = self.get_user_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")

    @action(detail=False, methods=["post"], url_path="item")
    @transaction.atomic
    def add_item(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        food_item = serializer.validated_data["food_item"]
        quantity = serializer.validated_data["quantity"]

        cart = self.get_user_cart()

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            food_item=food_item,
            defaults={"quantity": quantity},
        )

        if not created:
            new_quantity = item.quantity + quantity

            if new_quantity > 99:
                raise ValidationError({
                    "quantity": "Total quantity cannot exceed 99."
                })

            item.quantity = new_quantity
            item.save(update_fields=["quantity", "updated_at"])

        cart = self.get_user_cart()
        response_serializer = self.get_serializer(cart)

        return Response(
            response_serializer.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )

    @action(detail=False, methods=["patch"], url_path="update-item")
    @transaction.atomic
    def update_item(self, request):
        item_id = request.data.get("item_id")

        if item_id is None:
            raise ValidationError({
                "item_id": "This field is required."
            })

        cart = self.get_user_cart()

        try:
            item = cart.items.get(pk=item_id)
        except CartItem.DoesNotExist:
            return Response(
                {"detail": "Cart item not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CartItemSerializer(
            item,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        cart = self.get_user_cart()

        return Response(self.get_serializer(cart).data)

    @action(detail=False, methods=["delete"], url_path="remove-item")
    @transaction.atomic
    def remove_item(self, request):
        item_id = request.query_params.get("item_id")

        if item_id is None:
            raise ValidationError({
                "item_id": "This query parameter is required."
            })

        cart = self.get_user_cart()

        deleted, _ = cart.items.filter(pk=item_id).delete()

        if deleted == 0:
            return Response(
                {"detail": "Cart item not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = self.get_user_cart()

        return Response(self.get_serializer(cart).data)