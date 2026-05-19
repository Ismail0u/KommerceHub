"""
core/models.py
--------------
Abstract base model inherited by all models in the project.

Principle: "Convention over Configuration"
Instead of repeating id/created_at/updated_at/is_deleted in each model,
they are centralized here. A change here propagates everywhere.

Analogy: this is the base "mixin", similar to a 'BaseEntity' in Java/Spring.
"""

import uuid

from django.db import models
from django.utils import timezone

from core.managers import ActiveManager


class BaseModel(models.Model):
    """
    Abstract base model for all KommerceHub models.

    Provides:
    - Auto-generated UUID as primary key (no sequential ID exposed in API)
    - Automatic timestamps (created_at, updated_at)
    - Soft delete (is_deleted) — data is NEVER physically deleted
    - `objects` manager that automatically filters out deleted records
    - `all_objects` manager for admin/audit use cases

    Absolute rule: never call `.delete()` directly on a model inheriting
    from BaseModel. Always use `.soft_delete()`.

    Example:
        class Product(BaseModel):
            name = models.CharField(max_length=255)
            # id, created_at, updated_at, is_deleted → automatically inherited

        product = Product.objects.get(id=some_uuid)
        product.soft_delete()  # Soft delete
        Product.objects.filter(name="foo")  # → automatically excludes deleted records
        Product.all_objects.filter(is_deleted=True)  # → access archived data
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Universally unique identifier (UUID v4), non-sequential.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation timestamp (automatic, not editable).",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update timestamp (automatic).",
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,  # Critical index: most queries filter on this field
        help_text="Soft delete — record is hidden but preserved in the database.",
    )

    # ── Managers ──────────────────────────────────────────────────────────────
    # `objects`: standard usage → excludes deleted records
    objects = ActiveManager()
    # `all_objects`: admin/audit usage → includes all records
    all_objects = models.Manager()

    class Meta:
        abstract = True
        # Default ordering: newest first (can be overridden in subclasses)
        ordering = ["-created_at"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"

    def soft_delete(self) -> None:
        """
        Logical deletion (soft delete).

        Marks the record as deleted without removing it from the database.
        Preserves audit integrity and compliance requirements (e.g., GDPR).

        Note:
            Uses `update_fields` to perform a partial UPDATE (performance)
            and avoid overwriting other in-memory changes.
        """
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])

    def restore(self) -> None:
        """
        Restore a soft-deleted record.

        Useful for undo operations or accidental deletions.
        """
        self.is_deleted = False
        self.save(update_fields=["is_deleted", "updated_at"])
