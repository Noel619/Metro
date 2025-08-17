import unittest
import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from risk.game_setup import setup_new_game
from risk.models import Map, Player

class TestGameSetup(unittest.TestCase):

    def setUp(self):
        """Set up a new game for each test."""
        self.map, self.players = setup_new_game()

    def test_setup_return_types(self):
        """Test that setup_new_game returns objects of the correct type."""
        self.assertIsInstance(self.map, Map)
        self.assertIsInstance(self.players, list)
        self.assertTrue(all(isinstance(p, Player) for p in self.players))

    def test_player_and_territory_counts(self):
        """Test the number of players and territories created."""
        self.assertEqual(len(self.players), 2)
        self.assertEqual(len(self.map.territories), 4)

    def test_territory_ownership_and_armies(self):
        """Test that territories are assigned to the correct owners with correct armies."""
        player1 = self.players[0]
        player2 = self.players[1]

        westeros = self.map.get_territory("Westeros")
        self.assertEqual(westeros.owner, player1)
        self.assertEqual(westeros.armies, 5)

        essos = self.map.get_territory("Essos")
        self.assertEqual(essos.owner, player2)
        self.assertEqual(essos.armies, 5)

        sothoryos = self.map.get_territory("Sothoryos")
        self.assertEqual(sothoryos.owner, player1)
        self.assertEqual(sothoryos.armies, 3)

        ulthos = self.map.get_territory("Ulthos")
        self.assertEqual(ulthos.owner, player2)
        self.assertEqual(ulthos.armies, 3)

        self.assertEqual(len(player1.territories), 2)
        self.assertEqual(len(player2.territories), 2)

    def test_map_adjacencies(self):
        """Test the connections between territories."""
        adj = self.map.adjacencies

        self.assertIn("Essos", adj["Westeros"])
        self.assertIn("Sothoryos", adj["Westeros"])

        self.assertIn("Westeros", adj["Essos"])
        self.assertIn("Sothoryos", adj["Essos"])
        self.assertIn("Ulthos", adj["Essos"])

        self.assertIn("Westeros", adj["Sothoryos"])
        self.assertIn("Essos", adj["Sothoryos"])

        self.assertIn("Essos", adj["Ulthos"])
        self.assertNotIn("Westeros", adj["Ulthos"])

if __name__ == '__main__':
    unittest.main()
