# ==============================================================
# tests/test_usager_search.py
# Vérifie la recherche d’usagers selon différents critères.
# ==============================================================


import unittest
import uuid


from core.db import init_db
from DTO.usagerDTO import UsagerCreateDTO, UsagerSearchDTO
from metier.usagerMetier import creerUsager, rechercherUsager


class TestUsagerSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialise le schéma (tables) avant les tests
        init_db()

    def test_rechercher_usager_par_nom_prenom(self):
        # Crée un usager unique pour le test
        prenom = "Search"
        nom = f"User-{uuid.uuid4().hex[:6]}"
        created = creerUsager(
            UsagerCreateDTO(
                prenom=prenom,
                nom=nom,
                adresse="999 Rue Test",
                mobile=f"550{uuid.uuid4().hex[:6]}",
                mot_de_passe="pwd",
                type_usager="client",
            )
        )

        # Recherche par nom + prénom
        crit = UsagerSearchDTO(prenom=prenom, nom=nom)
        results = rechercherUsager(crit)

        self.assertIsInstance(results, list)
        self.assertTrue(any(u.idUsager == created.idUsager for u in results))


if __name__ == "__main__":
    unittest.main()
