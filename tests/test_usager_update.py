# ==============================================================
# test_usager_update.py
# Test unitaire pour vérifier la mise à jour d’un usager.
# Ce test crée un usager, modifie certains de ses champs
# et vérifie que les changements sont bien enregistrés en base.
# ==============================================================

import unittest
import uuid

from core.db import init_db
from DTO.usagerDTO import UsagerCreateDTO, UsagerUpdateDTO
from metier.usagerMetier import creerUsager, modifierUsager

# --------------------------------------------------------------
# Classe principale de test pour la mise à jour d’un usager
# --------------------------------------------------------------
class TestUsagerUpdate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialise la base avant de lancer les tests
        init_db()

    def test_modifier_usager_fields(self):
        # Étape 1 : création d’un usager de départ
        created = creerUsager(
            UsagerCreateDTO(
                prenom="Old",
                nom=f"Upd-{uuid.uuid4()}",
                adresse="1 Rue Old",
                mobile=f"557{uuid.uuid4().hex[:6]}",
                mot_de_passe="oldpwd",
                type_usager="client"
            )
        )

        # Étape 2 : mise à jour de certains champs de l’usager
        updated = modifierUsager(
            id_usager=str(created.idUsager),
            data=UsagerUpdateDTO(
                prenom="New",
                adresse="99 Rue New",
                mobile=created.mobile,  # on garde le même mobile pour éviter les doublons
                type_usager="vip"
            )
        )

        # Étape 3 : vérifie que les champs ont bien été modifiés
        self.assertEqual(updated.prenom, "New")
        self.assertEqual(updated.adresse, "99 Rue New")
        self.assertEqual(updated.type_usager, "vip")

# Point d’entrée du test unitaire
if __name__ == "__main__":
    unittest.main()
