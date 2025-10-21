# ==============================================================
# test_type_chambre_delete.py
# Test unitaire pour vérifier la suppression d’un type de chambre.
# Ce test crée un type de chambre temporaire, s’assure qu’il existe,
# le supprime, puis vérifie qu’il n’est plus présent dans la base.
# ==============================================================

import unittest
import uuid
from sqlalchemy import select

from core.db import init_db, SessionLocal
from DTO.chambreDTO import TypeChambreCreateDTO
from metier.chambreMetier import creerTypeChambre, supprimerTypeChambre
from modele.type_chambre import TypeChambre

# --------------------------------------------------------------
# Classe principale de test
# --------------------------------------------------------------
class TestTypeChambreDelete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialise le schéma de base avant les tests
        init_db()

    def test_supprimer_type_chambre_ok_when_unreferenced(self):
        # Génère un nom unique pour éviter les doublons en base
        unique_name = f"test-del-tc-{uuid.uuid4()}"

        # Crée un nouveau type de chambre temporaire
        _ = creerTypeChambre(
            TypeChambreCreateDTO(
                nom_type=unique_name,
                prix_plancher=80.0,
                prix_plafond=None,
                description_chambre="to delete"
            )
        )

        # Vérifie que le type de chambre a bien été créé
        with SessionLocal() as s:
            ent = s.execute(
                select(TypeChambre).where(TypeChambre.nom_type == unique_name)
            ).scalar_one_or_none()
            self.assertIsNotNone(ent)
            id_type = str(ent.id_type_chambre)

        # Supprime le type de chambre via la logique métier
        ok = supprimerTypeChambre(id_type)
        self.assertTrue(ok)

        # Vérifie qu’il a bien été retiré de la base
        with SessionLocal() as s:
            again = s.get(TypeChambre, id_type)
            self.assertIsNone(again)

# Point d’entrée du test unitaire
if __name__ == "__main__":
    unittest.main()
