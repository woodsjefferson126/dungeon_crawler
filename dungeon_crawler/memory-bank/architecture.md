# 🏗️ Dungeon Crawler CLI - System Architecture

## 📦 Core Components

### 1. Game Engine (`game_engine.py`)
- **Responsibilities:**
  - Game state management
  - Main game loop
  - Command processing
  - Event handling
- **Key Classes:**
  - `GameEngine`: Main orchestrator
  - `GameState`: Current game state
  - `CommandProcessor`: Handles player input

### 2. Player System (`player.py`)
- **Responsibilities:**
  - Player state management
  - Character progression
  - Inventory management
- **Key Classes:**
  - `Player`: Main player class
  - `Inventory`: Item management
  - `CharacterClass`: Class-specific logic

### 3. World System (`world.py`)
- **Responsibilities:**
  - Room generation and management
  - Navigation system
  - Map generation
- **Key Classes:**
  - `Room`: Individual room data
    - Properties: id, title, description, exits, dark, items, enemy, npc
    - Methods: display_info(), validate_exit()
  - `World`: Overall dungeon structure
    - Properties: rooms (dict), current_room
    - Methods: load_rooms(), move_player(), get_room()
  - `MapGenerator`: Procedural generation (future implementation)
- **Implementation Details:**
  - Room data stored in JSON format
  - Color-coded room display (yellow title, white description, cyan exits)
  - Dark room mechanics requiring torch
  - Validated movement system with compass directions
  - Unit tests for room loading and movement

### 4. Combat System (`combat.py`)
- **Responsibilities:**
  - Turn-based combat management
  - Damage calculation and application
  - Special abilities and spell casting
  - Combat state tracking
  - Enemy defeat handling
- **Key Classes:**
  - `CombatManager`: Combat flow orchestration
    - Properties: player_health, player_class, enemy, in_combat, shield_active, shield_rounds, mana
    - Methods: start_combat(), end_combat(), player_attack(), cast_spell(), process_round()
  - `Enemy`: Enemy behavior and state
    - Properties: name, health, damage_range, description, hit_chance
    - Methods: take_damage(), attack()
- **Implementation Details:**
  - Color-coded combat text (red for damage, green for success)
  - Class-specific combat bonuses
  - Wizard spell system with mana costs
  - Shield spell damage reduction
  - Combat state persistence
  - Enemy defeat tracking
  - Unit tests for combat mechanics

### 5. NPC System (`npc.py`)
- **Responsibilities:**
  - NPC interactions
  - Dialogue trees
  - State management
- **Key Classes:**
  - `NPC`: Individual NPC data
  - `DialogueManager`: Conversation handling
  - `NPCState`: NPC-specific state

### 6. Persistence System (`persistence.py`)
- **Responsibilities:**
  - Save/load functionality
  - Game state serialization
  - Data validation
- **Key Classes:**
  - `SaveManager`: Save/load operations
  - `GameStateSerializer`: State serialization

### 7. UI System (`ui.py`)
- **Responsibilities:**
  - Terminal output formatting
  - Color management
  - Input handling
- **Key Classes:**
  - `TerminalUI`: Main UI handler
  - `ColorManager`: Color scheme management
  - `InputHandler`: User input processing

## 🔄 Data Flow

1. **Game Initialization:**
   ```
   main.py → GameEngine → World → Player
   ```

2. **Game Loop:**
   ```
   Input → CommandProcessor → GameEngine → 
   [Combat/NPC/World] → UI → Output
   ```

3. **Save/Load:**
   ```
   GameState → SaveManager → JSON → File System
   ```

## 📁 Project Structure

```
dungeon_crawler/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── game_engine.py
│   ├── player.py
│   ├── world.py
│   ├── combat.py
│   ├── npc.py
│   ├── persistence.py
│   └── ui.py
├── data/
│   ├── rooms.json
│   ├── enemies.json
│   └── npcs.json
├── tests/
│   ├── __init__.py
│   ├── test_game_engine.py
│   ├── test_player.py
│   └── ...
└── saves/
    └── (player save files)
```

## 🔒 Key Design Decisions

1. **State Management:**
   - Centralized `GameState` class
   - Immutable state updates
   - Event-driven architecture

2. **Data Storage:**
   - JSON for static data (rooms, enemies, NPCs)
   - JSON for save files
   - Simple file-based persistence

3. **Error Handling:**
   - Custom exceptions for game-specific errors
   - Graceful degradation
   - Input validation at all levels

4. **Testing Strategy:**
   - Unit tests for core systems
   - Integration tests for game flow
   - Mock-based testing for UI components

## 🔄 Dependencies

- `colorama`: Terminal color management
- `json`: Data serialization
- `random`: Game mechanics
- `os`: File system operations
- `dataclasses`: Data structure management

## 🎯 Future Considerations

1. **Performance:**
   - Room generation optimization
   - Save file compression
   - Memory usage monitoring

2. **Extensibility:**
   - Plugin system for new features
   - Mod support
   - Custom content creation

3. **Maintenance:**
   - Logging system
   - Debug tools
   - Performance metrics
