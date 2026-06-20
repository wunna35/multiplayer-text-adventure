#!/usr/bin/env python3
"""
Multiplayer Text-Based Adventure Game - Single Player Mode
Run this file to play the game!
"""

from game.engine import GameEngine

def main():
    """Main game loop for single-player mode."""
    print("\n" + "="*50)
    print("  MULTIPLAYER TEXT-BASED ADVENTURE GAME")
    print("="*50)
    print("\nWelcome to the realm of adventure!\n")
    
    # Get player name
    player_name = input("Enter your character name: ").strip()
    if not player_name:
        player_name = "Adventurer"
    
    # Initialize game
    engine = GameEngine()
    print(engine.start_new_game(player_name))
    print("Type 'help' for a list of commands.\n")
    
    # Main game loop
    while engine.running:
        try:
            command = input("> ").strip()
            if command:
                response = engine.process_command(command)
                print(response)
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Thanks for playing!")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nGoodbye!")

if __name__ == "__main__":
    main()