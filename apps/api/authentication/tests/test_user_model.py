"""
authentication/tests/test_user_model.py
---------------------------------------
Unit tests for: User, UserManager, UserRole, and RBAC permissions.

Organization:
- TestUserCreation        → creation via UserManager
- TestUserRole            → RBAC properties (is_admin, is_merchant, is_seller)
- TestUserConstraints     → DB constraints (email OR phone required)
- TestMustChangePassword  → first-login blocking flag
- TestRBACPermissions     → DRF permission classes

Fixtures used: conftest.py (admin_user, merchant_user, seller_user)
"""

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.test import APIRequestFactory

from authentication.models import UserRole
from authentication.permissions import (
    IsAdmin,
    IsAdminOrMerchant,
    IsMerchant,
    IsMerchantOrSeller,
    IsNotForcedPasswordChange,
    IsSeller,
)

User = get_user_model()


# ── Tests: User creation ─────────────────────────────────────────────────────


@pytest.mark.django_db
class TestUserCreation:
    """Validate correct user creation."""

    def test_create_merchant_with_email(self):
        """A merchant is created with an email."""
        user = User.objects.create_user(
            email="merchant@test.com",
            password="SecurePass!123",
            role=UserRole.MERCHANT,
        )
        assert user.email == "merchant@test.com"
        assert user.phone is None
        assert user.role == UserRole.MERCHANT

    def test_create_seller_with_phone(self):
        """A seller is created with a phone number (no email)."""
        user = User.objects.create_user(
            phone="+22796000001",
            password="TempPass!456",
            role=UserRole.SELLER,
        )
        assert user.phone == "+22796000001"
        assert user.email is None
        assert user.role == UserRole.SELLER

    def test_password_is_hashed(self):
        """Password must be hashed (never stored in plain text)."""
        user = User.objects.create_user(
            email="hashed@test.com",
            password="PlainPassword!",
            role=UserRole.MERCHANT,
        )
        assert user.password != "PlainPassword!"
        assert user.check_password("PlainPassword!") is True

    def test_email_is_normalized(self):
        """Emails are normalized (domain lowercased)."""
        user = User.objects.create_user(
            email="Merchant@TEST.COM",
            password="Pass!123",
            role=UserRole.MERCHANT,
        )
        assert user.email == "Merchant@test.com"

    def test_create_user_without_email_and_phone_raises(self):
        """Creating a user without email and phone must raise ValueError."""
        with pytest.raises(ValueError, match="email or a phone number"):
            User.objects.create_user(
                password="Pass!123",
                role=UserRole.MERCHANT,
            )

    def test_create_superuser_sets_admin_role(self):
        """create_superuser() must automatically assign ADMIN role."""
        admin = User.objects.create_superuser(
            email="superadmin@kommercehub.app",
            password="AdminPass!123",
        )
        assert admin.role == UserRole.ADMIN
        assert admin.is_staff is True
        assert admin.is_superuser is True

    def test_user_id_is_uuid(self):
        """User ID must be a UUID (not a sequential integer)."""
        import uuid
        user = User.objects.create_user(
            email="uuid@test.com",
            password="Pass!123",
            role=UserRole.MERCHANT,
        )
        assert isinstance(user.id, uuid.UUID)

    def test_new_user_is_active_by_default(self):
        """A new user must be active by default."""
        user = User.objects.create_user(
            email="active@test.com",
            password="Pass!123",
            role=UserRole.MERCHANT,
        )
        assert user.is_active is True

    def test_new_user_must_change_password_false_by_default(self):
        """must_change_password is False by default (merchant)."""
        user = User.objects.create_user(
            email="noforce@test.com",
            password="Pass!123",
            role=UserRole.MERCHANT,
        )
        assert user.must_change_password is False


# ── Tests: DB constraints ────────────────────────────────────────────────────


@pytest.mark.django_db
class TestUserConstraints:
    """Validate database integrity constraints."""

    def test_email_must_be_unique(self):
        """Two users cannot share the same email."""
        User.objects.create_user(
            email="duplicate@test.com",
            password="Pass!123",
            role=UserRole.MERCHANT,
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="duplicate@test.com",
                password="AnotherPass!",
                role=UserRole.MERCHANT,
            )

    def test_phone_must_be_unique(self):
        """Two users cannot share the same phone number."""
        User.objects.create_user(
            phone="+22796000001",
            password="Pass!123",
            role=UserRole.SELLER,
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                phone="+22796000001",
                password="AnotherPass!",
                role=UserRole.SELLER,
            )


# ── Tests: RBAC roles ────────────────────────────────────────────────────────


