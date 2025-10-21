# ==============================================================
# modele/reservation.py
# Modèle SQLAlchemy qui représente la table "reservation" dans la BD.
# Chaque réservation relie une chambre et un usager avec des dates
# précises, un prix par jour, et des informations optionnelles.
# ==============================================================

from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from .base import Base

# Import uniquement pour la vérification des types (évite les boucles d’import)
if TYPE_CHECKING:
    from .usager import Usager
    from .chambre import Chambre

# --------------------------------------------------------------
# Classe principale Reservation
# Chaque instance représente une ligne de la table "reservation"
# --------------------------------------------------------------
class Reservation(Base):
    __tablename__ = "reservation"

    # Identifiant unique de la réservation (UUID auto-généré)
    id_reservation: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    # Date et heure du début de la réservation
    date_debut_reservation: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Date et heure de fin de la réservation
    date_fin_reservation: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Prix facturé par jour (de type monétaire)
    prix_jour: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Informations additionnelles facultatives (commentaire, demande spéciale, etc.)
    info_reservation: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Clé étrangère vers l’usager ayant fait la réservation
    fk_id_usager: Mapped[UUID] = mapped_column(ForeignKey("usager.id_usager"), nullable=False)

    # Clé étrangère vers la chambre réservée
    fk_id_chambre: Mapped[UUID] = mapped_column(ForeignKey("chambre.id_chambre"), nullable=False)

    # Relation vers l’usager (un usager peut avoir plusieurs réservations)
    usager: Mapped["Usager"] = relationship("Usager", back_populates="reservations")

    # Relation vers la chambre (une chambre peut avoir plusieurs réservations)
    chambre: Mapped["Chambre"] = relationship("Chambre", back_populates="reservations")
