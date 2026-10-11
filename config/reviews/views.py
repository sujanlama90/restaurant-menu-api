from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Q
from .models import Review
from .serializer import ReviewSerializer
from .permissions import ReviewPermission
from .custom_pagination import CustomPagination

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [ReviewPermission]
    pagination_class=CustomPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["food_item", "rating"]
    search_fields = ["comment", "food_item__name"]
    ordering_fields = ["rating", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

        queryset = Review.objects.select_related(
            "customer",
            "food_item",
        )

        # Public users can see approved reviews only.
        if not user.is_authenticated:
            return queryset.filter(is_approved=True)

        role = getattr(user, "role", None)

        # Staff and admins can see all reviews.
        if role in ["STAFF", "ADMIN"]:
            return queryset

        # Customers can see approved reviews and their own reviews.
        return queryset.filter(
            Q(is_approved=True) | Q(customer=user)
        )

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        url_path="approve",
    )
    def approve(self, request, pk=None):
        # Only staff and admins can approve reviews.
        if getattr(request.user, "role", None) not in [
            "STAFF",
            "ADMIN",
        ]:
            raise PermissionDenied(
                "Only staff or admins can approve reviews."
            )

        review = self.get_object()
        review.is_approved = True
        review.save(update_fields=["is_approved", "updated_at"])

        return Response(
            self.get_serializer(review).data,
            status=status.HTTP_200_OK,
        )
