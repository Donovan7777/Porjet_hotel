# ==============================================================
# tests/test_chambre.py
# Série de tests unitaires simples ("smoke tests") pour vérifier
# que les modèles ORM (SQLAlchemy) fonctionnent bien ensemble.
# On vérifie ici la structure, les relations et quelques requêtes
# de base sur les tables Chambre, TypeChambre, Usager et Réservation.
# ==============================================================

import unittest
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.db import SessionLocal
from modele.chambre import Chambre
from modele.type_chambre import TypeChambre
from modele.reservation import Reservation
from modele.usager import Usager

# --------------------------------------------------------------
# Classe principale de tests ORM
# Ces tests ne vérifient pas la logique métier, mais s’assurent
# que les modèles et leurs relations sont bien configurés.
# --------------------------------------------------------------
class TestModels(unittest.TestCase):

    def test_orm_can_query_any_chambre_and_follow_relationship(self):
        """Test de base : lire une chambre et accéder à son type via la relation."""
        with SessionLocal() as session:  # ouverture de la session SQLAlchemy
            ch = session.execute(select(Chambre)).scalars().first()
            # Vérifie qu’il y a au moins une chambre dans la table
            self.assertIsNotNone(ch, "No rows in table 'chambre'. Insert sample data first.")

            # Vérifie que la relation avec TypeChambre est bien fonctionnelle
            self.assertIsNotNone(ch.type_chambre, "Relationship 'type_chambre' is not mapped.")
            self.assertIsInstance(ch.type_chambre, TypeChambre)

            # Accès à un champ pour confirmer que la relation est bien chargée
            _ = ch.type_chambre.nom_type  # ne devrait pas lever d’erreur

            # Vérifie que la relation inverse (back_populates) existe bien
            self.assertTrue(hasattr(ch.type_chambre, "chambres"))

    def test_join_query_reservation_usager_chambre(self):
        """Test simple : jointure entre Réservation, Usager et Chambre."""
        with SessionLocal() as session:
            # Requête avec double jointure pour vérifier la cohérence du mapping ORM
            r = session.execute(
                select(Reservation).join(Reservation.usager).join(Reservation.chambre)
            ).scalars().first()

            # Même si aucune réservation n’existe, l’objectif est que la requête fonctionne
            # sans lever d’erreur SQL ou de mapping.
            self.assertTrue(True, "Join ran without raising exceptions")

    def test_specific_room_example_if_exists(self):
        """
        Test optionnel : vérifie la présence d’une chambre spécifique (#243) si elle existe.
        Si la chambre n’est pas dans la base, le test est ignoré.
        """
        with SessionLocal() as session:
            ch = session.execute(
                select(Chambre).where(Chambre.numero_chambre == 243)
            ).scalars().first()

            # Si la chambre n’existe pas, on saute le test (ne compte pas comme échec)
            if ch is None:
                self.skipTest("Room 243 not present in DB, skipping example check.")
            else:
                # Vérifie que la chambre 243 est bien liée à un type "king"
                self.assertEqual(ch.numero_chambre, 243)
                self.assertIsNotNone(ch.type_chambre)
                self.assertEqual(ch.type_chambre.nom_type.lower(), "king")

# Point d’entrée pour exécuter le test manuellement
if __name__ == "__main__":
    unittest.main(verbosity=2)
