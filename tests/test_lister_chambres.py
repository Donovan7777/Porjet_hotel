# ==============================================================
# tests/test_lister_chambres.py
# Vérifie que la liste des chambres peut être récupérée.
# ==============================================================

import unittest
from core.db import init_db
from metier.chambreMetier import listerChambres

class TestListerChambres(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_lister_chambres_retourne_liste(self):
        chambres = listerChambres()
        self.assertIsInstance(chambres, list)
        if chambres:
            self.assertTrue(hasattr(chambres[0], "numero_chambre"))

if __name__ == "__main__":
    unittest.main()
