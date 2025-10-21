# ==============================================================
# test_supprimer_chambre.py
# Test unitaire pour valider la suppression d’une chambre.
# Le test crée un type de chambre, crée ensuite une chambre liée,
# puis la supprime et vérifie que la suppression est bien effective.
# ==============================================================

import unittest
import uuid
from sqlalchemy import select

from core.db import init_db, SessionLocal
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, supprimerChambre
from modele.chambre import Chambre

# --------------------------------------------------------------
# Classe de test principale
# Chaque méthode "test_*" est exécutée automatiquement par unittest
# --------------------------------------------------------------
class TestChambreDelete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialise la base de données avant d’exécuter les tests
        # (par ex. création des tables, connexion, etc.)
        init_db()

    def test_supprimer_chambre_ok(self):
        # Étape 1 : créer un type de chambre temporaire
        type_name = f"test-del-type-{uuid.uuid4()}"
        tc_dto = creerTypeChambre(
            TypeChambreCreateDTO(
                nom_type=type_name,
                prix_plancher=100.0,
                prix_plafond=None,
                description_chambre="type for delete chambre"
            )
        )

        # Étape 2 : créer une chambre associée à ce type
        ch_dto = creerChambre(
            ChambreCreateDTO(
                numero_chambre=990,
                disponible_reservation=True,
                autre_informations="tmp chambre to delete",
                nom_type=tc_dto.nom_type
            )
        )

        # Étape 3 : supprimer la chambre
        ok = supprimerChambre(str(ch_dto.idChambre))
        # On s’attend à ce que la suppression retourne True
        self.assertTrue(ok)

        # Étape 4 : vérifier dans la base que la chambre n’existe plus
        with SessionLocal() as s:
            found = s.execute(
                select(Chambre).where(Chambre.id_chambre == ch_dto.idChambre)
            ).scalar_one_or_none()
            # Si la suppression a bien fonctionné, "found" doit être None
            self.assertIsNone(found)

# Point d’entrée du test
if __name__ == "__main__":
    unittest.main()
