#!/usr/bin/env python3
"""
Multiplayer Server
Handles multiple player connections and synchronizes game state.
"""

import socket
import threading
import json
import uuid
from game.engine import GameEngine
from game.player import Player

class GameServer:
    """Multiplayer game server."""
    
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.engine = GameEngine()
        self.players = {}  # player_id -> Player object
        self.client_threads = {}  # player_id -> thread
        self.server_socket = None
        self.running = False
        
    def start(self):
        """Start the server."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"\n[SERVER] Starting on {self.host}:{self.port}")
        print("[SERVER] Waiting for players...\n")
        
        try:
            while self.running:
                client_socket, address = self.server_socket.accept()
                player_id = str(uuid.uuid4())
                print(f"[CONNECTION] Player {player_id} connected from {address}")
                
                thread = threading.Thread(
                    target=self.handle_player,
                    args=(client_socket, player_id, address),
                    daemon=True
                )
                thread.start()
                self.client_threads[player_id] = thread
        
        except KeyboardInterrupt:
            print("\n[SERVER] Shutting down...")
            self.stop()
    
    def handle_player(self, client_socket, player_id, address):
        """Handle a single player connection."""
        try:
            # Receive player name
            client_socket.sendall(b"Enter your character name: ")
            player_name = client_socket.recv(1024).decode().strip()
            
            if not player_name:
                player_name = f"Player{player_id[:8]}"
            
            # Create player
            player = Player(player_name)
            player.player_id = player_id
            self.players[player_id] = player
            
            # Send welcome message
            welcome = f"Welcome, {player_name}! Type 'help' for commands.\n"
            client_socket.sendall(welcome.encode())
            
            # Game loop for this player
            while self.running:
                try:
                    command = client_socket.recv(1024).decode().strip()
                    if not command:
                        continue
                    
                    if command.lower() == "quit":
                        break
                    
                    # Process command using game engine
                    response = self.process_player_command(player_id, command)
                    client_socket.sendall((response + "\n").encode())
                
                except socket.timeout:
                    continue
        
        except Exception as e:
            print(f"[ERROR] Player {player_id}: {e}")
        
        finally:
            print(f"[DISCONNECT] Player {player_id} disconnected")
            if player_id in self.players:
                del self.players[player_id]
            client_socket.close()
    
    def process_player_command(self, player_id, command):
        """Process a command from a player."""
        player = self.players.get(player_id)
        if not player:
            return "Error: Player not found."
        
        # For now, just return a basic response
        # In a real implementation, you'd integrate with the game engine
        cmd = command.lower().split()[0]
        
        if cmd == "status":
            return player.display_status()
        elif cmd == "players":
            player_list = "\n".join([f"- {p.name} (Level {p.level})" for p in self.players.values()])
            return f"Players online:\n{player_list}"
        else:
            return f"Server received: {command}"
    
    def stop(self):
        """Stop the server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("[SERVER] Stopped.")


if __name__ == "__main__":
    server = GameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        server.stop()