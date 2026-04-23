"""
core/managers.py
----------------
Custom Django ORM managers shared across all models in the project.

Why a separate manager?
- Separation of concerns (SRP)
- Independently testable from the model
- Reusable across all models inheriting from BaseModel
"""

from django.db import models


class ActiveManager(models.Manager):
    """
    Default manager that automatically excludes soft-deleted records.

    Usage:
        Product.objects.all()          # → only active records (is_deleted=False)
        Product.all_objects.all()      # → all records, including deleted ones
        Product.objects.filter(...)   # → filters applied only on active records

    Note:
        This manager is assigned to `objects` on BaseModel.
        `all_objects` uses Django’s default manager for admin/audit use cases.
    """

    def get_queryset(self) -> models.QuerySet:
        """Return only non-deleted records."""
        return super().get_queryset().filter(is_deleted=False)