"""
conftest.py
-----------
Shared pytest fixtures available across all test modules.

Convention:
- Fixtures requiring database access need either @pytest.mark.django_db
  on the test or the `db` fixture as a parameter.
- Factories (e.g., factory_boy) are defined in each app/module-level conftest.
- This file contains globally reusable fixtures.
"""

import pytest
from django.contrib.auth import get_user_model

from authentication.models import UserRole

User = get_user_model()


# ── Base fixtures ─────────────────────────────────────────────────────────────


@pytest.fixture
def admin_user(db):
    """Platform administrator user."""
    return User.objects.create_user(
        email="admin@kommercehub.app",
        password="AdminSecure!123",
        role=UserRole.ADMIN,
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def merchant_user(db):
    """Merchant user."""
    return User.objects.create_user(
        email="merchant@boutique-niger.com",
        password="MerchantSecure!123",
        role=UserRole.MERCHANT,
    )


@pytest.fixture
def seller_user(db):
    """Seller user with a temporary password."""
    return User.objects.create_user(
        phone="+22796000001",
        password="TempPass!456",
        role=UserRole.SELLER,
        must_change_password=True,
    )


@pytest.fixture
def seller_user_active(db):
    """Seller user who has already changed their password."""
    return User.objects.create_user(
        phone="+22796000002",
        password="NewPass!789",
        role=UserRole.SELLER,
        must_change_password=False,
    )