# ==============================================================
# tests/test_reservation_updates.py
# Tests unitaires pour vérifier la mise à jour et la suppression
# des réservations. Compatible avec la version officielle du prof
# (creerReservation(dto: ReservationDTO))
# ==============================================================

import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.db import SessionLocal
from DTO.reservationDTO import ReservationDTO, ReservationUpdateDTO
from DTO.usagerDTO import UsagerDTO
from DTO.chambreDTO import ChambreDTO
from metier.reservationMetier import (
    creerReservation,
    modifierReservation,
    supprimerReservation,
)
from modele.chambre import Chambre
from modele.usager import Usager
from modele.reservation import Reservation


# --------------------------------------------------------------
# Classe de test principale
# --------------------------------------------------------------
class TestReservationUpdateDelete(unittest.TestCase):
    # Petite méthode utilitaire pour aller chercher le premier usager et la première chambre
    def _first_usager_and_chambre(self, s: Session):
        u = s.execute(select(Usager)).scalars().first()
        ch = s.execute(select(Chambre)).scalars().first()
        return u, ch

    # ----------------------------------------------------------
    # Test 1 : mise à jour d’une réservation existante
    # ----------------------------------------------------------
    def test_modifier_reservation(self):
        with SessionLocal() as s:
            u, ch = self._first_usager_and_chambre(s)
            if not u or not ch:
                self.skipTest("Need at least one Usager and one Chambre in DB.")

            # DTOs imbriqués pour respecter la signature officielle
            u_dto = UsagerDTO(u)
            ch_dto = ChambreDTO(ch)

            # Création d’une réservation initiale
            start = datetime(2025, 10, 1, 15, 0, 0)
            end = datetime(2025, 10, 2, 11, 0, 0)
            dto = ReservationDTO(
                idReservation=None,
                dateDebut=start,
                dateFin=end,
                prixParJour=float(Decimal("111.11")),
                infoReservation="before update",
                chambre=ch_dto,
                usager=u_dto,
            )

            created = creerReservation(dto)

            # Prépare une mise à jour : nouvelle date de fin, nouveau prix et nouvelle note
            new_end = end + timedelta(days=1)
            upd = ReservationUpdateDTO(
                dateFin=new_end,
                prixParJour=222.22,
                infoReservation="after update",
            )

            # Exécute la modification via le service métier
            updated = modifierReservation(str(created.idReservation), upd)

            # Vérifie que les champs ont bien été mis à jour
            self.assertEqual(updated.prixParJour, 222.22)
            self.assertEqual(updated.infoReservation, "after update")
            self.assertEqual(updated.dateFin, new_end)

            # Nettoyage pour garder la BD propre après le test
            ok = supprimerReservation(str(created.idReservation))
            self.assertTrue(ok)

    # ----------------------------------------------------------
    # Test 2 : suppression d’une réservation
    # ----------------------------------------------------------
    def test_supprimer_reservation(self):
        with SessionLocal() as s:
            u, ch = self._first_usager_and_chambre(s)
            if not u or not ch:
                self.skipTest("Need at least one Usager and one Chambre in DB.")

            # DTOs imbriqués pour respecter la signature officielle
            u_dto = UsagerDTO(u)
            ch_dto = ChambreDTO(ch)

            # Création d’une réservation temporaire pour test
            start = datetime(2025, 11, 1, 15, 0, 0)
            end = datetime(2025, 11, 2, 11, 0, 0)
            dto = ReservationDTO(
                idReservation=None,
                dateDebut=start,
                dateFin=end,
                prixParJour=float(Decimal("150.00")),
                infoReservation="to delete",
                chambre=ch_dto,
                usager=u_dto,
            )

            created = creerReservation(dto)

            # Suppression de la réservation via la logique métier
            ok = supprimerReservation(str(created.idReservation))
            self.assertTrue(ok)

            # Vérifie que la réservation n’existe plus dans la base
            gone = s.get(Reservation, str(created.idReservation))
            self.assertIsNone(gone)


# Point d’entrée pour exécuter le test manuellement
if __name__ == "__main__":
    unittest.main()
