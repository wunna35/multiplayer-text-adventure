"""
World and Location System
Defines the game world, locations, NPCs, and items.
"""

class Location:
    """Represents a location in the game world."""
    
    def __init__(self, name, description, exits=None, items=None, npcs=None, enemies=None):
        self.name = name
        self.description = description
        self.exits = exits or {}  # {"north": "location_name", "south": "location_name"}
        self.items = items or []  # Items available in this location
        self.npcs = npcs or []  # NPCs in this location
        self.enemies = enemies or []  # Enemies in this location
        self.players = []  # Players currently in this location
        
    def get_full_description(self):
        """Get detailed description including items, NPCs, and enemies."""
        desc = f"=== {self.name} ===\n{self.description}\n"
        
        if self.items:
            desc += f"\nItems here: {', '.join([item.name for item in self.items])}"
        
        if self.npcs:
            desc += f"\nNPCs: {', '.join([npc.name for npc in self.npcs])}"
        
        if self.enemies:
            desc += f"\nEnemies: {', '.join([enemy.name for enemy in self.enemies])}"
        
        if self.exits:
            exits_str = ", ".join(self.exits.keys())
            desc += f"\n\nExits: {exits_str}"
        
        return desc
    
    def add_item(self, item):
        """Add an item to the location."""
        self.items.append(item)
    
    def remove_item(self, item):
        """Remove an item from the location."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def add_player(self, player):
        """Add a player to this location."""
        if player not in self.players:
            self.players.append(player)
    
    def remove_player(self, player):
        """Remove a player from this location."""
        if player in self.players:
            self.players.remove(player)


class World:
    """Represents the entire game world."""
    
    def __init__(self):
        self.locations = {}
        self.setup_world()
    
    def setup_world(self):
        """Initialize all locations in the world."""
        
        # Town Square - Starting location
        town_square = Location(
            "Town Square",
            "You stand in the center of a bustling town. Merchants sell their wares,\n"
            "and the smell of fresh bread fills the air. A fountain sits in the middle\n"
            "of the square, and several paths lead in different directions.",
            exits={"north": "forest", "east": "market", "south": "inn", "west": "blacksmith"},
        )
        self.locations["town_square"] = town_square
        
        # Forest - Monster hunting area
        forest = Location(
            "Enchanted Forest",
            "You enter a dense forest with towering trees. Sunlight barely pierces\n"
            "the canopy above. You hear strange sounds echoing through the trees.\n"
            "This is a dangerous place.",
            exits={"south": "town_square", "north": "mountain_pass", "east": "river"},
        )
        self.locations["forest"] = forest
        
        # Market
        market = Location(
            "Market Square",
            "A vibrant market filled with exotic goods from distant lands.\n"
            "Merchants call out their wares from colorful stalls.",
            exits={"west": "town_square", "north": "tower", "east": "harbor"},
        )
        self.locations["market"] = market
        
        # Inn
        inn = Location(
            "The Sleeping Dragon Inn",
            "A warm and welcoming inn with a cozy fireplace. The smell of ale\n"
            "and hearty food fills your nostrils. Several travelers gather at tables.",
            exits={"north": "town_square", "east": "tavern"},
        )
        self.locations["inn"] = inn
        
        # Blacksmith
        blacksmith = Location(
            "Blacksmith's Forge",
            "A hot and dusty forge. The sound of a hammer striking steel rings out.\n"
            "Weapons and armor hang on the walls. The blacksmith eyes you curiously.",
            exits={"east": "town_square"},
        )
        self.locations["blacksmith"] = blacksmith
        
        # Mountain Pass - Dangerous area
        mountain_pass = Location(
            "Mountain Pass",
            "A treacherous mountain path with steep cliffs on either side.\n"
            "The wind howls fiercely. You spot a cave entrance nearby.",
            exits={"south": "forest", "west": "cave", "east": "peak"},
        )
        self.locations["mountain_pass"] = mountain_pass
        
        # Cave - Boss area
        cave = Location(
            "Dark Cave",
            "You enter a dark, musty cave. Your torch flickers in the cold air.\n"
            "Strange markings cover the walls. You feel an ominous presence.",
            exits={"east": "mountain_pass"},
        )
        self.locations["cave"] = cave
        
        # Peak - High area
        peak = Location(
            "Mountain Peak",
            "You stand atop the mountain. The view is breathtaking - you can see\n"
            "the entire kingdom spread before you. The air is thin and cold.",
            exits={"west": "mountain_pass", "south": "river"},
        )
        self.locations["peak"] = peak
        
        # River
        river = Location(
            "Riverside",
            "A peaceful river flows gently through a grassy meadow.\n"
            "The water is clear and refreshing. Fish jump in the stream.",
            exits={"west": "forest", "north": "peak", "east": "market"},
        )
        self.locations["river"] = river
        
        # Tower - Magic area
        tower = Location(
            "Wizard's Tower",
            "An impressive tower of stone and magic. Strange symbols glow on the walls.\n"
            "Bookshelves line every surface, filled with ancient tomes of knowledge.",
            exits={"south": "market", "down": "tower_basement"},
        )
        self.locations["tower"] = tower
        
        # Tower Basement - Treasure area
        tower_basement = Location(
            "Tower Basement",
            "A dark basement beneath the tower. Ancient artifacts and treasure\n"
            "fill the shelves. You hear the sound of dripping water.",
            exits={"up": "tower"},
        )
        self.locations["tower_basement"] = tower_basement
        
        # Harbor
        harbor = Location(
            "Harbor",
            "A busy harbor with ships coming and going. The smell of salt water\n"
            "fills the air. Sailors shout orders as they load cargo.",
            exits={"west": "market"},
        )
        self.locations["harbor"] = harbor
        
        # Tavern
        tavern = Location(
            "The Rusty Anchor Tavern",
            "A rowdy tavern filled with adventurers and travelers.\n"
            "The sound of laughter and clinking glasses fills the air.",
            exits={"west": "inn"},
        )
        self.locations["tavern"] = tavern
    
    def get_location(self, location_name):
        """Get a location by name."""
        return self.locations.get(location_name.lower())
    
    def get_all_locations(self):
        """Get all locations in the world."""
        return list(self.locations.values())
    
    def display_map(self):
        """Display a simple map of the world."""
        map_str = """
        ╔════════════════════════════════════════╗
        ║    WORLD MAP                           ║
        ╠════════════════════════════════════════╣
        ║                    PEAK                ║
        ║                     |                  ║
        ║  CAVE -- MOUNTAIN PASS -- RIVER        ║
        ║           |                  |         ║
        ║        FOREST ----------- MARKET -- HARBOR
        ║           |                  |        ║
        ║     TOWN SQUARE -------- TOWER        ║
        ║      |    |                 |         ║
        ║    INN  BLACKSMITH     TOWER BASE      ║
        ║      |                                 ║
        ║    TAVERN                              ║
        ║                                        ║
        ╚════════════════════════════════════════╝
        """
        return map_str