from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions,authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters

from .models import Category,FoodItem
from .serailizer import CategorySerializer,FoodItemSerializer
from .permissions import IsRestaurantStaff
from .custom_pagination import CustomPagination


class Categories(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    pagination_class =CustomPagination
    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.role in ["STAFF", "ADMIN"]:
            return Category.objects.all()

        return Category.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsRestaurantStaff]

        return [permission() for permission in permission_classes]
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active"])

class FoodItemView(viewsets.ModelViewSet):
    serializer_class=FoodItemSerializer
    authentication_classes=[JWTAuthentication]
    pagination_class =CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['category', 'food_type']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        user = self.request.user
        queryset = FoodItem.objects.select_related('category')

        if (
            user.is_authenticated
            and user.is_active
            and user.role in ['STAFF', 'ADMIN']
        ):
            return queryset

        return queryset.filter(
            is_available=True,
            category__is_active=True,
        )

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
                IsRestaurantStaff,
            ]

        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        instance.is_available = False
        instance.save(update_fields=['is_available'])
    