#!/usr/bin/env python3

import sys
import time
from dataclasses import dataclass
from typing import List, Dict, Optional
import json
from colorama import init, Fore, Back, Style

# Initialize colorama
init()

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
        """Display the game's title screen"""
        print(Fore.YELLOW + Style.BRIGHT + """
╔══════════════════════════════════════════╗
║     Depths of the Forgotten (CLI)        ║
║            - Version 1.0 -               ║
╚══════════════════════════════════════════╝
""" + Style.RESET_ALL)

    def get_input(self, prompt: str) -> str:
        """Get input from the user with proper formatting"""
        print(Fore.CYAN + prompt + Style.RESET_ALL, end='')
        return input().strip().lower()

    def display_debug_info(self):
        """Display debug information"""
        print(Fore.MAGENTA + "\n=== DEBUG INFO ===")
        print(f"Room: {self.game_state.current_room}")
        print(f"Steps: {self.game_state.steps_taken}")
        print(f"Health: {self.game_state.health}")
        print(f"Inventory: {self.game_state.inventory}")
        print(f"Enemies Defeated: {self.game_state.enemies_defeated}")
        print(f"Items Used: {self.game_state.items_used}")
        print(f"Time Elapsed: {int(time.time() - self.game_state.start_time)}s")
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
