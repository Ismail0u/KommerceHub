"""
core/tests/test_base_model.py
-----------------------------
Unit tests for BaseModel and ActiveManager.

Testing strategy:
- A concrete model `ConcreteModel` is created to test the abstract model.
- Each test covers ONE specific behavior (FIRST principle: Fast, Isolated).
- Tests are organized by behavior classes.

Target coverage: 100% for core/models.py and core/managers.py
"""

import uuid

import pytest
from django.db import models

from core.models import BaseModel


# ── Test model (concrete, used to test the abstract model) ─────────────────────
# We define a temporary model for testing purposes.
# Django will treat it as a real model only within tests thanks to
# @pytest.mark.django_db and the test database.

class ConcreteModel(BaseModel):
    """Minimal concrete model used to test BaseModel."""

    name = models.CharField(max_length=100, default="test")

    class Meta(BaseModel.Meta):
        # `app_label` is required for models defined outside a Django app
        app_label = "core"


# ── Tests: UUID and timestamps ────────────────────────────────────────────────


@pytest.mark.django_db
class TestBaseModelIdentity:
    """Validate identity fields: UUID and timestamps."""

    def test_id_is_uuid(self, db):
        """ID must be an auto-generated UUID v4."""
        obj = ConcreteModel.objects.create(name="test")
        assert isinstance(obj.id, uuid.UUID)

    def test_id_is_unique_per_instance(self, db):
        """Each instance must have a unique UUID."""
        obj1 = ConcreteModel.objects.create(name="a")
        obj2 = ConcreteModel.objects.create(name="b")
        assert obj1.id != obj2.id

    def test_id_is_not_editable(self):
        """ID must not be editable (editable=False)."""
        field = ConcreteModel._meta.get_field("id")
        assert field.editable is False

    def test_created_at_is_set_on_creation(self, db):
        """created_at must be automatically set on creation."""
        obj = ConcreteModel.objects.create(name="test")
        assert obj.created_at is not None

    def test_updated_at_changes_on_save(self, db):
        """updated_at must update on each save."""
        obj = ConcreteModel.objects.create(name="initial")
        first_updated = obj.updated_at
        obj.name = "modified"
        obj.save()
        assert obj.updated_at > first_updated


# ── Tests: Soft Delete ───────────────────────────────────────────────────────


@pytest.mark.django_db
class TestSoftDelete:
    """Validate soft delete behavior."""

    def test_new_object_is_not_deleted(self, db):
        """A new object must have is_deleted=False by default."""
        obj = ConcreteModel.objects.create(name="fresh")
        assert obj.is_deleted is False

    def test_soft_delete_sets_flag(self, db):
        """soft_delete() must set is_deleted to True."""
        obj = ConcreteModel.objects.create(name="to_delete")
        obj.soft_delete()
        assert obj.is_deleted is True

    def test_soft_delete_persists_in_db(self, db):
        """soft_delete() must persist the flag in the database."""
        obj = ConcreteModel.objects.create(name="to_delete")
        obj.soft_delete()
        # Reload from DB to verify persistence
        refreshed = ConcreteModel.all_objects.get(id=obj.id)
        assert refreshed.is_deleted is True

    def test_soft_deleted_object_still_exists_in_db(self, db):
        """A soft-deleted object must NOT be physically deleted."""
        obj = ConcreteModel.objects.create(name="to_delete")
        obj_id = obj.id
        obj.soft_delete()
        # Object still exists in DB (via all_objects)
        assert ConcreteModel.all_objects.filter(id=obj_id).exists()

    def test_restore_undeletes_object(self, db):
        """restore() must reset is_deleted to False."""
        obj = ConcreteModel.objects.create(name="deleted_then_restored")
        obj.soft_delete()
        obj.restore()
        assert obj.is_deleted is False

    def test_restore_makes_object_visible_again(self, db):
        """After restore(), object must be visible again via objects manager."""
        obj = ConcreteModel.objects.create(name="to_restore")
        obj_id = obj.id
        obj.soft_delete()
        obj.restore()
        assert ConcreteModel.objects.filter(id=obj_id).exists()


# ── Tests: ActiveManager ─────────────────────────────────────────────────────


@pytest.mark.django_db
class TestActiveManager:
    """Ensure the default manager excludes soft-deleted records."""

    def test_objects_excludes_soft_deleted(self, db):
        """objects.all() must exclude soft-deleted records."""
        active = ConcreteModel.objects.create(name="active")
        deleted = ConcreteModel.objects.create(name="deleted")
        deleted.soft_delete()

        qs = ConcreteModel.objects.all()
        ids = list(qs.values_list("id", flat=True))

        assert active.id in ids
        assert deleted.id not in ids

    def test_all_objects_includes_soft_deleted(self, db):
        """all_objects.all() must include soft-deleted records."""
        active = ConcreteModel.objects.create(name="active")
        deleted = ConcreteModel.objects.create(name="deleted")
        deleted.soft_delete()

        qs = ConcreteModel.all_objects.all()
        ids = list(qs.values_list("id", flat=True))

        assert active.id in ids
        assert deleted.id in ids

    def test_objects_filter_applies_to_active_only(self, db):
        """objects.filter() must apply only to active records."""
        ConcreteModel.objects.create(name="active_foo")
        deleted_foo = ConcreteModel.objects.create(name="deleted_foo")
        deleted_foo.soft_delete()

        results = ConcreteModel.objects.filter(name__contains="foo")
        assert results.count() == 1
        assert results.first().name == "active_foo"

    def test_objects_count_excludes_deleted(self, db):
        """objects.count() must exclude soft-deleted records."""
        ConcreteModel.objects.create(name="one")
        ConcreteModel.objects.create(name="two")
        to_delete = ConcreteModel.objects.create(name="three")
        to_delete.soft_delete()

        assert ConcreteModel.objects.count() == 2
        assert ConcreteModel.all_objects.count() == 3


# ── Tests: Repr ──────────────────────────────────────────────────────────────


@pytest.mark.django_db
class TestBaseModelRepr:
    """Validate string representation."""

    def test_repr_contains_class_name_and_id(self, db):
        """__repr__ must include class name and ID."""
        obj = ConcreteModel.objects.create(name="repr_test")
        assert "ConcreteModel" in repr(obj)
        assert str(obj.id) in repr(obj)