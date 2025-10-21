# ==============================================================
# test_usager_delete.py
# Test unitaire pour vérifier la suppression d’un usager.
# Ce test crée un usager temporaire, le supprime ensuite,
# puis s’assure qu’il n’existe plus dans la base de données.
# ==============================================================

import unittest
import uuid
from sqlalchemy import select

from core.db import init_db, SessionLocal
from DTO.usagerDTO import UsagerCreateDTO
from metier.usagerMetier import creerUsager, supprimerUsager
from modele.usager import Usager

# --------------------------------------------------------------
# Classe principale de test pour la suppression d’un usager
# --------------------------------------------------------------
class TestUsagerDelete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialise la base de données avant les tests
        init_db()

    def test_supprimer_usager_ok(self):
        # Étape 1 : création d’un usager temporaire pour le test
        created = creerUsager(
            UsagerCreateDTO(
                prenom="Del",
                nom=f"User-{uuid.uuid4()}",
                adresse="456 Rue X",
                mobile=f"556{uuid.uuid4().hex[:6]}",
                mot_de_passe="pwd",
                type_usager="client"
            )
        )

        # Étape 2 : suppression de cet usager via la logique métier
        ok = supprimerUsager(str(created.idUsager))
        self.assertTrue(ok)

        # Étape 3 : vérification dans la base que l’usager n’existe plus
        with SessionLocal() as s:
            ent = s.get(Usager, str(created.idUsager))
            self.assertIsNone(ent)

# Point d’entrée du test unitaire
if __name__ == "__main__":
    unittest.main()
