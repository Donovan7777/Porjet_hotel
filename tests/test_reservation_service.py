# ==============================================================
# tests/test_reservation_service.py
# Test unitaire pour valider la création d’une réservation complète
# à partir d’un ReservationDTO (comme exigé par le professeur).
# Ce test vérifie que l’id de la réservation est bien généré
# et que les liens avec la chambre et l’usager sont valides.
# ==============================================================

import datetime
from decimal import Decimal

from sqlalchemy import select

from core.db import SessionLocal, init_db
from DTO.reservationDTO import ReservationDTO
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from DTO.usagerDTO import UsagerDTO
from metier.reservationMetier import creerReservation
from modele.usager import Usager
from modele.chambre import Chambre

# --------------------------------------------------------------
# Test principal : création d’une réservation à partir d’un DTO complet
# --------------------------------------------------------------
def test_creer_reservation_depuis_dto_generates_id():
    # On s’assure que la base et les tables sont prêtes
    init_db()

    # On récupère un usager et une chambre existants dans la base
    with SessionLocal() as s:
        u = s.execute(select(Usager)).scalars().first()
        ch = s.execute(select(Chambre)).scalars().first()

        # Vérifie que les dépendances existent
        assert u is not None, "Aucun usager en base pour exécuter le test."
        assert ch is not None, "Aucune chambre en base pour exécuter le test."

        # Construction des DTOs nécessaires à la réservation
        u_dto = UsagerDTO(u)
        # ChambreDTO nécessite un TypeChambreDTO imbriqué,
        # qui est automatiquement récupéré via la relation ORM
        ch_dto = ChambreDTO(ch)

        # Fenêtre de réservation simulée sur 2 jours
        now = datetime.datetime.now()
        dto = ReservationDTO(
            idReservation=None,  # sera généré automatiquement
            dateDebut=now + datetime.timedelta(days=1),
            dateFin=now + datetime.timedelta(days=3),
            prixParJour=float(Decimal("129.99")),
            infoReservation="Test unitaire",
            chambre=ch_dto,
            usager=u_dto,
        )

        # Appel du service métier pour créer la réservation
        created = creerReservation(dto)

        # Vérifications du résultat
        assert created.idReservation is not None, "idReservation n'a pas été généré."
        assert created.usager.idUsager == u.id_usager
        assert created.chambre.idChambre == ch.id_chambre
        assert created.dateFin > created.dateDebut
