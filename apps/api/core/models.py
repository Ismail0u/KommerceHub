"""
core/models.py
--------------
Abstract base model inherited by all  models in the project.

Principle : "Convention over Configuration"
instead of repeating id/created_at/updated_at/is_deleted in each model,
they are centralized here. A change here propagates evrywhere .

Analogy : this is the base "mixin", similar to a 'BaseEntity' in Java/Spring.
"""

import uuid

from django.db import models
from django.utils import timezone

from core.managers import ActiveManager


class BaseModel(models.Model):
    """
    Abstract base model for all KommerceHub models.

    Provides :
    - Auto-generated UUID as primary key (no sequential ID exposed in API)
    - automatic Timestamps  (created_at, updated_at)
    - Soft delete (is_deleted) — Data is NEVER physically deleted
    - `objects` Manager that automatically filters out deleted records
    - `all_objects` Manager for admin/audit use cases

    Absolute rule : never call `.delete()` directly on a model inheriting 
    from BaseModel. Always use `.soft_delete()`.

    Example:
        class Product(BaseModel):
            name = models.CharField(max_length=255)
            # id, created_at, updated_at, is_deleted → automatically inherited

        product = Product.objects.get(id=some_uuid)
        product.soft_delete()  #  Soft delete
        Product.objects.filter(name="foo")  # → automatically excludes deleted records
        Product.all_objects.filter(is_deleted=True)  # → access archived data 
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identifiant unique universel (UUID v4), non-séquentiel.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création (automatique, non modifiable).",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date de dernière modification (automatique).",
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,  # Index critique : toutes les requêtes filtrent sur ce champ
        help_text="Soft delete — l'enregistrement est masqué mais conservé en base.",
    )

    # ── Managers ──────────────────────────────────────────────────────────────
    # `objects` : usage normal → exclut les supprimés
    objects = ActiveManager()
    # `all_objects` : usage admin/audit → inclut tout
    all_objects = models.Manager()

    class Meta:
        abstract = True
        # Ordre par défaut : plus récent en premier (override possible dans les sous-classes)
        ordering = ["-created_at"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"

    def soft_delete(self) -> None:
        """
        Suppression logique (soft delete).

        Marque l'enregistrement comme supprimé sans le retirer de la base.
        Préserve l'intégrité des données d'audit et de la conformité RGPD.

        Note:
            Utilise `update_fields` pour n'émettre qu'un UPDATE partiel
            (performance) et éviter d'écraser des champs modifiés en mémoire.
        """
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])

    def restore(self) -> None:
        """
        Restaure un enregistrement soft-deleted.

        Utile pour les annulations d'opérations ou les erreurs de suppression.
        """
        self.is_deleted = False
        self.save(update_fields=["is_deleted", "updated_at"])
