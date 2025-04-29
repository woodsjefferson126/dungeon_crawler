#!/usr/bin/env python3

import sys
import time
import random
from dataclasses import dataclass
from typing import List, Dict, Optional
import json
from colorama import init, Fore, Back, Style

# Initialize colorama
init()

# Character class definitions
CHARACTER_CLASSES = {
    "warrior": {
        "health_range": (12, 15),
        "damage_bonus": 1.2,
        "description": "A mighty warrior skilled in combat"
    },
    "wizard": {
        "health_range": (8, 12),
        "spells": ["fireball", "shield", "heal"],
        "description": "A powerful wizard with arcane knowledge"
    },
    "scoundrel": {
        "health_range": (1, 12),
        "escape_bonus": 1.2,
        "lockpick_chance": 0.5,
        "description": "A cunning rogue with quick reflexes"
    }
}

# D&D-style name components
NAME_COMPONENTS = {
    "prefix": ["Ael", "Bryn", "Cor", "Dain", "Eir", "Fen", "Gor", "Hael", "Ior", "Jor"],
    "suffix": ["wyn", "ric", "thas", "mir", "lan", "dor", "ven", "thor", "gar", "wyn"]
}

@dataclass
class GameState:
    """Tracks the current state of the game"""
    player_name: str
    player_class: str
    health: int
    inventory: List[str]
    current_room: str
    flags: Dict[str, bool]
    steps_taken: int
    enemies_defeated: int
    items_used: int
    start_time: float
    debug_mode: bool = False

class DungeonCrawler:
    def __init__(self):
        # Initialize with default values
        self.game_state = GameState(
            player_name="",
            player_class="",
            health=100,
            inventory=[],
            current_room="entry",
            flags={},
            steps_taken=0,
            enemies_defeated=0,
            items_used=0,
            start_time=time.time(),
            debug_mode=False
        )
        self.running: bool = True

    def display_title(self):
        """Display the game's title screen with ASCII art"""
        print(Fore.YELLOW + Style.BRIGHT + """
╔══════════════════════════════════════════╗
║     Depths of the Forgotten (CLI)        ║
║            - Version 1.0 -               ║
╚══════════════════════════════════════════╝
""" + Style.RESET_ALL)

    def generate_random_name(self) -> str:
        """Generate a random D&D-style name"""
        prefix = random.choice(NAME_COMPONENTS["prefix"])
        suffix = random.choice(NAME_COMPONENTS["suffix"])
        return f"{prefix}{suffix}"

    def select_character_class(self) -> str:
        """Handle character class selection with autocomplete"""
        while True:
            print(Fore.CYAN + "\nChoose your character class:")
            for class_name, details in CHARACTER_CLASSES.items():
                print(f"- {class_name.capitalize()}: {details['description']}")
            
            choice = self.get_input("\nEnter your choice (type first few letters to autocomplete): ").lower()
            
            # Find matching classes based on input
            matches = [c for c in CHARACTER_CLASSES.keys() if c.startswith(choice)]
            
            if len(matches) == 1:
                return matches[0]
            elif len(matches) > 1:
                print(Fore.YELLOW + "\nMultiple matches found:")
                for match in matches:
                    print(f"- {match.capitalize()}")
                print(Fore.RED + "Please be more specific." + Style.RESET_ALL)
            elif choice in CHARACTER_CLASSES:
                return choice
            else:
                print(Fore.RED + "Invalid choice. Please select a valid class." + Style.RESET_ALL)

    def select_player_name(self) -> str:
        """Handle player name selection"""
        random_name = self.generate_random_name()
        print(Fore.CYAN + f"\nSuggested name: {random_name}")
        while True:
            name = self.get_input("Enter your name (or press Enter to use the suggested name): ").strip()
            if not name:
                return random_name
            if name.isalnum() and len(name) <= 20:
                return name
            print(Fore.RED + "Invalid name. Use only letters and numbers, max 20 characters." + Style.RESET_ALL)

    def initialize_player(self):
        """Initialize player with selected class and name"""
        self.game_state.player_class = self.select_character_class()
        self.game_state.player_name = self.select_player_name()
        
        # Set initial health based on class
        health_range = CHARACTER_CLASSES[self.game_state.player_class]["health_range"]
        self.game_state.health = random.randint(*health_range)
        
        # Set starting inventory
        self.game_state.inventory = ["Torch", "Rusty Dagger"]
        
        # Display welcome message
        print(Fore.GREEN + f"\nWelcome, {self.game_state.player_name} the {self.game_state.player_class.capitalize()}!")
        print(f"You start with {self.game_state.health} health and:")
        for item in self.game_state.inventory:
            print(f"- {item}")
        print(Style.RESET_ALL)

    def get_input(self, prompt: str) -> str:
        """Get input from the user with proper formatting"""
        print(Fore.CYAN + prompt + Style.RESET_ALL, end='')
        return input().strip().lower()

    def display_debug_info(self):
        """Display debug information"""
        print(Fore.MAGENTA + "\n=== DEBUG INFO ===")
        print(f"Name: {self.game_state.player_name}")
        print(f"Class: {self.game_state.player_class}")
        print(f"Room: {self.game_state.current_room}")
        print(f"Steps: {self.game_state.steps_taken}")
        print(f"Health: {self.game_state.health}")
        
        # Show inventory with counts
        print("Inventory:")
        if not self.game_state.inventory:
            print("  Empty")
        else:
            # Count items
            item_counts = {}
            for item in self.game_state.inventory:
                item_counts[item] = item_counts.get(item, 0) + 1
            # Display items with counts
            for item, count in item_counts.items():
                print(f"  {item} x{count}")
        
        print(f"Enemies Defeated: {self.game_state.enemies_defeated}")
        print(f"Items Used: {self.game_state.items_used}")
        print(f"Time Elapsed: {int(time.time() - self.game_state.start_time)}s")
        print("Flags:", "None" if not self.game_state.flags else "")
        for flag, value in self.game_state.flags.items():
            print(f"  {flag}: {value}")
        print("=================" + Style.RESET_ALL)

    def handle_command(self, command: str) -> None:
        """Process user commands"""
        if command == 'q':
            self.running = False
        elif command == ':d':
            self.game_state.debug_mode = not self.game_state.debug_mode
            if self.game_state.debug_mode:
                self.display_debug_info()
            print(f"Debug mode: {'on' if self.game_state.debug_mode else 'off'}")
        # More commands will be added here

    def main_loop(self):
        """Main game loop"""
        while self.running:
            if self.game_state.debug_mode:
                self.display_debug_info()
            command = self.get_input("\nEnter command (q to quit): ")
            self.handle_command(command)

    def run(self):
        """Start the game"""
        try:
            self.display_title()
            print(Fore.WHITE + "Welcome to the dungeon!" + Style.RESET_ALL)
            self.initialize_player()
            self.main_loop()
        except KeyboardInterrupt:
            print("\nGame terminated by user")
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
        finally:
            print("\nThanks for playing!")

if __name__ == "__main__":
    game = DungeonCrawler()
    game.run()
