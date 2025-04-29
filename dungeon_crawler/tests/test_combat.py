#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dungeon_crawler.combat import Enemy, CombatManager

class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.enemy = Enemy(
            name="Test Goblin",
            health=10,
            damage_range=(1, 4),
            description="A small but fierce goblin"
        )

    def test_enemy_initialization(self):
        self.assertEqual(self.enemy.name, "Test Goblin")
        self.assertEqual(self.enemy.health, 10)
        self.assertEqual(self.enemy.damage_range, (1, 4))
        self.assertEqual(self.enemy.description, "A small but fierce goblin")
        self.assertEqual(self.enemy.hit_chance, 0.3)

    def test_take_damage(self):
        # Test normal damage
        self.assertFalse(self.enemy.take_damage(5))
        self.assertEqual(self.enemy.health, 5)
        
        # Test lethal damage
        self.assertTrue(self.enemy.take_damage(5))
        self.assertEqual(self.enemy.health, 0)
        
        # Test overkill
        self.enemy.health = 10
        self.assertTrue(self.enemy.take_damage(15))
        self.assertEqual(self.enemy.health, 0)

    @patch('random.random')
    def test_attack(self, mock_random):
        # Test successful hit
        mock_random.return_value = 0.1  # Less than hit_chance
        damage, hit = self.enemy.attack()
        self.assertTrue(hit)
        self.assertTrue(1 <= damage <= 4)
        
        # Test miss
        mock_random.return_value = 0.5  # More than hit_chance
        damage, hit = self.enemy.attack()
        self.assertFalse(hit)
        self.assertEqual(damage, 0)

class TestCombatManager(unittest.TestCase):
    def setUp(self):
        self.combat_manager = CombatManager(player_health=20, player_class="warrior")
        self.enemy = Enemy(
            name="Test Goblin",
            health=10,
            damage_range=(1, 4),
            description="A small but fierce goblin"
        )

    def test_combat_initialization(self):
        self.assertEqual(self.combat_manager.player_health, 20)
        self.assertEqual(self.combat_manager.player_class, "warrior")
        self.assertFalse(self.combat_manager.in_combat)
        self.assertIsNone(self.combat_manager.enemy)
        self.assertFalse(self.combat_manager.shield_active)
        self.assertEqual(self.combat_manager.shield_rounds, 0)

    def test_start_combat(self):
        self.combat_manager.start_combat(self.enemy)
        self.assertTrue(self.combat_manager.in_combat)
        self.assertEqual(self.combat_manager.enemy, self.enemy)

    def test_end_combat(self):
        self.combat_manager.start_combat(self.enemy)
        self.combat_manager.end_combat()
        self.assertFalse(self.combat_manager.in_combat)
        self.assertIsNone(self.combat_manager.enemy)
        self.assertFalse(self.combat_manager.shield_active)
        self.assertEqual(self.combat_manager.shield_rounds, 0)

    @patch('random.random')
    def test_player_attack(self, mock_random):
        self.combat_manager.start_combat(self.enemy)
        
        # Test successful hit
        mock_random.return_value = 0.1  # Less than hit_chance
        damage, hit = self.combat_manager.player_attack()
        self.assertTrue(hit)
        self.assertTrue(1 <= damage <= 9)  # Warrior bonus applied
        
        # Test miss
        mock_random.return_value = 0.7  # More than hit_chance
        damage, hit = self.combat_manager.player_attack()
        self.assertFalse(hit)
        self.assertEqual(damage, 0)

    def test_cast_spell(self):
        # Test non-wizard
        damage, message = self.combat_manager.cast_spell("fireball")
        self.assertEqual(damage, 0)
        self.assertEqual(message, "Only wizards can cast spells!")
        
        # Test wizard with fireball
        wizard_combat = CombatManager(player_health=20, player_class="wizard")
        damage, message = wizard_combat.cast_spell("fireball")
        self.assertTrue(8 <= damage <= 12)
        self.assertEqual(message, f"You cast fireball for {damage} damage!")
        self.assertEqual(wizard_combat.mana, 7)  # 10 - 3 mana cost
        
        # Test shield spell
        damage, message = wizard_combat.cast_spell("shield")
        self.assertEqual(damage, 0)
        self.assertEqual(message, "You create a magical shield that will reduce damage by 50% for 3 rounds.")
        self.assertTrue(wizard_combat.shield_active)
        self.assertEqual(wizard_combat.shield_rounds, 3)
        self.assertEqual(wizard_combat.mana, 5)  # 7 - 2 mana cost
        
        # Test heal spell
        wizard_combat.player_health = 10
        damage, message = wizard_combat.cast_spell("heal")
        self.assertEqual(damage, 0)
        self.assertTrue("You heal yourself for" in message)
        self.assertTrue(10 < wizard_combat.player_health <= 20)
        self.assertEqual(wizard_combat.mana, 1)  # 5 - 4 mana cost
        
        # Test not enough mana
        damage, message = wizard_combat.cast_spell("fireball")
        self.assertEqual(damage, 0)
        self.assertEqual(message, "Not enough mana to cast fireball!")
        self.assertEqual(wizard_combat.mana, 1)  # Mana shouldn't change

    @patch('random.random')
    def test_process_round(self, mock_random):
        self.combat_manager.start_combat(self.enemy)
        
        # Test successful attack
        mock_random.return_value = 0.1  # Always hit
        ended, message = self.combat_manager.process_round("attack")
        self.assertTrue("You hit" in message)
        
        # Test failed flee
        mock_random.return_value = 0.8  # Always fail flee
        ended, message = self.combat_manager.process_round("flee")
        self.assertFalse(ended)
        self.assertTrue("failed to flee" in message)
        
        # Test successful flee
        mock_random.return_value = 0.1  # Always succeed flee
        ended, message = self.combat_manager.process_round("flee")
        self.assertTrue(ended)
        self.assertTrue("successfully fled" in message)

if __name__ == '__main__':
    unittest.main() 