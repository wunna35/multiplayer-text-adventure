# Multiplayer Text-Based Adventure Game

A full-featured, immersive text-based adventure game written in Python with multiplayer support. Explore a rich fantasy world, fight monsters, solve puzzles, and interact with NPCs in a shared game universe.

## Features

- **Multiplayer Support**: Multiple players can connect and play in the same world simultaneously
- **Rich World System**: Multiple interconnected locations with unique descriptions and NPCs
- **Combat System**: Turn-based combat with weapons, armor, and abilities
- **Inventory Management**: Collect items, use potions, equip gear
- **Character Progression**: Level up, gain experience, improve stats
- **NPC Interactions**: Quest-giving NPCs with dialogue system
- **Save/Load System**: Save your progress and resume later
- **Player Interactions**: Trade with other players, form parties
- **Puzzle System**: Environmental puzzles to solve for rewards

## Installation

### Requirements
- Python 3.8+
- No external dependencies required (uses only standard library)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/wunna35/multiplayer-text-adventure.git
cd multiplayer-text-adventure
```

2. Run the game:
```bash
python main.py
```

3. For multiplayer (server):
```bash
python server.py
```

4. For multiplayer (client - in another terminal):
```bash
python client.py
```

## How to Play

### Basic Commands

- `help` - Display available commands
- `look` - Examine your current location
- `go <direction>` - Move in a direction (north, south, east, west)
- `inventory` or `inv` - View your inventory
- `examine <item>` - Examine an item
- `take <item>` - Pick up an item
- `drop <item>` - Drop an item
- `equip <item>` - Equip a weapon or armor
- `attack <enemy>` - Attack an enemy
- `use <item>` - Use an item (potion, key, etc.)
- `talk <npc>` - Talk to an NPC
- `status` - View character stats
- `save` - Save your game
- `load` - Load a saved game
- `players` - See other players in the world
- `trade <player>` - Initiate trade with another player
- `quit` - Exit the game

### Combat

- Turn-based system where you and enemies take turns attacking
- Damage depends on your weapon and the enemy's armor
- Healing potions restore health
- Victory grants experience and loot

### Progression

- Gain experience from defeating enemies
- Level up to increase stats (health, strength, defense)
- Discover new abilities as you progress
- Find better equipment to improve performance

## Project Structure

```
multiplayer-text-adventure/
├── main.py              # Single-player entry point
├── server.py            # Multiplayer server
├── client.py            # Multiplayer client
├── game/
│   ├── __init__.py
│   ├── engine.py        # Core game engine
│   ├── world.py         # World and location definitions
│   ├── player.py        # Player class and management
│   ├── npc.py           # NPC definitions and interactions
│   ├── items.py         # Item system
│   ├── combat.py        # Combat system
│   └── database.py      # Save/load system
├── data/
│   ├── locations.json   # Location data
│   ├── npcs.json        # NPC data
│   └── items.json       # Item definitions
└── saves/               # Saved games directory
```

## Contributing

Feel free to fork, modify, and expand this game! Some ideas:
- Add new locations and quests
- Implement new enemy types
- Create new items and abilities
- Improve the UI with better formatting
- Add sound effects or ASCII art

## License

MIT License - Feel free to use this for learning or as a base for your own game!

## Author

Created as a demonstration of game design patterns in Python.

---

Enjoy your adventure! 🎮