#!/usr/bin/env python3

import sys
import time
import random
import os
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Set
import json
from colorama import init, Fore, Back, Style
from .combat import Enemy, CombatManager

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
class Room:
    """Represents a room in the dungeon"""
    id: str
    title: str
    description: str
    exits: Dict[str, str]
    dark: bool
    items: List[str]
    enemy: Optional[Dict[str, Any]]
    npc: Optional[Dict[str, Any]]

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
    rooms: Dict[str, Room] = None
    defeated_enemies: Set[str] = None  # Track which enemies have been defeated

    def __post_init__(self):
        if self.defeated_enemies is None:
            self.defeated_enemies = set()

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
            debug_mode=False,
            rooms={},
            defeated_enemies=set()
        )
        self.running: bool = True
        self.load_rooms()
        self.load_enemies()
        self.combat_manager = CombatManager(
            player_health=self.game_state.health,
            player_class=self.game_state.player_class
        )

    def load_rooms(self):
        """Load room data from JSON file"""
        try:
            with open(os.path.join(os.path.dirname(__file__), 'data', 'rooms.json'), 'r') as f:
                room_data = json.load(f)
                for room_id, data in room_data.items():
                    self.game_state.rooms[room_id] = Room(
                        id=room_id,
                        title=data['title'],
                        description=data['description'],
                        exits=data['exits'],
                        dark=data['dark'],
                        items=data['items'],
                        enemy=data['enemy'],
                        npc=data['npc']
                    )
        except FileNotFoundError:
            print(Fore.RED + "Error: rooms.json not found!" + Style.RESET_ALL)
            sys.exit(1)
        except json.JSONDecodeError:
            print(Fore.RED + "Error: Invalid JSON in rooms.json!" + Style.RESET_ALL)
            sys.exit(1)

    def load_enemies(self):
        """Load enemy data from JSON file"""
        try:
            with open(os.path.join(os.path.dirname(__file__), 'data', 'enemies.json'), 'r') as f:
                self.enemies = json.load(f)
        except FileNotFoundError:
            print(Fore.RED + "Error: enemies.json not found!" + Style.RESET_ALL)
            sys.exit(1)
        except json.JSONDecodeError:
            print(Fore.RED + "Error: Invalid JSON in enemies.json!" + Style.RESET_ALL)
            sys.exit(1)

    def create_enemy(self, enemy_type: str) -> Enemy:
        """Create an enemy instance from the enemy data"""
        if enemy_type not in self.enemies:
            raise ValueError(f"Unknown enemy type: {enemy_type}")
        
        data = self.enemies[enemy_type]
        enemy = Enemy(
            name=data['name'],
            health=data['health'],
            damage_range=tuple(data['damage_range']),
            description=data['description'],
            hit_chance=data.get('hit_chance', 0.3)
        )
        
        # Initialize combat manager with current player state
        self.combat_manager = CombatManager(
            player_health=self.game_state.health,
            player_class=self.game_state.player_class
        )
        
        return enemy

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

    def display_room(self):
        """Display the current room's information"""
        room = self.game_state.rooms[self.game_state.current_room]
        
        # Check if room is dark and player has a torch
        is_dark = room.dark and "Torch" not in self.game_state.inventory
        
        print(Fore.YELLOW + f"\n{room.title}" + Style.RESET_ALL)
        
        if is_dark:
            print(Fore.RED + "It's too dark to see anything!" + Style.RESET_ALL)
        else:
            print(Fore.WHITE + room.description + Style.RESET_ALL)
            
            # Display items if any
            if room.items:
                print(Fore.CYAN + "\nItems in the room:")
                for item in room.items:
                    print(f"- {item}")
            
            # Display NPC if present
            if room.npc:
                print(Fore.BLUE + f"\n{room.npc['name']} is here:")
                print(room.npc['description'])
            
            # Display enemy if present
            if room.enemy:
                print(Fore.RED + f"\n{room.enemy['name']} is here!")
                print(room.enemy['description'])
        
        # Always show exits
        print(Fore.CYAN + "\nExits:")
        for direction, target in room.exits.items():
            print(f"- {direction.capitalize()}: {self.game_state.rooms[target].title}")
        
        # Show combat options if in combat
        if self.combat_manager.in_combat:
            print(Fore.GREEN + "\nCombat Options:")
            print("- attack: Attack the enemy")
            if self.game_state.player_class == "wizard":
                print("- cast fireball: Cast a fireball spell")
                print("- cast shield: Create a magical shield")
                print("- cast heal: Heal yourself")
            print("- flee: Attempt to flee from combat")

    def move_player(self, direction: str) -> bool:
        """Attempt to move the player in the given direction"""
        current_room = self.game_state.rooms[self.game_state.current_room]
        
        if direction not in current_room.exits:
            print(Fore.RED + f"You can't go {direction} from here!" + Style.RESET_ALL)
            return False
        
        target_room_id = current_room.exits[direction]
        target_room = self.game_state.rooms[target_room_id]
        
        # Check if the target room has a defeated enemy
        if target_room.enemy and f"{target_room_id}_{target_room.enemy['type']}" in self.game_state.defeated_enemies:
            target_room.enemy = None
        
        self.game_state.current_room = target_room_id
        self.game_state.steps_taken += 1
        return True

    def handle_command(self, command: str) -> None:
        """Process user commands"""
        if self.combat_manager.in_combat:
            self.handle_combat_command(command)
            return
        
        if command in ['q', ':q']:
            self.running = False
        elif command == ':d':
            self.game_state.debug_mode = not self.game_state.debug_mode
            if self.game_state.debug_mode:
                self.display_debug_info()
            print(f"Debug mode: {'on' if self.game_state.debug_mode else 'off'}")
        elif command in ['n', 's', 'e', 'w']:
            direction_map = {
                'n': 'north',
                's': 'south',
                'e': 'east',
                'w': 'west'
            }
            if self.move_player(direction_map[command]):
                self.display_room()
                # Check for enemy in the new room
                current_room = self.game_state.rooms[self.game_state.current_room]
                if current_room.enemy:
                    enemy = self.create_enemy(current_room.enemy['type'])
                    self.combat_manager.start_combat(enemy)
        else:
            print(Fore.RED + "Invalid command. Use n, s, e, w for movement, :d for debug mode, or q to quit." + Style.RESET_ALL)

    def handle_combat_command(self, command: str) -> None:
        """Handle combat-specific commands"""
        if not self.combat_manager.in_combat:
            print(Fore.RED + "You're not in combat!" + Style.RESET_ALL)
            return
        
        # Handle special commands even during combat
        if command in ['q', ':q']:
            self.running = False
            return
        elif command == ':d':
            self.game_state.debug_mode = not self.game_state.debug_mode
            if self.game_state.debug_mode:
                self.display_debug_info()
            print(f"Debug mode: {'on' if self.game_state.debug_mode else 'off'}")
            return
        
        # Process combat action
        ended, message = self.combat_manager.process_round(command)
        print(message)
        
        if ended:
            if self.combat_manager.player_health <= 0:
                self.game_over()
            else:
                self.game_state.health = self.combat_manager.player_health
                if self.combat_manager.enemy and self.combat_manager.enemy.health <= 0:
                    self.game_state.enemies_defeated += 1
                    # Remove enemy from the room after defeat
                    current_room = self.game_state.rooms[self.game_state.current_room]
                    if current_room.enemy:
                        # Add to defeated enemies set
                        self.game_state.defeated_enemies.add(f"{self.game_state.current_room}_{current_room.enemy['type']}")
                        current_room.enemy = None
                    print(Fore.GREEN + f"\nEnemies defeated: {self.game_state.enemies_defeated}" + Style.RESET_ALL)
                    self.display_debug_info()  # Show updated stats

    def game_over(self):
        """Handle game over state"""
        print(Fore.RED + r"""
__     ______  _    _   _      ____   _____ ______ 
\ \   / / __ \| |  | | | |    / __ \ / ____|  ____|
 \ \_/ / |  | | |  | | | |   | |  | | (___ | |__   
  \   /| |  | | |  | | | |   | |  | |\___ \|  __|  
   | | | |__| | |__| | | |___| |__| |____) | |____ 
   |_|  \____/ \____/  |______\____/|_____/|______|
""" + Style.RESET_ALL)
        print(Fore.RED + "You have died in great pain!" + Style.RESET_ALL)
        self.running = False

    def main_loop(self):
        """Main game loop"""
        self.display_room()  # Show initial room
        while self.running:
            if self.game_state.debug_mode:
                self.display_debug_info()
            
            if self.combat_manager.in_combat:
                # Show combat options
                print(Fore.GREEN + "\nCombat Options:")
                print("- attack: Attack the enemy")
                if self.game_state.player_class == "wizard":
                    print("- cast fireball: Cast a fireball spell")
                    print("- cast shield: Create a magical shield")
                    print("- cast heal: Heal yourself")
                print("- flee: Attempt to flee from combat")
                print(Fore.CYAN + "\nEnter your action: " + Style.RESET_ALL, end='')
            else:
                print(Fore.CYAN + "\nEnter command (n/s/e/w for movement, :d for debug, q to quit): " + Style.RESET_ALL, end='')
            
            command = input().strip().lower()
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
