# ==============================================================
# tests/test_type_chambre_search.py
# Vérifie la recherche de TypeChambre selon différents critères.
# ==============================================================


import unittest
import uuid


from core.db import init_db
from DTO.chambreDTO import TypeChambreCreateDTO, TypeChambreSearchDTO
from metier.chambreMetier import creerTypeChambre, rechercherTypeChambre


class TestTypeChambreSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialise le schéma (tables) avant les tests
        init_db()

    def test_rechercher_type_chambre_par_nom(self):
        # Crée un type de chambre unique
        unique = f"tc-search-{uuid.uuid4().hex[:6]}"
        t = creerTypeChambre(
            TypeChambreCreateDTO(
                nom_type=unique,
                prix_plancher=80.0,
                prix_plafond=None,
                description_chambre="search test",
            )
        )

        # Recherche par nom
        crit = TypeChambreSearchDTO(nom_type=unique)
        results = rechercherTypeChambre(crit)

        self.assertIsInstance(results, list)
        self.assertTrue(any(tc.nom_type == unique for tc in results))


if __name__ == "__main__":
    unittest.main()
