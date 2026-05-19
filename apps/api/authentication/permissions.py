"""
authentication/permissions.py
-----------------------------
DRF permission classes for KommerceHub RBAC system.

Architecture:
    We create granular permission classes instead of a single "god object".
    Each ViewSet composes permissions based on its needs:

    class ProductViewSet(ModelViewSet):
        permission_classes = [IsAuthenticated, IsMerchant, IsNotForcedPasswordChange]

DRF Pattern:
    has_permission()         → Checked BEFORE accessing the view (endpoint level)
    has_object_permission() → Checked AFTER, when the object is available (object level)

All permissions inherit from BasePermission and return a boolean.
"""

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from authentication.models import UserRole


class IsAdmin(BasePermission):
    """
    Allows access only to platform administrators.

    Usage: Merchant validation endpoints, global analytics.
    """

    message = "Access restricted to platform administrators."

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


class IsMerchant(BasePermission):
    """
    Allows access only to merchants.

    Usage: Product CRUD, seller management, dashboard.
    """

    message = "Access restricted to merchants."

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.MERCHANT
        )


class IsSeller(BasePermission):
    """
    Allows access only to sellers.

    Usage: Sales recording via mobile POS.
    """

    message = "Access restricted to sellers."

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.SELLER
        )


class IsMerchantOrSeller(BasePermission):
    """
    Allows access to both merchants and sellers.

    Usage: Product browsing, sales history.
    """

    message = "Access restricted to merchants and sellers."

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {UserRole.MERCHANT, UserRole.SELLER}
        )


class IsAdminOrMerchant(BasePermission):
    """
    Allows access to admins and merchants.

    Usage: Sales cancellation, exports, reporting.
    """

    message = "Access restricted to administrators and merchants."

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {UserRole.ADMIN, UserRole.MERCHANT}
        )


class IsNotForcedPasswordChange(BasePermission):
    """
    Blocks access if the user is required to change their password.

    CRITICAL: This permission must be applied to ALL ViewSets
    except the /auth/change-password/ endpoint.

    Analogy: A "locked" bank account until identity confirmation.

    Returns:
        403 with { "detail": "...", "force_password_change": true }
        → The frontend/mobile app intercepts this and redirects
          to the password change screen.
    """

    message = {
        "detail": "You must change your password before continuing.",
        "force_password_change": True,
    }

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False  # Let IsAuthenticated handle this case
        return not request.user.must_change_password