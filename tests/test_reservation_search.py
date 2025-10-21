# ==============================================================
# tests/test_reservation_search.py
# Vérifie la recherche de réservations selon différents critères.
# ==============================================================

import unittest
from core.db import init_db, SessionLocal
from DTO.reservationDTO import CriteresRechercheDTO
from metier.reservationMetier import rechercherReservation
from modele.reservation import Reservation

class TestReservationSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_rechercher_reservation_sans_criteres(self):
        # Quand aucun critère n’est donné, on doit recevoir une liste (peut-être vide)
        criteres = CriteresRechercheDTO()
        results = rechercherReservation(criteres)
        self.assertIsInstance(results, list)

    def test_rechercher_reservation_par_nom(self):
        with SessionLocal() as s:
            row = s.query(Reservation).first()
            if not row or not row.usager:
                self.skipTest("Aucune réservation avec usager pour tester la recherche par nom.")

            criteres = CriteresRechercheDTO(nom=row.usager.nom, prenom=row.usager.prenom)
            results = rechercherReservation(criteres)
            self.assertTrue(isinstance(results, list))
            if results:
                self.assertEqual(results[0].usager.nom, row.usager.nom)

if __name__ == "__main__":
    unittest.main()
