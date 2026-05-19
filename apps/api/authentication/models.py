"""
authentication/models.py
------------------------
Custom User model for KommerceHub.

Key architectural decisions:
1. Inherits from AbstractBaseUser (not AbstractUser) for full control
2. UserRole uses TextChoices → human-readable values in DB and API
3. email AND phone are nullable since each role uses one or the other
4. must_change_password blocks API access via a dedicated permission
5. UUIDs everywhere → no sequential IDs exposed (security, no enumeration)
"""

import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.managers import UserManager


class UserRole(models.TextChoices):
    """
    System RBAC roles.

    Permission hierarchy:
    ADMIN > MERCHANT > SELLER

    Note:
        TextChoices are stored as strings in DB ("admin", "merchant", "seller")
        instead of integers → better readability in SQL queries and logs.
    """

    ADMIN = "admin", _("Administrator")
    MERCHANT = "merchant", _("Merchant")
    SELLER = "seller", _("Seller")


class User(AbstractBaseUser, PermissionsMixin):
    """
    Core User model for KommerceHub.

    Two authentication modes depending on role:
    - Admin/Merchant: email + password
    - Seller        : phone + temporary password

    Critical field:
        must_change_password:
            If True, ALL API requests return 403 (except change-password endpoint).
            This is enforced at the API level, not just UI.

    Relationships:
        User (1) ─── (1) Merchant   [if role == MERCHANT]
        User (1) ─── (1) Seller     [if role == SELLER]

    Example:
        # Create a merchant
        user = User.objects.create_user(
            email="merchant@shop.com",
            password="temp_pwd_123",
            role=UserRole.MERCHANT,
        )

        # Create a seller (no email)
        user = User.objects.create_user(
            phone="+22796000001",
            password="temp_pwd_456",
            role=UserRole.SELLER,
            must_change_password=True,
        )
    """

    # ── Identity ──────────────────────────────────────────────────────────────
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        help_text="Email for merchant/admin. Null for sellers.",
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text="Phone number for sellers. Null for merchants/admins.",
    )

    # ── RBAC ──────────────────────────────────────────────────────────────────
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        help_text="Role determining access permissions.",
    )

    # ── Status ────────────────────────────────────────────────────────────────
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive users cannot authenticate.",
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Grants access to Django admin interface.",
    )
    must_change_password = models.BooleanField(
        default=False,
        help_text=(
            "If True, BLOCKS access to all APIs except /auth/change-password/. "
            "Automatically enabled for seller accounts."
        ),
    )

    # ── Timestamps ────────────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ── Manager ───────────────────────────────────────────────────────────────
    objects = UserManager()

    # Required by AbstractBaseUser
    # Email is used as primary identifier (for merchants/admins)
    # Sellers authenticate via phone, but internally email remains the USERNAME_FIELD
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [
            models.Index(fields=["role"], name="user_role_idx"),
            models.Index(fields=["is_active"], name="user_is_active_idx"),
        ]
        constraints = [
            # Business rule: a user must have either email OR phone (not both null)
            models.CheckConstraint(
                check=~models.Q(email=None, phone=None),
                name="user_email_or_phone_required",
            ),
        ]

    def __str__(self) -> str:
        return self.email or self.phone or str(self.id)

    def __repr__(self) -> str:
        return f"<User id={self.id} role={self.role}>"

    # ── RBAC Properties ───────────────────────────────────────────────────────
    # Prefer these properties instead of checking role directly
    # → if role names change, only one place to update

    @property
    def is_admin(self) -> bool:
        """Platform administrator (global access)."""
        return self.role == UserRole.ADMIN

    @property
    def is_merchant(self) -> bool:
        """Merchant (access limited to own data)."""
        return self.role == UserRole.MERCHANT

    @property
    def is_seller(self) -> bool:
        """Seller (restricted to sales operations)."""
        return self.role == UserRole.SELLER