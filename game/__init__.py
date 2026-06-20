"""
Multiplayer Text-Based Adventure Game Engine
A full-featured game with world exploration, combat, NPCs, and multiplayer support.
"""

__version__ = "1.0.0"
__author__ = "Adventure Game Dev"

from .engine import GameEngine
from .player import Player
from .world import World
from .items import Item, Inventory
from .combat import Combat

__all__ = [
    "GameEngine",
    "Player",
    "World",
    "Item",
    "Inventory",
    "Combat",
]