# ==============================================================
# modele/usager.py
# Modèle SQLAlchemy représentant la table "usager" dans la BD.
# Chaque usager correspond à un client ou un administrateur de l’hôtel.
# ==============================================================

from __future__ import annotations

from typing import List, TYPE_CHECKING
from sqlalchemy import String, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from .base import Base

# Import seulement utilisé pour la vérification des types
# afin d’éviter les imports circulaires (ne s’exécute pas à l’exécution)
if TYPE_CHECKING:
    from .reservation import Reservation

# --------------------------------------------------------------
# Classe principale Usager
# Représente un utilisateur de la plateforme (client ou admin)
# --------------------------------------------------------------
class Usager(Base):
    __tablename__ = "usager"

    # Identifiant unique de l’usager (UUID auto-généré)
    id_usager: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    # Prénom de l’usager
    prenom: Mapped[str] = mapped_column(String(50), nullable=False)

    # Nom de famille de l’usager
    nom: Mapped[str] = mapped_column(String(50), nullable=False)

    # Adresse complète de l’usager
    adresse: Mapped[str] = mapped_column(String(100), nullable=False)

    # Numéro de téléphone mobile (format fixe à 15 caractères)
    mobile: Mapped[str] = mapped_column(CHAR(15), nullable=False)

    # Mot de passe haché (longueur fixe de 60 caractères)
    mot_de_passe: Mapped[str] = mapped_column(CHAR(60), nullable=False)

    # Type d’usager (ex : "Admin" ou "Usager normal")
    type_usager: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relation avec la table des réservations
    # Un usager peut avoir plusieurs réservations associées
    reservations: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="usager")
