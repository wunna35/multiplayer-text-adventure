#!/usr/bin/env python3
"""
Multiplayer Client
Connects to the multiplayer server.
"""

import socket
import sys

class GameClient:
    """Multiplayer game client."""
    
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        
    def connect(self):
        """Connect to the server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"[CLIENT] Connected to {self.host}:{self.port}\n")
            return True
        except Exception as e:
            print(f"[ERROR] Could not connect: {e}")
            return False
    
    def start(self):
        """Start the game client."""
        if not self.connect():
            return
        
        try:
            # Game loop
            while True:
                try:
                    # Receive message from server
                    message = self.socket.recv(1024).decode()
                    if not message:
                        break
                    
                    print(message, end='')
                    
                    # Send player input
                    user_input = input()
                    if user_input.lower() == "quit":
                        self.socket.sendall(b"quit")
                        break
                    
                    self.socket.sendall(user_input.encode())
                
                except socket.timeout:
                    continue
        
        except KeyboardInterrupt:
            print("\n[CLIENT] Disconnecting...")
        
        finally:
            self.socket.close()
            print("[CLIENT] Disconnected.")


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    
    client = GameClient(host, port)
    client.start()