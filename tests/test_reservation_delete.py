# ==============================================================
# tests/test_reservation_delete.py
# Vérifie la suppression d’une réservation existante.
# ==============================================================

import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import select
from core.db import init_db, SessionLocal
from DTO.reservationDTO import ReservationDTO
from DTO.usagerDTO import UsagerDTO
from DTO.chambreDTO import ChambreDTO
from metier.reservationMetier import creerReservation, supprimerReservation
from modele.reservation import Reservation
from modele.usager import Usager
from modele.chambre import Chambre

class TestReservationDelete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_supprimer_reservation_ok(self):
        with SessionLocal() as s:
            u = s.execute(select(Usager)).scalars().first()
            ch = s.execute(select(Chambre)).scalars().first()
            if not u or not ch:
                self.skipTest("Need at least one Usager and one Chambre in DB.")

            # Prépare DTO complet
            dto = ReservationDTO(
                idReservation=None,
                dateDebut=datetime.now(),
                dateFin=datetime.now() + timedelta(days=1),
                prixParJour=float(Decimal("123.45")),
                infoReservation="Reservation à supprimer",
                chambre=ChambreDTO(ch),
                usager=UsagerDTO(u),
            )

            created = creerReservation(dto)
            ok = supprimerReservation(str(created.idReservation))
            self.assertTrue(ok)

            # Vérifie que la réservation n'existe plus
            gone = s.get(Reservation, str(created.idReservation))
            self.assertIsNone(gone)

if __name__ == "__main__":
    unittest.main()
