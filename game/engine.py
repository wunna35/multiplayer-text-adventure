"""
Game Engine
Core game logic and command processing.
"""

import random
import json
import os
from .player import Player
from .world import World
from .combat import Combat, spawn_random_enemy
from .items import create_item

class GameEngine:
    """Main game engine handling all game logic."""
    
    def __init__(self):
        self.world = World()
        self.player = None
        self.current_combat = None
        self.running = False
        self.saves_dir = "saves"
        
        # Create saves directory if it doesn't exist
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)
    
    def start_new_game(self, player_name):
        """Initialize a new game."""
        self.player = Player(player_name)
        self.running = True
        
        # Add starting items
        self.player.inventory.add_item(create_item("rusty_sword"))
        self.player.inventory.add_item(create_item("leather_armor"))
        self.player.inventory.add_item(create_item("health_potion"))
        self.player.inventory.add_item(create_item("health_potion"))
        
        return f"Welcome, {player_name}! Your adventure begins in the Town Square.\n"
    
    def process_command(self, command):
        """Process player commands."""
        command = command.lower().strip()
        parts = command.split()
        
        if not parts:
            return ""
        
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Command routing
        if cmd == "help":
            return self.cmd_help()
        elif cmd == "look":
            return self.cmd_look()
        elif cmd == "go" or cmd == "move":
            return self.cmd_go(args)
        elif cmd == "inventory" or cmd == "inv":
            return self.cmd_inventory()
        elif cmd == "take" or cmd == "pickup":
            return self.cmd_take(" ".join(args))
        elif cmd == "drop":
            return self.cmd_drop(" ".join(args))
        elif cmd == "examine":
            return self.cmd_examine(" ".join(args))
        elif cmd == "equip":
            return self.cmd_equip(" ".join(args))
        elif cmd == "use":
            return self.cmd_use(" ".join(args))
        elif cmd == "attack":
            return self.cmd_attack(" ".join(args))
        elif cmd == "status":
            return self.player.display_status()
        elif cmd == "talk" or cmd == "speak":
            return self.cmd_talk(" ".join(args))
        elif cmd == "map":
            return self.world.display_map()
        elif cmd == "save":
            return self.cmd_save(" ".join(args) if args else "autosave")
        elif cmd == "load":
            return self.cmd_load(" ".join(args) if args else "autosave")
        elif cmd == "quit" or cmd == "exit":
            self.running = False
            return "Thanks for playing! Goodbye."
        else:
            return f"Unknown command: '{cmd}'. Type 'help' for available commands."
    
    def cmd_help(self):
        """Display help information."""
        help_text = """
╔════════════════════════════════════════╗
║         AVAILABLE COMMANDS             ║
╠════════════════════════════════════════╣
║ Movement:                              ║
║  go <direction>    - Move (north, etc) ║
║  look              - View location     ║
║                                        ║
║ Inventory:                             ║
║  inventory (inv)   - View items        ║
║  take <item>       - Pick up item      ║
║  drop <item>       - Drop item         ║
║  examine <item>    - Inspect item      ║
║  equip <item>      - Equip weapon/armor║
║  use <item>        - Use item (potion) ║
║                                        ║
║ Combat:                                ║
║  attack <enemy>    - Attack enemy      ║
║  attack            - Continue fighting ║
║                                        ║
║ Other:                                 ║
║  status            - View stats        ║
║  talk <npc>        - Talk to NPC       ║
║  map               - View world map    ║
║  save <name>       - Save game         ║
║  load <name>       - Load game         ║
║  help              - This message      ║
║  quit              - Exit game         ║
╚════════════════════════════════════════╝
        """
        return help_text
    
    def cmd_look(self):
        """Look at current location."""
        location = self.world.get_location(self.player.current_location)
        if location:
            return location.get_full_description()
        return "You are lost!"
    
    def cmd_go(self, args):
        """Move to a new location."""
        if not args:
            return "Go where? Specify a direction (north, south, east, west, up, down)."
        
        direction = args[0].lower()
        location = self.world.get_location(self.player.current_location)
        
        if location and direction in location.exits:
            new_location = location.exits[direction]
            self.player.move(new_location)
            return f"You travel {direction}.\n\n" + self.cmd_look()
        else:
            return f"You cannot go {direction} from here."
    
    def cmd_inventory(self):
        """Display inventory."""
        return self.player.inventory.display_inventory()
    
    def cmd_take(self, item_name):
        """Pick up an item."""
        if not item_name:
            return "Take what? Specify an item name."
        
        location = self.world.get_location(self.player.current_location)
        
        for item in location.items:
            if item.name.lower() == item_name.lower():
                if self.player.inventory.add_item(item):
                    location.remove_item(item)
                    return f"You take the {item.name}."
                else:
                    return "Your inventory is full!"
        
        return f"There is no {item_name} here."
    
    def cmd_drop(self, item_name):
        """Drop an item."""
        if not item_name:
            return "Drop what? Specify an item name."
        
        item = self.player.inventory.remove_item(item_name)
        if item:
            location = self.world.get_location(self.player.current_location)
            location.add_item(item)
            return f"You drop the {item.name}."
        else:
            return f"You don't have a {item_name}."
    
    def cmd_examine(self, item_name):
        """Examine an item."""
        if not item_name:
            return "Examine what? Specify an item name."
        
        item = self.player.inventory.get_item(item_name)
        if item:
            return f"{item.name}\n{item.description}\nValue: {item.value} gold"
        
        location = self.world.get_location(self.player.current_location)
        for item in location.items:
            if item.name.lower() == item_name.lower():
                return f"{item.name}\n{item.description}\nValue: {item.value} gold"
        
        return f"You don't see a {item_name}."
    
    def cmd_equip(self, item_name):
        """Equip a weapon or armor."""
        if not item_name:
            return "Equip what? Specify an item name."
        
        item = self.player.inventory.get_item(item_name)
        if not item:
            return f"You don't have a {item_name}."
        
        if item.item_type == "weapon":
            self.player.inventory.equip_weapon(item_name)
            return f"You equip the {item.name}."
        elif item.item_type == "armor":
            self.player.inventory.equip_armor(item_name)
            return f"You wear the {item.name}."
        else:
            return f"You cannot equip {item.name}."
    
    def cmd_use(self, item_name):
        """Use an item."""
        if not item_name:
            return "Use what? Specify an item name."
        
        item = self.player.inventory.get_item(item_name)
        if not item:
            return f"You don't have a {item_name}."
        
        if item.item_type == "potion":
            if item.effect_type == "heal":
                self.player.heal(item.effect_value)
                self.player.inventory.remove_item(item_name)
                return f"You drink the {item.name} and restore {item.effect_value} HP!\n" + \
                       f"Health: {self.player.health}/{self.player.max_health}"
        
        return f"You can't use {item.name} right now."
    
    def cmd_attack(self, enemy_name):
        """Attack an enemy."""
        if self.current_combat:
            # Continue existing combat
            turn_log = self.current_combat.do_turn()
            if turn_log:
                result = turn_log
                if not self.current_combat.is_combat_active():
                    result += self.current_combat.end_combat()
                    self.current_combat = None
                return result
            else:
                return "Combat has ended!"
        
        location = self.world.get_location(self.player.current_location)
        
        if not enemy_name:
            # Check for enemies in location
            if not location.enemies:
                return "There are no enemies here to attack!"
            enemy_name = location.enemies[0].name.lower()
        
        # Find enemy
        for enemy in location.enemies:
            if enemy.name.lower() == enemy_name.lower():
                enemy_copy = spawn_random_enemy() if enemy.name.lower() == "random" else enemy
                self.current_combat = Combat(self.player, enemy_copy)
                location.enemies.remove(enemy)
                
                result = self.current_combat.start_combat()
                result += self.current_combat.do_turn()
                
                if not self.current_combat.is_combat_active():
                    result += self.current_combat.end_combat()
                    self.current_combat = None
                
                return result
        
        return f"There is no {enemy_name} here."
    
    def cmd_talk(self, npc_name):
        """Talk to an NPC."""
        location = self.world.get_location(self.player.current_location)
        
        for npc in location.npcs:
            if npc.name.lower() == npc_name.lower():
                message = f"{npc.name}: {npc.greet()}"
                if npc.has_quest():
                    message += f"\n\nQuest: {npc.quest}"
                return message
        
        return f"There is no {npc_name} here."
    
    def cmd_save(self, save_name):
        """Save the game."""
        if not self.player:
            return "No game in progress."
        
        save_data = {
            "player": self.player.save_to_dict(),
            "location": self.player.current_location
        }
        
        filepath = os.path.join(self.saves_dir, f"{save_name}.json")
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        return f"Game saved as '{save_name}'."
    
    def cmd_load(self, save_name):
        """Load a saved game."""
        filepath = os.path.join(self.saves_dir, f"{save_name}.json")
        
        if not os.path.exists(filepath):
            return f"Save file '{save_name}' not found."
        
        with open(filepath, 'r') as f:
            save_data = json.load(f)
        
        self.player = Player.load_from_dict(save_data["player"])
        self.player.current_location = save_data["location"]
        self.running = True
        
        return f"Game loaded from '{save_name}'.\n\n" + self.cmd_look()