"""
Combat System
Handles turn-based combat between players and enemies.
"""

import random

class Enemy:
    """Represents an enemy creature."""
    
    def __init__(self, name, health, attack_power, defense, experience_reward, items_drop=None):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.experience_reward = experience_reward
        self.items_drop = items_drop or []
        self.is_alive = True
    
    def take_damage(self, damage):
        """Take damage and return remaining health."""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        if self.health <= 0:
            self.is_alive = False
        return self.health
    
    def attack(self):
        """Return attack power for this turn."""
        return self.attack_power + random.randint(-3, 3)
    
    def __str__(self):
        return f"{self.name} (HP: {self.health}/{self.max_health})"


class Combat:
    """Manages combat between a player and an enemy."""
    
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn_count = 0
        self.combat_log = []
    
    def start_combat(self):
        """Start the combat encounter."""
        self.player.in_combat = True
        self.player.current_enemy = self.enemy
        log = f"\n⚔️  Combat started!\nYou face {self.enemy.name}!\n"
        self.combat_log.append(log)
        return log
    
    def player_attack(self):
        """Player attacks the enemy."""
        if not self.player.is_alive() or not self.enemy.is_alive:
            return "Combat is not active!"
        
        player_damage = self.player.get_attack_power()
        enemy_health = self.enemy.take_damage(player_damage)
        
        log = f"\nYou attack {self.enemy.name} for {player_damage} damage!"
        if enemy_health > 0:
            log += f"\n{self.enemy.name} has {enemy_health}/{self.enemy.max_health} HP remaining."
        else:
            log += f"\n{self.enemy.name} is defeated!"
        
        self.combat_log.append(log)
        return log
    
    def enemy_attack(self):
        """Enemy attacks the player."""
        if not self.player.is_alive() or not self.enemy.is_alive:
            return ""
        
        enemy_damage = self.enemy.attack()
        player_health = self.player.take_damage(enemy_damage)
        
        log = f"\n{self.enemy.name} attacks you for {enemy_damage} damage!"
        if player_health > 0:
            log += f"\nYou have {player_health}/{self.player.max_health} HP remaining."
        else:
            log += f"\nYou have been defeated!"
        
        self.combat_log.append(log)
        return log
    
    def do_turn(self):
        """Execute one full combat turn."""
        if not self.player.is_alive() or not self.enemy.is_alive:
            return None
        
        self.turn_count += 1
        turn_log = f"\n=== Turn {self.turn_count} ===\n"
        
        # Player always goes first if they initiate combat
        turn_log += self.player_attack()
        
        if self.enemy.is_alive:
            turn_log += self.enemy_attack()
        
        return turn_log
    
    def is_combat_active(self):
        """Check if combat is still ongoing."""
        return self.player.is_alive() and self.enemy.is_alive
    
    def end_combat(self):
        """End the combat encounter."""
        self.player.in_combat = False
        self.player.current_enemy = None
        
        if self.player.is_alive():
            # Player won
            self.player.gain_experience(self.enemy.experience_reward)
            log = f"\n🎉 Victory! You gain {self.enemy.experience_reward} experience!\n"
            
            # Drop items
            if self.enemy.items_drop:
                log += f"The {self.enemy.name} drops:\n"
                for item in self.enemy.items_drop:
                    self.player.inventory.add_item(item)
                    log += f"  - {item.name}\n"
            
            self.combat_log.append(log)
            return log
        else:
            # Player lost
            log = "\n💀 You have been defeated... Game Over!\n"
            self.combat_log.append(log)
            return log
    
    def get_combat_log(self):
        """Get the full combat log."""
        return "".join(self.combat_log)


# Predefined enemies for the game
ENEMIES_DATABASE = {
    "goblin": Enemy("Goblin", 20, 5, 1, 50),
    "orc": Enemy("Orc", 40, 8, 2, 100),
    "troll": Enemy("Troll", 60, 10, 3, 150),
    "dragon": Enemy("Dragon", 150, 20, 5, 500),
    "skeleton": Enemy("Skeleton", 30, 6, 2, 75),
    "bandit": Enemy("Bandit", 35, 7, 2, 80),
    "spider": Enemy("Giant Spider", 25, 6, 1, 60),
    "wolf": Enemy("Dire Wolf", 45, 9, 2, 120),
}


def get_enemy(enemy_name):
    """Get an enemy from the database."""
    return ENEMIES_DATABASE.get(enemy_name.lower())


def create_enemy(enemy_name):
    """Create a copy of an enemy from the database."""
    enemy = get_enemy(enemy_name)
    if enemy:
        new_enemy = Enemy(
            enemy.name,
            enemy.max_health,
            enemy.attack_power,
            enemy.defense,
            enemy.experience_reward,
            enemy.items_drop.copy()
        )
        return new_enemy
    return None


def spawn_random_enemy():
    """Spawn a random enemy."""
    enemy_names = list(ENEMIES_DATABASE.keys())
    return create_enemy(random.choice(enemy_names))