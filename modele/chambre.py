# ==============================================================
# modele/chambre.py
# Modèle SQLAlchemy représentant la table "chambre" dans la BD.
# Chaque chambre appartient à un type de chambre et peut avoir
# plusieurs réservations associées.
# ==============================================================

from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, String, SmallInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from .base import Base

# Import utilisé seulement pour les vérifications de type
# (pas exécuté à l’exécution, évite les imports circulaires)
if TYPE_CHECKING:
    from .type_chambre import TypeChambre
    from .reservation import Reservation

# --------------------------------------------------------------
# Classe principale Chambre
# Chaque instance correspond à une ligne de la table "chambre"
# --------------------------------------------------------------
class Chambre(Base):
    __tablename__ = "chambre"

    # Identifiant unique (UUID) généré automatiquement
    id_chambre: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    # Numéro de la chambre (ex: 101, 202, etc.)
    numero_chambre: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    # Indique si la chambre est disponible pour une réservation
    disponible_reservation: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Autres infos facultatives (ex: vue sur la mer, étage, etc.)
    autre_informations: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Clé étrangère vers la table "type_chambre"
    fk_type_chambre: Mapped[UUID] = mapped_column(ForeignKey("type_chambre.id_type_chambre"))

    # Relation avec la classe TypeChambre (plusieurs chambres par type)
    type_chambre: Mapped["TypeChambre"] = relationship("TypeChambre", back_populates="chambres")

    # Relation inverse avec Reservation (une chambre peut avoir plusieurs réservations)
    reservations: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="chambre")
