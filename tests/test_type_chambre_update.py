# ==============================================================
# test_type_chambre_update.py
# Test unitaire pour vérifier la mise à jour d’un type de chambre.
# Le test crée un type de chambre, le modifie entièrement
# (nom, prix, description) et vérifie que les changements sont bien appliqués.
# ==============================================================

import unittest
import uuid
from sqlalchemy import select

from core.db import init_db, SessionLocal
from DTO.chambreDTO import TypeChambreCreateDTO, TypeChambreUpdateDTO
from metier.chambreMetier import creerTypeChambre, modifierTypeChambre
from modele.type_chambre import TypeChambre

# --------------------------------------------------------------
# Classe principale de test pour la mise à jour d’un type de chambre
# --------------------------------------------------------------
class TestTypeChambreUpdate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialise la base de données avant de lancer les tests
        init_db()

    def test_modifier_type_chambre_fields(self):
        # Crée un nom unique pour éviter tout conflit dans la BD
        base = f"tc-{uuid.uuid4().hex[:8]}"

        # Étape 1 : création d’un type de chambre de base
        _ = creerTypeChambre(
            TypeChambreCreateDTO(
                nom_type=base,
                prix_plancher=70.0,
                prix_plafond="200",
                description_chambre="desc old"
            )
        )

        # Étape 2 : récupère l’enregistrement fraîchement créé
        with SessionLocal() as s:
            ent = s.execute(
                select(TypeChambre).where(TypeChambre.nom_type == base)
            ).scalar_one_or_none()
            self.assertIsNotNone(ent)
            id_type = str(ent.id_type_chambre)

        # Étape 3 : exécute la mise à jour complète du type
        updated = modifierTypeChambre(
            id_type_chambre=id_type,
            data=TypeChambreUpdateDTO(
                nom_type=f"{base}-n",
                prix_plancher=99.5,
                prix_plafond="300",
                description_chambre="desc new"
            )
        )

        # Étape 4 : vérifie que tous les champs ont bien été mis à jour
        self.assertEqual(updated.nom_type, f"{base}-n")
        self.assertEqual(float(updated.prix_plancher), 99.5)
        # Le champ prix_plafond peut être rempli d’espaces à cause du type CHAR/NCHAR,
        # donc on enlève les espaces avant la comparaison
        self.assertEqual(updated.prix_plafond.strip(), "300")
        self.assertEqual(updated.description_chambre, "desc new")

# Point d’entrée du test unitaire
if __name__ == "__main__":
    unittest.main()
