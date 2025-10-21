# ==============================================================
# modele/type_chambre.py
# Modèle SQLAlchemy représentant la table "type_chambre" dans la BD.
# Chaque type de chambre définit une catégorie (simple, double, suite)
# avec sa description et ses limites de prix.
# ==============================================================

from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from .base import Base

# Import seulement pour la vérification des types (évite les imports circulaires)
if TYPE_CHECKING:
    from .chambre import Chambre

# --------------------------------------------------------------
# Classe principale TypeChambre
# Représente un type de chambre (ex : simple, double, suite)
# --------------------------------------------------------------
class TypeChambre(Base):
    __tablename__ = "type_chambre"

    # Identifiant unique du type de chambre (UUID auto-généré)
    id_type_chambre: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    # Nom du type (ex : "simple", "double", "suite exécutive")
    nom_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # Prix plancher de base pour ce type de chambre
    prix_plancher: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Prix plafond (optionnel, souvent utilisé pour indiquer une fourchette)
    prix_plafond: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Courte description du type (vue, taille, services inclus, etc.)
    description_chambre: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Relation vers les chambres associées à ce type
    # Un type de chambre peut être lié à plusieurs chambres physiques
    chambres: Mapped[List["Chambre"]] = relationship("Chambre", back_populates="type_chambre")
