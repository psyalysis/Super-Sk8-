""" Main module for Super-Sk8! game. """

# Importing libraries and modules
import pygame
import time

import graphics
import level
import control
import tricks
import config


class Main:
    def __init__(self):
        # Set game running state
        self.running = True

        # Initialize pygame
        pygame.init()

        # Create game window
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Super-Sk8!")

        # Initialize modules
        self.control = control.Control()
        self.graphics = graphics.Graphics(self.screen)

        self.player = {
            "isAirborne": False,
            "currentTrick": {
                "name": None,
                "duration": 0,
                "startTime": 0,
                "endTime": 0
            }
        }

    def update(self):
        """Update game state - called once per frame."""
        # Get current input state
        trickFound = self.control.check_trick_input(self.player)

        # Handle game logic based on state
        if trickFound != None:
            if not self.player["isAirborne"]:
                self.start_trick(trickFound)
            elif self.player["currentTrick"]["name"] != trickFound:
                # Different trick while airborne - ignore
                pass
        else:
            if self.player["isAirborne"]:
                self.land()
        
        # Update level/physics
        self.level.update(self.player)

    def start_trick(self, trick_name):
        """Start a trick."""
        if not self.player["isAirborne"]:
            self.player["isAirborne"] = True
            self.player["currentTrick"]["name"] = trick_name
            self.player["currentTrick"]["startTime"] = time.time()
            self.player["currentTrick"]["endTime"] = 0
            print(f"Started trick: {trick_name}")

    def land(self):
        """Land from a trick."""
        if self.player["isAirborne"]:
            self.player["isAirborne"] = False
            self.player["currentTrick"]["endTime"] = time.time()
            trick_name = self.player['currentTrick']['name']
            print(f"Landed from trick: {trick_name}")
        
    def run(self):
        # Main game loop
        while self.running:
            # Process all events first
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.control.handle_keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.control.handle_keyup(event.key)
            
            # Update game state once per frame
            self.update()
            
            # Draw once per frame
            self.graphics.draw(self.player)


if __name__ == "__main__":
    print("Starting game...")
    main = Main()  # Initialize the game
    print("Game initialized")

    print("Running game loop...")
    main.run()  # Run the game loop
    print("Game exited")