@pytest.mark.django_db
class TestUserRole:
    """Validate RBAC properties on the User model."""

    def test_admin_is_admin(self, admin_user):
        """admin_user.is_admin == True."""
        assert admin_user.is_admin is True
        assert admin_user.is_merchant is False
        assert admin_user.is_seller is False

    def test_merchant_is_merchant(self, merchant_user):
        """merchant_user.is_merchant == True."""
        assert merchant_user.is_merchant is True
        assert merchant_user.is_admin is False
        assert merchant_user.is_seller is False

    def test_seller_is_seller(self, seller_user):
        """seller_user.is_seller == True."""
        assert seller_user.is_seller is True
        assert seller_user.is_admin is False
        assert seller_user.is_merchant is False

    def test_user_role_choices_values(self):
        """TextChoices values must be correct."""
        assert UserRole.ADMIN == "admin"
        assert UserRole.MERCHANT == "merchant"
        assert UserRole.SELLER == "seller"

    def test_str_returns_email_for_merchant(self, merchant_user):
        """__str__ returns email for merchant."""
        assert str(merchant_user) == merchant_user.email

    def test_str_returns_phone_for_seller(self, seller_user):
        """__str__ returns phone for seller."""
        assert str(seller_user) == seller_user.phone


# ── Tests: must_change_password ─────────────────────────────────────────────


@pytest.mark.django_db
class TestMustChangePassword:
    """Validate first-login blocking flag."""

    def test_seller_created_with_must_change_password(self, seller_user):
        """Seller is created with must_change_password=True."""
        assert seller_user.must_change_password is True

    def test_flag_can_be_reset_after_change(self, seller_user):
        """Flag resets after password change."""
        seller_user.set_password("NewSecurePass!999")
        seller_user.must_change_password = False
        seller_user.save()

        refreshed = User.objects.get(id=seller_user.id)
        assert refreshed.must_change_password is False


# ── Tests: DRF RBAC permissions ─────────────────────────────────────────────


class TestRBACPermissions:
    """
    Validate DRF permission classes.

    Note: These tests do NOT require DB access.
    Users are mocked in memory (not persisted).
    """

    factory = APIRequestFactory()

    def _make_request(self, user):
        """Create a mock DRF request with an authenticated user."""
        request = self.factory.get("/")
        request.user = user
        return request

    def _make_user(self, role: str, must_change: bool = False):
        """Create an in-memory User (not saved)."""
        user = User(role=role, must_change_password=must_change)
        user.is_authenticated = True
        return user

    # IsAdmin

    def test_is_admin_allows_admin(self):
        request = self._make_request(self._make_user(UserRole.ADMIN))
        assert IsAdmin().has_permission(request, None) is True

    def test_is_admin_blocks_merchant(self):
        request = self._make_request(self._make_user(UserRole.MERCHANT))
        assert IsAdmin().has_permission(request, None) is False

    def test_is_admin_blocks_seller(self):
        request = self._make_request(self._make_user(UserRole.SELLER))
        assert IsAdmin().has_permission(request, None) is False

    # IsMerchant

    def test_is_merchant_allows_merchant(self):
        request = self._make_request(self._make_user(UserRole.MERCHANT))
        assert IsMerchant().has_permission(request, None) is True

    def test_is_merchant_blocks_seller(self):
        request = self._make_request(self._make_user(UserRole.SELLER))
        assert IsMerchant().has_permission(request, None) is False

    # IsSeller

    def test_is_seller_allows_seller(self):
        request = self._make_request(self._make_user(UserRole.SELLER))
        assert IsSeller().has_permission(request, None) is True

    def test_is_seller_blocks_merchant(self):
        request = self._make_request(self._make_user(UserRole.MERCHANT))
        assert IsSeller().has_permission(request, None) is False

    # IsMerchantOrSeller

    def test_is_merchant_or_seller_allows_merchant(self):
        request = self._make_request(self._make_user(UserRole.MERCHANT))
        assert IsMerchantOrSeller().has_permission(request, None) is True

    def test_is_merchant_or_seller_allows_seller(self):
        request = self._make_request(self._make_user(UserRole.SELLER))
        assert IsMerchantOrSeller().has_permission(request, None) is True

    def test_is_merchant_or_seller_blocks_admin(self):
        request = self._make_request(self._make_user(UserRole.ADMIN))
        assert IsMerchantOrSeller().has_permission(request, None) is False

    # IsNotForcedPasswordChange

    def test_not_forced_allows_normal_user(self):
        request = self._make_request(self._make_user(UserRole.SELLER, must_change=False))
        assert IsNotForcedPasswordChange().has_permission(request, None) is True

    def test_not_forced_blocks_user_with_flag(self):
        request = self._make_request(self._make_user(UserRole.SELLER, must_change=True))
        assert IsNotForcedPasswordChange().has_permission(request, None) is False

    # IsAdminOrMerchant

    def test_is_admin_or_merchant_allows_admin(self):
        request = self._make_request(self._make_user(UserRole.ADMIN))
        assert IsAdminOrMerchant().has_permission(request, None) is True

    def test_is_admin_or_merchant_allows_merchant(self):
        request = self._make_request(self._make_user(UserRole.MERCHANT))
        assert IsAdminOrMerchant().has_permission(request, None) is True

    def test_is_admin_or_merchant_blocks_seller(self):
        request = self._make_request(self._make_user(UserRole.SELLER))
        assert IsAdminOrMerchant().has_permission(request, None) is False