# 🏰 Dungeon Crawler CLI – Design Document



# 📜 Title

**Depths of the Forgotten** (CLI Edition)



# 🎮 Game Overview

**Genre:** Text-based Dungeon Crawler / Interactive Fiction  
**Platform:** Command Line
**Style:** Dark fantasy, minimal, text only with colorful output



# 🧬 Core Gameplay

Players explore a dungeon, make directional choices, encounter enemies, interact with friendly or neutral NPCs, and can toggle a debug mode to inspect the current game state.

## 🏆 Victory Condition

* Defeat the dungeon boss to win.

## Player Death

* Players die with health drops to zero
* Player is told "You have died in great pain", show ASCII art, offer to reload last save or restart from scratch.

ASCII art to show:
```
__     ______  _    _   _      ____   _____ ______ 
  \ \   / / __ \| |  | | | |    / __ \ / ____|  ____|
   \ \_/ / |  | | |  | | | |   | |  | | (___ | |__   
    \   /| |  | | |  | | | |   | |  | |\___ \|  __|  
     | | | |__| | |__| | | |___| |__| |____) | |____ 
     |_|  \____/ \____/  |______\____/|_____/|______|
```

# 🧪 Game Engine Overview

- Load rooms, handle movement
- Track:
  - Current Room
  - Player Health
  - Inventory (with stackable items)
  - Flags
  - Steps Taken
- Handle:
  - Combat
  - NPC dialogue trees
  - Saving/loading
  - Debug toggling
  - Colorful output display

# 💻 Features

## 👤 Player

- **Attributes:**
  - `Health`: Tracks damage taken (integer)
  - `Inventory`: List of strings representing key items
  - `Current Room`: Points to the room ID or label
  - `Flags`: Boolean markers for special story progress

- **Start State:**
  - Health: 100
  - Inventory: [Rusty Dagger, Torch]
  - Current Room: "entry_hall"


## 🖥️ Colorized Text (Colorama)

The game uses Colorama for colorful CLI output.

| Purpose           | Color                        |
| ----------------- | ---------------------------- |
| Room Title        | Yellow                       |
| Room Description  | White                        |
| Available Exits   | Cyan                         |
| Combat Messages   | Red (enemy) / Green (player) |
| Debug Information | Magenta                      |
| NPC Dialogue      | Blue                         |

## 🌐 New Player Experience

1. **Title Screen:** Display an ASCII banner and colorful intro.
2. **Character Class Selection:**  

| Class      | Special Ability                  | Starting Health | Damage inflicted in combat |
| ---------- | -------------------------------- | --------------- | -------------------------- |
| Warrior    | Deals +20% combat damage        | 12-15 HP         | 1-15 HP |
| Wizard     | Gains access to spells (Fireball, Shield, Heal) | 8-12 HP | 1-8 HP |
| Scoundrel  | +20% chance to flee successfully. Has 50% chance of picking locks. | 1-12 HP         | 1-8 HP |

3. **Name Selection:** A random D&D-style name is suggested or user can pick their own.
4. **Starting Equipment:** Torch (stackable) and a basic dagger.



# 🗺️ Room Structure & Compass Navigation

## 🧱 Room Format

Stored as JSON:
* Room description
* Some rooms have a `dark: true` flag which means player needs a torch. Without a torch: display "It's too dark to proceed."
* Monsters, NPCs, items that are present
* Available actions
* Available exits

Example JSON for a boss lair:

```
{
  "id": "boss_lair",
  "title": "Lair of the Forgotten King",
  "description": "A massive cavern lit by an eerie green glow. At its center stands the towering figure of the Forgotten King.",
  "options": [
    {"text": "Search for a useful book.", "effect": "add_item:ancient_tome"},
    {"text": "Run away screaming.", "next": "dark_temple"},
    {"text": "Continue into the dungeon.", "next": "crystal_cavern"}
  ]
  "enemy": {
    "name": "Forgotten King",
    "health": 50,
    "damage": [5, 20],
    "description": "An ancient monarch who clings to unlife, seeking to drag all into darkness."
  },
  "dark": false
}
```

## Prompt format:**
  ```
  Room: Entry Hall
  You stand in a crumbling stone hall. The air smells of damp and dust.

  1) Go north into the darkness.
  2) Light your torch.

  Choose an option: _
  ```

## 🔄 Navigation Mapping

n/e/s/w/u/d for North/East/South/West/Up/Down movement.



# ⚔️ Combat System

Player attacks deal damage randomly generated within a set range based on character class.

## 🧟 Enemy Data

Stored as JSON:
* Monster type and description
* Weapon
* Health
* Attack damage done (default 1-8 HP, 5-10 HP for boss)


## Bosses

Each dungeon has one boss located in a random room. They have more health and do more damage than all other monsters.

## ⚔️ Combat Flow

Combat is turn-based. Each turn, player or enemy can:
* Attack, players have a 50% chance of doing damage. Monsters have a 30% chance. Damage varies by NPC.
* Use item, e.g. invisibility potion
* Cast spell (wizard only)
  * `Fireball`: Heavy damage (5-20 HP)
  * `Shield`: Damage reduced by 50% for next 3 rounds
  * `Heal`: 30% HP restored
* Flee with a chance of success.




# 🧑‍🤝‍🧑 Friendly/Neutral NPC System

## 🧑‍🤝‍🧑 NPC Data

Stored as JSON:
* % chance that NPC will become an enemy after each player interaction (default: 5%)
* Dialogue tree with interaction options, e.g. give gold, provide hints for boss fight



## 🛣️ NPC Interaction Flow

Choose dialogue options and affect the game state.



# 🎒 Inventory System

Player can carry up to 5 items. Examples include:

| Item         | Use                           | Stackable |
| ------------ | ----------------------------- | --------- |
| Torch        | Required to explore dark areas | Yes       |
| Healing Herb | Heal 20 HP                    | Yes       |
| Iron Key     | Open specific doors           | No        |
| Bomb         | Deal 10 HP damage to enemies  | Yes       |
| Ancient Tome | Provides knowledge for advanced puzzles  |
| Shiny Sword  | Enhances combat effectiveness            |
| Golden Key   | Unlocks special treasure rooms           |


# 🐞 Debug Mode

Toggle `:d` to view internal game state for testing.


# 🛡️ Save and Load

*  Three save slots.
*  Friendly error handling for corrupted saves.


# 🔁 Replayability Features

- Alternate endings
- Secret rooms and hidden flags
- Variable NPC outcomes



# 🚀 How to Run

```bash
pip install colorama
python dungeon_crawler.py
```



# ✅ Summary of Features

- Compass-based movement (including up/down)
- Turn-based combat system
- Friendly NPC interactions
- ASCII title screen
- Inventory with stackable items
- Colorful terminal output (Colorama)
- Save/load support
- Developer debug mode


# Possible future extensions

* Science fiction version
* Add XP and player levels
* high-contrast option for colorblind users later.
* Procedural dungeon generation.
* Time-based events (enemy patrols).
* In-game achievements or lore collectibles.
* Advanced class upgrades (e.g., Warrior > Knight).
