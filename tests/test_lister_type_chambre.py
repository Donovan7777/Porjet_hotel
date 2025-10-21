# ==============================================================
# tests/test_lister_type_chambre.py
# Vérifie que la liste des types de chambres peut être récupérée.
# ==============================================================

import unittest
from core.db import init_db
from metier.chambreMetier import listerTypesChambre

class TestListerTypeChambre(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_lister_type_chambre_retourne_liste(self):
        types = listerTypesChambre()
        self.assertIsInstance(types, list)
        if types:
            self.assertTrue(hasattr(types[0], "nom_type"))

if __name__ == "__main__":
    unittest.main()
