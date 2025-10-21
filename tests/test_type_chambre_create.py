# ==============================================================
# tests/test_type_chambre_create.py
# Vérifie la création d’un TypeChambre dans la base de données.
# ==============================================================

import unittest
import uuid
from core.db import init_db, SessionLocal
from DTO.chambreDTO import TypeChambreCreateDTO
from metier.chambreMetier import creerTypeChambre
from modele.type_chambre import TypeChambre
from sqlalchemy import select

class TestTypeChambreCreate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_creer_type_chambre_ok(self):
        unique_name = f"type-{uuid.uuid4().hex[:8]}"
        dto = TypeChambreCreateDTO(
            nom_type=unique_name,
            prix_plancher=100.0,
            prix_plafond="200",
            description_chambre="Type créé par test unitaire"
        )

        created = creerTypeChambre(dto)

        # on ne vérifie pas un ID car le DTO n’en contient pas
        self.assertIsNotNone(created.nom_type)
        self.assertEqual(created.nom_type, unique_name)
        self.assertEqual(float(created.prix_plancher), 100.0)

        # Vérifie que la donnée existe bien dans la BD
        with SessionLocal() as s:
            found = s.execute(select(TypeChambre).where(TypeChambre.nom_type == unique_name)).scalar_one_or_none()
            self.assertIsNotNone(found)

if __name__ == "__main__":
    unittest.main()
