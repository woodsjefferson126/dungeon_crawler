# tests/test_dungeon_crawler.py

import unittest
from unittest.mock import patch
import sys
import os
import time

# Add the parent directory to the Python path so we can import dungeon_crawler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dungeon_crawler import DungeonCrawler, GameState

class TestDungeonCrawler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.game = DungeonCrawler()

    def test_initial_game_state(self):
        """Test that game state is initialized with correct default values"""
        state = self.game.game_state
        self.assertEqual(state.player_name, "")
        self.assertEqual(state.player_class, "")
        self.assertEqual(state.health, 100)
        self.assertEqual(state.inventory, [])
        self.assertEqual(state.current_room, "entry")
        self.assertEqual(state.flags, {})
        self.assertEqual(state.steps_taken, 0)
        self.assertEqual(state.enemies_defeated, 0)
        self.assertEqual(state.items_used, 0)
        self.assertFalse(state.debug_mode)

    def test_debug_mode_toggle(self):
        """Test that debug mode toggles correctly"""
        initial_debug_state = self.game.game_state.debug_mode
        self.game.handle_command(":d")
        self.assertNotEqual(initial_debug_state, self.game.game_state.debug_mode)
        self.game.handle_command(":d")
        self.assertEqual(initial_debug_state, self.game.game_state.debug_mode)

    def test_quit_command(self):
        """Test that quit command sets running to False"""
        self.assertTrue(self.game.running)
        self.game.handle_command("q")
        self.assertFalse(self.game.running)

    @patch('builtins.input', return_value='test input')
    def test_get_input(self, mock_input):
        """Test that get_input returns stripped lowercase input"""
        result = self.game.get_input("prompt")
        self.assertEqual(result, "test input")
        mock_input.assert_called_once()

    def test_game_state_dataclass(self):
        """Test GameState dataclass initialization"""
        state = GameState(
            player_name="Test Player",
            player_class="Warrior",
            health=100,
            inventory=["sword"],
            current_room="entry",
            flags={"visited_entry": True},
            steps_taken=1,
            enemies_defeated=0,
            items_used=0,
            start_time=time.time()
        )
        self.assertEqual(state.player_name, "Test Player")
        self.assertEqual(state.player_class, "Warrior")
        self.assertEqual(state.inventory, ["sword"])
        self.assertTrue(state.flags["visited_entry"])

if __name__ == '__main__':
    unittest.main()

