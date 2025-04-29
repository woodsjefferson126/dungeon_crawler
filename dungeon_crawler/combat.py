#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple
import random
from colorama import Fore, Style

@dataclass
class Enemy:
    """Represents an enemy in the dungeon"""
    name: str
    health: int
    damage_range: Tuple[int, int]
    description: str
    hit_chance: float = 0.3  # 30% chance to hit by default

    def take_damage(self, damage: int) -> bool:
        """Apply damage to the enemy and return True if defeated"""
        self.health = max(0, self.health - damage)
        return self.health <= 0

    def attack(self) -> Tuple[int, bool]:
        """Attempt to attack and return (damage, hit)"""
        if random.random() < self.hit_chance:
            damage = random.randint(*self.damage_range)
            return damage, True
        return 0, False

class CombatManager:
    """Manages combat between player and enemies"""
    def __init__(self, player_health: int, player_class: str):
        self.player_health = player_health
        self.player_class = player_class
        self.enemy: Optional[Enemy] = None
        self.in_combat = False
        self.shield_active = False
        self.shield_rounds = 0
        self.mana = 10  # Assuming a default mana value

    def start_combat(self, enemy: Enemy) -> None:
        """Start combat with an enemy"""
        self.enemy = enemy
        self.in_combat = True
        print(f"\n{Fore.RED}Combat started with {enemy.name}!{Style.RESET_ALL}")
        print(f"{Fore.RED}{enemy.description}{Style.RESET_ALL}")
        
        # Show initial combat prompt
        print(Fore.GREEN + "\nCombat Options:")
        print("- attack: Attack the enemy")
        if self.player_class == "wizard":
            print("- cast fireball: Cast a fireball spell")
            print("- cast shield: Create a magical shield")
            print("- cast heal: Heal yourself")
        print("- flee: Attempt to flee from combat")
        print(Fore.CYAN + "\nEnter your action: " + Style.RESET_ALL, end='')

    def end_combat(self) -> None:
        """End the current combat"""
        self.enemy = None
        self.in_combat = False
        self.shield_active = False
        self.shield_rounds = 0

    def player_attack(self) -> Tuple[int, bool]:
        """Player attempts to attack and return (damage, hit)"""
        # Base hit chance is 50%
        hit_chance = 0.5
        
        # Class-specific bonuses
        if self.player_class == "warrior":
            hit_chance += 0.1  # Warriors are more accurate
        
        if random.random() < hit_chance:
            # Base damage range
            damage_range = (1, 8)
            
            # Class-specific damage bonuses
            if self.player_class == "warrior":
                damage_range = (int(damage_range[0] * 1.2), int(damage_range[1] * 1.2))
            
            damage = random.randint(*damage_range)
            return damage, True
        return 0, False

    def cast_spell(self, spell_name: str) -> Tuple[int, str]:
        """Cast a spell and return (damage, message)"""
        if self.player_class != "wizard":
            return 0, "Only wizards can cast spells!"
        
        if spell_name == "fireball":
            if self.mana < 3:
                return 0, "Not enough mana to cast fireball!"
            self.mana -= 3
            damage = random.randint(8, 12)
            return damage, f"You cast fireball for {damage} damage!"
        
        elif spell_name == "shield":
            if self.mana < 2:
                return 0, "Not enough mana to cast shield!"
            self.mana -= 2
            self.shield_active = True
            self.shield_rounds = 3
            return 0, "You create a magical shield that will reduce damage by 50% for 3 rounds."
        
        elif spell_name == "heal":
            if self.mana < 4:
                return 0, "Not enough mana to cast heal!"
            self.mana -= 4
            heal_amount = random.randint(5, 10)
            self.player_health = min(20, self.player_health + heal_amount)
            return 0, f"You heal yourself for {heal_amount} health."
        
        return 0, "Unknown spell!"

    def process_round(self, player_action: str) -> Tuple[bool, str]:
        """Process a combat round and return (combat_ended, message)"""
        if not self.in_combat or not self.enemy:
            return False, "Not in combat!"
        
        message = ""
        enemy_defeated = False
        
        # Process player action
        if player_action == "attack":
            damage, hit = self.player_attack()
            if hit:
                message += f"\n{Fore.GREEN}You hit {self.enemy.name} for {damage} damage!{Style.RESET_ALL}"
                if self.enemy.take_damage(damage):
                    message += f"\n{Fore.GREEN}You defeated {self.enemy.name}!{Style.RESET_ALL}"
                    enemy_defeated = True
            else:
                message += f"\n{Fore.RED}You missed!{Style.RESET_ALL}"
        
        elif player_action.startswith("cast "):
            spell = player_action[5:]  # Get the spell name after "cast "
            damage, spell_message = self.cast_spell(spell)
            message += f"\n{Fore.BLUE}{spell_message}{Style.RESET_ALL}"
            if damage > 0 and self.enemy:
                if self.enemy.take_damage(damage):
                    message += f"\n{Fore.GREEN}You defeated {self.enemy.name}!{Style.RESET_ALL}"
                    enemy_defeated = True
        
        elif player_action == "flee":
            # Base flee chance is 50%
            flee_chance = 0.5
            
            # Class-specific bonuses
            if self.player_class == "scoundrel":
                flee_chance += 0.2  # Scoundrels are better at fleeing
            
            if random.random() < flee_chance:
                message += f"\n{Fore.GREEN}You successfully fled from {self.enemy.name}!{Style.RESET_ALL}"
                self.end_combat()
                return True, message
            else:
                message += f"\n{Fore.RED}You failed to flee!{Style.RESET_ALL}"
        
        # Enemy's turn if combat continues
        if self.in_combat and self.enemy and not enemy_defeated:
            damage, hit = self.enemy.attack()
            if hit:
                # Apply shield reduction if active
                if self.shield_active:
                    damage = int(damage * 0.5)  # 50% damage reduction
                    self.shield_rounds -= 1
                    if self.shield_rounds <= 0:
                        self.shield_active = False
                        message += f"\n{Fore.BLUE}Your shield fades away.{Style.RESET_ALL}"
                
                self.player_health = max(0, self.player_health - damage)
                message += f"\n{Fore.RED}{self.enemy.name} hit you for {damage} damage!{Style.RESET_ALL}"
                
                if self.player_health <= 0:
                    message += f"\n{Fore.RED}You have been defeated by {self.enemy.name}!{Style.RESET_ALL}"
                    self.end_combat()
                    return True, message
            else:
                message += f"\n{Fore.GREEN}{self.enemy.name} missed!{Style.RESET_ALL}"
        
        if enemy_defeated:
            self.end_combat()
            return True, message
        
        return False, message 