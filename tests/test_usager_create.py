# ==============================================================
# test_usager_create.py
# Test unitaire pour vérifier la création d’un nouvel usager.
# Ce test valide que la fonction métier creerUsager fonctionne
# correctement et qu’elle retourne bien un objet DTO valide.
# ==============================================================

import unittest
import uuid

from core.db import init_db
from DTO.usagerDTO import UsagerCreateDTO
from metier.usagerMetier import creerUsager

# --------------------------------------------------------------
# Classe de test principale pour la création d’usagers
# --------------------------------------------------------------
class TestUsagerCreate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialise la base de données avant d’exécuter les tests
        init_db()

    def test_creer_usager_ok(self):
        # Création d’un DTO valide avec des données uniques
        dto = UsagerCreateDTO(
            prenom="Test",
            nom=f"Create-{uuid.uuid4()}",
            adresse="123 Rue Test",
            mobile=f"555{uuid.uuid4().hex[:6]}",
            mot_de_passe="secret",
            type_usager="client"
        )

        # Appel de la fonction métier pour créer un nouvel usager
        created = creerUsager(dto)

        # Vérifications : l’usager doit être bien créé et correspondre aux données envoyées
        self.assertIsNotNone(created.idUsager)
        self.assertEqual(created.prenom, "Test")
        self.assertTrue(created.nom.startswith("Create-"))
        self.assertEqual(created.type_usager, "client")

# Point d’entrée du test unitaire
if __name__ == "__main__":
    unittest.main()
