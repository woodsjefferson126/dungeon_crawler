
# 🚀 Dungeon Crawler CLI Implementation Plan

## 🧪 Technology Stack Summary

- **Language:** Python 3.11+
- **Libraries:**
  - `colorama` (terminal color output)
  - `json` (built-in; for data storage)
  - `random` (built-in; for combat randomness)
  - `os` (built-in; optional terminal control)
  - `dataclasses` (for cleaner data structures)
- **Optional Enhancements:**
  - `rich` (for advanced terminal formatting)
  - `blessed` (for advanced input handling)

---

## 📂 Workspace Setup

### 1. Create Project Folder Structure
```bash
mkdir dungeon_crawler
cd dungeon_crawler
git init
```

Project structure:
```
/dungeon_crawler/
  dungeon_crawler.py
  rooms.json
  saves/ (directory for saved games)
README.md
requirements.txt
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install colorama
pip freeze > requirements.txt
```

(Optional later: add `rich` or `blessed` if needed.)

### 4. Create README

- Write README with game concept

### 5. Create main.py entry point

- Scaffold very basic game loop
- Create initial tests

### 6. Make Initial Git Commit
```bash
git add .
git commit -m "Initial project setup"
```



---

## 🔄 Phase 1: New User Experience

- Display ASCII title screen with intro text.
- Character class selection (Warrior, Wizard, Scoundrel).
- Allow player to choose name. Provide random D&D-style name suggestions.
- Assign starting equipment (Torch, Basic Dagger).
- Track health, inventory, and flags in a `GameState` object
- Handle invalid input.
- Add appropriate unit and integration tests.

**Milestone:** Fun and immersive player introduction complete.

---

## 🔄 Phase 2: Debug Mode

- Add `:d` command to toggle debug mode.
- Show internal game state after each move:
  - Current Room ID and Title
  - Steps Taken
  - Health
  - Inventory (with counts)
  - Flags
- Extend debug mode visibility as new features are added.
- Add appropriate unit and integration tests.

**Milestone:** Developer debug view available.

---

## 🔄 Phase 3: Core Movement System
- Create `story_data.json` containing a dungeon of 20+ rooms randomly arranged.
- Load dungeon room JSON from `story_data.json`
- Add current room to `GameState` object
- Build `Room` class (ID, Title, Description, Exits, Items, Enemy, NPC).
- Create `rooms.json` with 12 rooms inspired by Dungeons and Dragons such as `hidden_library` and `crystal_cavern`.
- Allow player to input movement commands (`n`, `s`, `e`, `w`, `u`, `d`).
- Validate commands and display funny error if invalid.
- Display room description and available exits.
- Add appropriate unit and integration tests.
- - Some rooms are marked "dark." Player must have a torch to see their description. Without a torch, players see: "It's too dark to proceed."

**Milestone:** Basic dungeon navigation working.

---

## ⚔️ Phase 4: Health and Combat System
- Track player's current room, health, inventory, and flags in a `Player` object
- Build `Enemy` class (Name, Health, Attack Range, Description).
- Detect enemy presence in room.
- Adjust player damage based on class (Warrior gets +20%).
- Implement combat flow (attack, use item, flee).
- Display colorized combat text using `colorama`.
- Extend debug mode to show enemy encounters and results.
- Add appropriate unit and integration tests.
- Trigger Game Over when health drops to zero with ASCII art.Offer reload save or quit.
- Adjust player damage based on class bonuses.
- Implement basic wizard spells.
- Boss fight in Final Boss Room.

**Milestone:** Player can fight and defeat enemies.

---

## 🧑‍🧹 Phase 5: NPC Interaction System

- Build `NPC` class (Name, Description, Options).
- Present interaction options (buy item, lore, leave).
- Apply effects: add items, update flags, remove gold.
- Extend debug mode to show NPC interactions.
- Add appropriate unit and integration tests.

**Milestone:** Player can talk to friendly characters.

---

## 🏹 Phase 6: Inventory and Items

- Create `Player` inventory system (stackable items).
- Implement using items (e.g., healing herbs, bombs).
- Display inventory in normal and debug mode.
- Add appropriate unit and integration tests.

**Milestone:** Player can manage and use inventory.

---

## 🔄 Phase 7: Save and Load System

- Save player state (room ID, inventory, health, flags, steps).
- Load player state from a save file.
- Extend debug mode to reflect loaded game state.
- Three save slots supported.
- Handle corrupted/missing save files gracefully.
- Add appropriate unit and integration tests.

**Milestone:** Player can save progress and reload it.

---

## 🔄 Phase 8: Overview Map

- Create an overview map of discovered dungeon rooms.
- Update map dynamically as player explores.
- Allow user to display map with `m` command
- Add appropriate unit and integration tests.

**Milestone:** Player can view a live overview map of explored dungeon areas.

---

## 🔄 Phase 9: Final Polish

- Add health-based hazards such as poison_gas and healing items
- Add optional flavor text for secret discoveries.
- Add replayability hooks (multiple endings, hidden flags).
- Add appropriate final tests for polish and edge cases.

**Milestone:** Game is feature-complete and polished.

---

## 🔗 Launch Plan

- Thoroughly playtest.
- Prepare a GitHub README with screenshots.
- Package final version.
- (Optional) Add extra visual upgrades with `rich`.

