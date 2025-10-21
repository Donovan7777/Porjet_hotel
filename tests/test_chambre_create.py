# ==============================================================
# tests/test_chambre_create.py
# Vérifie la création d’une Chambre rattachée à un TypeChambre.
# ==============================================================

import unittest
import uuid
from core.db import init_db, SessionLocal
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from metier.chambreMetier import creerTypeChambre, creerChambre
from modele.chambre import Chambre
from sqlalchemy import select

class TestChambreCreate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_creer_chambre_ok(self):
        # Crée un type de chambre unique
        type_name = f"ch-{uuid.uuid4().hex[:8]}"
        type_dto = creerTypeChambre(
            TypeChambreCreateDTO(
                nom_type=type_name,
                prix_plancher=99.9,
                prix_plafond=None,
                description_chambre="Type pour test chambre"
            )
        )

        # Numéro unique pour éviter les doublons
        num_unique = int(str(uuid.uuid4().int)[:3])  # ex: 482 ou 912

        # Crée la chambre
        ch_dto = creerChambre(
            ChambreCreateDTO(
                numero_chambre=num_unique,
                disponible_reservation=True,
                autre_informations="Chambre test",
                nom_type=type_dto.nom_type
            )
        )

        self.assertIsNotNone(ch_dto.idChambre)
        self.assertEqual(ch_dto.numero_chambre, num_unique)
        self.assertTrue(ch_dto.disponible_reservation)

        # Vérifie présence dans la BD (en filtrant par ID, plus sûr)
        with SessionLocal() as s:
            found = s.get(Chambre, ch_dto.idChambre)
            self.assertIsNotNone(found)
            self.assertEqual(found.numero_chambre, num_unique)

if __name__ == "__main__":
    unittest.main()
