"""
Item and Inventory System
Handles all items, equipment, and inventory management.
"""

class Item:
    """Represents a single item in the game."""
    
    def __init__(self, name, item_type, description, value=0, rarity="common"):
        self.name = name
        self.item_type = item_type  # "weapon", "armor", "potion", "consumable", "key", "misc"
        self.description = description
        self.value = value  # Gold value
        self.rarity = rarity  # common, uncommon, rare, epic, legendary
        self.equipped = False
        
    def __str__(self):
        return f"{self.name} ({self.rarity})"
    
    def __repr__(self):
        return f"Item({self.name})"


class Weapon(Item):
    """A weapon item with damage stats."""
    
    def __init__(self, name, description, damage, value=0, rarity="common"):
        super().__init__(name, "weapon", description, value, rarity)
        self.damage = damage
        
    def __str__(self):
        return f"{self.name} (DMG: {self.damage})"


class Armor(Item):
    """An armor item with defense stats."""
    
    def __init__(self, name, description, defense, value=0, rarity="common"):
        super().__init__(name, "armor", description, value, rarity)
        self.defense = defense
        
    def __str__(self):
        return f"{self.name} (DEF: {self.defense})"


class Potion(Item):
    """A consumable potion with healing/buff effects."""
    
    def __init__(self, name, description, effect_type, effect_value, value=0, rarity="common"):
        super().__init__(name, "potion", description, value, rarity)
        self.effect_type = effect_type  # "heal", "strength", "defense", "speed"
        self.effect_value = effect_value
        
    def __str__(self):
        return f"{self.name} ({self.effect_type} +{self.effect_value})"


class Inventory:
    """Manages player inventory with weight and capacity limits."""
    
    def __init__(self, max_weight=100):
        self.items = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.max_weight = max_weight
        self.gold = 0
        
    def add_item(self, item):
        """Add an item to inventory."""
        if len(self.items) < 20:  # Max 20 items
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item_name):
        """Remove an item by name."""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                return item
        return None
    
    def get_item(self, item_name):
        """Get an item by name."""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None
    
    def equip_weapon(self, weapon_name):
        """Equip a weapon from inventory."""
        weapon = self.get_item(weapon_name)
        if weapon and isinstance(weapon, Weapon):
            self.equipped_weapon = weapon
            return True
        return False
    
    def equip_armor(self, armor_name):
        """Equip armor from inventory."""
        armor = self.get_item(armor_name)
        if armor and isinstance(armor, Armor):
            self.equipped_armor = armor
            return True
        return False
    
    def unequip_weapon(self):
        """Unequip current weapon."""
        self.equipped_weapon = None
    
    def unequip_armor(self):
        """Unequip current armor."""
        self.equipped_armor = None
    
    def get_total_weight(self):
        """Calculate total inventory weight."""
        return len(self.items) * 2  # Simplified weight system
    
    def display_inventory(self):
        """Display inventory contents."""
        if not self.items:
            return "Your inventory is empty."
        
        inventory_str = "=== Inventory ===\n"
        for i, item in enumerate(self.items, 1):
            equipped_str = " [EQUIPPED]" if (item == self.equipped_weapon or item == self.equipped_armor) else ""
            inventory_str += f"{i}. {item}{equipped_str}\n"
        
        if self.equipped_weapon:
            inventory_str += f"\nWeapon: {self.equipped_weapon}\n"
        if self.equipped_armor:
            inventory_str += f"Armor: {self.equipped_armor}\n"
        
        inventory_str += f"Gold: {self.gold}\n"
        return inventory_str
    
    def list_items(self):
        """Return list of item names."""
        return [item.name for item in self.items]


# Predefined items for the game
ITEMS_DATABASE = {
    # Weapons
    "rusty_sword": Weapon("Rusty Sword", "An old, corroded sword", 5, 10, "common"),
    "iron_sword": Weapon("Iron Sword", "A solid iron blade", 12, 50, "uncommon"),
    "steel_sword": Weapon("Steel Sword", "A well-crafted steel weapon", 18, 150, "rare"),
    "excalibur": Weapon("Excalibur", "A legendary sword of immense power", 30, 1000, "legendary"),
    "wooden_staff": Weapon("Wooden Staff", "A simple wooden staff for casting spells", 8, 20, "common"),
    "mage_staff": Weapon("Mage's Staff", "A staff infused with magical energy", 16, 200, "rare"),
    
    # Armor
    "leather_armor": Armor("Leather Armor", "Basic leather protection", 3, 30, "common"),
    "iron_armor": Armor("Iron Armor", "Heavy iron plating", 8, 100, "uncommon"),
    "steel_armor": Armor("Steel Armor", "Superior steel protection", 15, 300, "rare"),
    "dragon_scale": Armor("Dragon Scale Mail", "Armor crafted from dragon scales", 25, 1000, "legendary"),
    
    # Potions
    "health_potion": Potion("Health Potion", "Restores 30 HP", "heal", 30, 15, "common"),
    "super_potion": Potion("Super Potion", "Restores 75 HP", "heal", 75, 50, "uncommon"),
    "elixir": Potion("Elixir of Life", "Restores all HP", "heal", 999, 200, "rare"),
    "strength_potion": Potion("Strength Potion", "Increases damage by 5 for one battle", "strength", 5, 25, "uncommon"),
    "defense_potion": Potion("Defense Potion", "Increases defense by 3 for one battle", "defense", 3, 25, "uncommon"),
    
    # Keys and Misc
    "rusty_key": Item("Rusty Key", "key", "An old, rusty key. Opens the chest in the dungeon.", 5, "common"),
    "golden_key": Item("Golden Key", "key", "A beautiful golden key. Unlocks the treasure room.", 100, "rare"),
    "map": Item("Old Map", "misc", "A worn map showing locations of treasure.", 50, "uncommon"),
    "crystal": Item("Crystal", "misc", "A shimmering crystal with mysterious energy.", 75, "rare"),
}


def get_item(item_name):
    """Get an item from the database by name."""
    return ITEMS_DATABASE.get(item_name.lower())


def create_item(item_name):
    """Create a copy of an item from the database."""
    item = get_item(item_name)
    if item:
        if isinstance(item, Weapon):
            return Weapon(item.name, item.description, item.damage, item.value, item.rarity)
        elif isinstance(item, Armor):
            return Armor(item.name, item.description, item.defense, item.value, item.rarity)
        elif isinstance(item, Potion):
            return Potion(item.name, item.description, item.effect_type, item.effect_value, item.value, item.rarity)
        else:
            return Item(item.name, item.item_type, item.description, item.value, item.rarity)
    return None