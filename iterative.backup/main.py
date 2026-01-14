""" Main module for Super-Sk8! game. """

# Importing libraries and modules
import pygame

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

    def run(self):
        # Main game loop
        while self.running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    self.control.handle_keydown(key)

                elif event.type == pygame.KEYUP:
                    key = event.key
                    self.control.handle_keyup(key)

if __name__ == "__main__":
    print("Starting game...")
    main = Main() # Initialize the game
    print("Game initialized")

    print("Running game loop...")
    main.run() # Run the game loop
    print("Game exited")