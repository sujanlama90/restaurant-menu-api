from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReviewPermission(BasePermission):

    def has_permission(self, request, view):
        # Anyone can view reviews (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Login is required for write operations
        if not request.user or not request.user.is_authenticated:
            return False

        role = getattr(request.user, "role", None)

        # Only customers can create reviews
        if view.action == "create":
            return role == "CUSTOMER"

        # Staff and admins can perform moderation actions
        if view.action == "approve":
            return role in ["STAFF", "ADMIN"]

        # Customers, staff, and admins can attempt updates/deletes.
        # Object-level permission checks determine whose review
        # they are allowed to modify.
        return role in ["CUSTOMER", "STAFF", "ADMIN"]

    def has_object_permission(self, request, view, obj):
        # Anyone can access objects available in the queryset
        if request.method in SAFE_METHODS:
            return True

        role = getattr(request.user, "role", None)

        # Staff and admins can manage any review
        if role in ["STAFF", "ADMIN"]:
            return True

        # Customers can modify or delete only their own reviews
        return obj.customer_id == request.user.id
