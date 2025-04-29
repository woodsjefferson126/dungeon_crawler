# Depths of the Forgotten (CLI Edition)

A text-based dungeon crawler adventure game where you explore mysterious dungeons, battle fearsome enemies, and uncover ancient secrets.

## 🎮 Features

- Rich text-based dungeon exploration with colorful output
- Three character classes: Warrior, Wizard, and Scoundrel
- Turn-based combat system with unique class abilities
- Interactive NPCs with dynamic relationships
- Inventory system with stackable items
- Multiple save slots
- Debug mode for development

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd dungeon-crawler
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Game

```bash
python dungeon_crawler.py
```

## 🎯 How to Play

- Use compass directions for movement (n/e/s/w/u/d)
- Type commands when prompted
- Toggle debug mode with :d
- Save your game progress in one of three slots
- Press 'q' to quit

### Character Classes

- **Warrior**: High health (12-15 HP), +20% combat damage
- **Wizard**: Access to spells (Fireball, Shield, Heal)
- **Scoundrel**: Better escape chance, lock picking ability

### Items

- Stackable items (max 5 per stack): Torches, Healing Herbs, Bombs
- Key items: Ancient Tomes, Keys, Weapons

## 🛠️ Development

Built with:
- Python 3.11+
- colorama (terminal colors)

## 📝 License

[License information here]
