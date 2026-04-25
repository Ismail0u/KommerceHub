"""
authentication/managers.py
--------------------------
Custom manager for the User model.

Why a custom UserManager?
Django's AbstractBaseUser requires defining how a user is created
when USERNAME_FIELD is customized. Here we support two identification modes:
- Merchant: email (standard)
- Seller  : phone (mobile-first, no email required)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.models import BaseUserManager

if TYPE_CHECKING:
    from authentication.models import User


class UserManager(BaseUserManager["User"]):
    """
    Custom manager for the KommerceHub User model.

    Handles two user types:
    - Merchant: authenticated via email
    - Seller  : authenticated via phone (no email required)
    """

    def create_user(
        self,
        password: str,
        email: str | None = None,
        phone: str | None = None,
        **extra_fields: Any,
    ) -> "User":
        """
        Create and persist a standard user.

        Args:
            password: Raw password (will be hashed using Django's configured hasher, e.g., Argon2).
            email: Email address (required for merchants).
            phone: Phone number (required for sellers).
            **extra_fields: Additional User model fields (role, etc.).

        Returns:
            Persisted User instance.

        Raises:
            ValueError: If neither email nor phone is provided.
        """
        if not email and not phone:
            raise ValueError(
                "A user must have at least an email or a phone number."
            )

        if email:
            email = self.normalize_email(email)

        user: "User" = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: Any,
    ) -> "User":
        """
        Create a superuser (platform admin).

        Primarily used by `manage.py createsuperuser`.

        Args:
            email: Admin email.
            password: Raw password.
            **extra_fields: Additional fields.

        Returns:
            User instance with full admin privileges.

        Raises:
            ValueError: If is_staff or is_superuser are not set to True.
        """
        # Local import to avoid circular dependencies
        from authentication.models import UserRole

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)