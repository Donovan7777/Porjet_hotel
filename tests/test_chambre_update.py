# ==============================================================
# test_modifier_chambre.py
# Test unitaire pour vérifier la mise à jour complète d’une chambre.
# Ce test s’assure que tous les champs peuvent être modifiés
# (numéro, disponibilité, infos, type de chambre, etc.)
# ==============================================================

import unittest
import uuid

from core.db import init_db
from DTO.chambreDTO import (
    TypeChambreCreateDTO,
    ChambreCreateDTO,
    ChambreUpdateDTO,
)
from metier.chambreMetier import (
    creerTypeChambre,
    creerChambre,
    modifierChambre,
)

# --------------------------------------------------------------
# Classe de test principale pour la modification de chambre
# --------------------------------------------------------------
class TestChambreUpdate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialise la base de données avant les tests
        init_db()

    def test_modifier_chambre_all_fields_and_type(self):
        # On utilise des noms uniques courts pour éviter les doublons
        # (max 50 caractères comme défini dans le DTO)
        typeA_name = f"tA-{uuid.uuid4().hex[:8]}"
        typeB_name = f"tB-{uuid.uuid4().hex[:8]}"

        # Création du premier type de chambre (type A)
        typeA = creerTypeChambre(
            TypeChambreCreateDTO(
                nom_type=typeA_name,
                prix_plancher=90.0,
                prix_plafond=None,
                description_chambre="A"
            )
        )

        # Création du deuxième type de chambre (type B)
        typeB = creerTypeChambre(
            TypeChambreCreateDTO(
                nom_type=typeB_name,
                prix_plancher=120.0,
                prix_plafond="250",
                description_chambre="B"
            )
        )

        # Création d’une chambre associée au type A
        ch = creerChambre(
            ChambreCreateDTO(
                numero_chambre=991,
                disponible_reservation=False,
                autre_informations="before",
                nom_type=typeA.nom_type
            )
        )

        # Mise à jour complète : changement du numéro, de la dispo,
        # de l’info, et passage au type B
        updated = modifierChambre(
            id_chambre=str(ch.idChambre),
            data=ChambreUpdateDTO(
                numero_chambre=555,
                disponible_reservation=True,
                autre_informations="after",
                nom_type=typeB.nom_type
            )
        )

        # Vérifie que tous les champs ont bien été modifiés
        self.assertEqual(updated.numero_chambre, 555)
        self.assertTrue(updated.disponible_reservation)
        self.assertEqual(updated.autre_informations, "after")
        self.assertEqual(updated.type_chambre.nom_type, typeB.nom_type)

# Point d’entrée du test
if __name__ == "__main__":
    unittest.main()
