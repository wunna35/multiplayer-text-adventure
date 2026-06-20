"""
Player Character System
Manages player stats, leveling, and character data.
"""

import random
from .items import Inventory

class Player:
    """Represents a player character."""
    
    def __init__(self, name, start_location="town_square"):
        self.name = name
        self.level = 1
        self.experience = 0
        self.experience_to_level = 100
        
        # Base stats
        self.max_health = 100
        self.health = self.max_health
        self.strength = 10
        self.defense = 5
        self.speed = 8
        
        # Location and state
        self.current_location = start_location
        self.inventory = Inventory()
        self.inventory.gold = 50  # Starting gold
        
        # Combat stats
        self.in_combat = False
        self.current_enemy = None
        
        # Multiplayer
        self.player_id = None
        self.is_online = True
        
    def gain_experience(self, amount):
        """Gain experience points and level up if threshold reached."""
        self.experience += amount
        if self.experience >= self.experience_to_level:
            self.level_up()
    
    def level_up(self):
        """Increase level and improve stats."""
        self.level += 1
        self.experience = 0
        self.experience_to_level = int(self.experience_to_level * 1.2)
        
        # Improve stats on level up
        self.max_health += 20
        self.health = self.max_health
        self.strength += 2
        self.defense += 1
        self.speed += 1
    
    def take_damage(self, damage):
        """Take damage and return remaining health."""
        actual_damage = max(1, damage - self.get_defense())
        self.health -= actual_damage
        return self.health
    
    def heal(self, amount):
        """Heal the player."""
        self.health = min(self.max_health, self.health + amount)
    
    def get_attack_power(self):
        """Calculate total attack power with equipment."""
        base_power = self.strength
        if self.inventory.equipped_weapon:
            base_power += self.inventory.equipped_weapon.damage
        # Add randomness to combat
        return base_power + random.randint(-2, 5)
    
    def get_defense(self):
        """Calculate total defense with equipment."""
        base_defense = self.defense
        if self.inventory.equipped_armor:
            base_defense += self.inventory.equipped_armor.defense
        return base_defense
    
    def is_alive(self):
        """Check if player is alive."""
        return self.health > 0
    
    def display_status(self):
        """Display player status."""
        status = f"""
=== {self.name} ===
Level: {self.level}
Experience: {self.experience}/{self.experience_to_level}

Health: {self.health}/{self.max_health}
Strength: {self.strength}
Defense: {self.get_defense()}
Speed: {self.speed}

Location: {self.current_location}
Gold: {self.inventory.gold}

Equipped:
  Weapon: {self.inventory.equipped_weapon if self.inventory.equipped_weapon else "None"}
  Armor: {self.inventory.equipped_armor if self.inventory.equipped_armor else "None"}
"""
        return status
    
    def move(self, new_location):
        """Move to a new location."""
        self.current_location = new_location
    
    def save_to_dict(self):
        """Convert player to dictionary for saving."""
        return {
            "name": self.name,
            "level": self.level,
            "experience": self.experience,
            "max_health": self.max_health,
            "health": self.health,
            "strength": self.strength,
            "defense": self.defense,
            "speed": self.speed,
            "current_location": self.current_location,
            "gold": self.inventory.gold,
        }
    
    @staticmethod
    def load_from_dict(data):
        """Create player from saved dictionary."""
        player = Player(data["name"], data["current_location"])
        player.level = data["level"]
        player.experience = data["experience"]
        player.max_health = data["max_health"]
        player.health = data["health"]
        player.strength = data["strength"]
        player.defense = data["defense"]
        player.speed = data["speed"]
        player.inventory.gold = data["gold"]
        return player


class NPC:
    """Represents a Non-Player Character."""
    
    def __init__(self, name, location, description, dialogue=None, quest=None):
        self.name = name
        self.location = location
        self.description = description
        self.dialogue = dialogue or ["Hello, traveler!"]
        self.quest = quest
        self.is_alive = True
        
    def greet(self):
        """Get a greeting from the NPC."""
        import random
        return random.choice(self.dialogue)
    
    def has_quest(self):
        """Check if NPC has a quest."""
        return self.quest is not None
    
    def get_quest(self):
        """Get quest information."""
        return self.quest