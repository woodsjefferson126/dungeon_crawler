import unittest
import os
import sys
from unittest.mock import patch, MagicMock
import json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dungeon_crawler import DungeonCrawler, Room, GameState

class TestMovementSystem(unittest.TestCase):
    def setUp(self):
        # Create a test rooms.json file
        self.test_rooms = {
            "entry": {
                "title": "Entry Hall",
                "description": "A crumbling stone hall",
                "exits": {"north": "corridor"},
                "dark": False,
                "items": [],
                "enemy": None,
                "npc": None
            },
            "corridor": {
                "title": "Dark Corridor",
                "description": "A narrow corridor",
                "exits": {"south": "entry"},
                "dark": True,
                "items": [],
                "enemy": None,
                "npc": None
            }
        }
        
        # Create a temporary data directory if it doesn't exist
        os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)
        
        # Write the test rooms to a file
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'rooms.json'), 'w') as f:
            json.dump(self.test_rooms, f)
        
        # Initialize the game
        self.game = DungeonCrawler()

    def tearDown(self):
        # Clean up the test file
        os.remove(os.path.join(os.path.dirname(__file__), '..', 'data', 'rooms.json'))

    def test_room_loading(self):
        """Test that rooms are loaded correctly"""
        self.assertIn('entry', self.game.game_state.rooms)
        self.assertIn('corridor', self.game.game_state.rooms)
        self.assertEqual(self.game.game_state.rooms['entry'].title, 'Entry Hall')
        self.assertEqual(self.game.game_state.rooms['corridor'].title, 'Dark Corridor')

    def test_valid_movement(self):
        """Test that valid movement works"""
        # Start in the entry room
        self.assertEqual(self.game.game_state.current_room, 'entry')
        
        # Move north (should work)
        with patch('builtins.print') as mock_print:
            self.game.handle_command('n')
            # Verify the room was updated
            self.assertEqual(self.game.game_state.steps_taken, 1)
            self.assertEqual(self.game.game_state.current_room, 'corridor')

    def test_invalid_movement(self):
        """Test that invalid movement is handled"""
        # Try to move in a direction with no exit
        with patch('builtins.print') as mock_print:
            self.game.handle_command('w')
            # Verify the error message was printed
            mock_print.assert_called_with('\x1b[31mYou can\'t go west from here!\x1b[0m')

    def test_dark_room_visibility(self):
        """Test that dark rooms are handled correctly"""
        # Move to the dark corridor
        self.game.game_state.current_room = "corridor"
        
        # Without a torch
        with patch('builtins.print') as mock_print:
            self.game.display_room()
            # Verify the dark room message was printed
            mock_print.assert_any_call('\x1b[31mIt\'s too dark to see anything!\x1b[0m')
        
        # With a torch
        self.game.game_state.inventory.append("Torch")
        with patch('builtins.print') as mock_print:
            self.game.display_room()
            # Verify the room description was printed
            mock_print.assert_any_call('\x1b[37mA narrow corridor\x1b[0m')

    def test_room_display(self):
        """Test that room information is displayed correctly"""
        with patch('builtins.print') as mock_print:
            self.game.display_room()
            
            # Debug: print all calls to print
            print("\nActual print calls:")
            for call in mock_print.call_args_list:
                args, kwargs = call
                print(f"print({args}, kwargs={kwargs})")
            
            # Verify the room title was printed
            mock_print.assert_any_call('\x1b[33m\nEntry Hall\x1b[0m')
            # Verify the room description was printed
            mock_print.assert_any_call('\x1b[37mA crumbling stone hall\x1b[0m')
            # Verify the exits section was printed
            mock_print.assert_any_call('\x1b[36m\nExits:\x1b[0m')
            # Verify the exit was printed with the correct format
            mock_print.assert_any_call('- North: Dark Corridor')

if __name__ == '__main__':
    unittest.main() 