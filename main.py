import pygame
import sys

import config
from level import Level
from player import Player
from input import Input
from graphics import Graphics
from tricks import Tricks
from sound import Sound

class Main:
    """Main game loop and component setup."""

    def __init__(self):
        pygame.init()

        self._setup_display()
        self._setup_timing()
        self._initialize_components()

        self.is_running = True

        self.score = 0

    def _setup_display(self):
        self.screen = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        pygame.display.set_caption("Super-Sk8!")

    def _setup_timing(self):
        self.clock = pygame.time.Clock()
        self.dt = 0

    def _initialize_components(self):
        self.level = Level(self.screen)
        self.player = Player(Sound())
        self.input = Input()
        self.graphics = Graphics(self.screen)
        self.tricks = Tricks(Sound(), self.graphics)

    def _process_events(self):
        """Handle Every Event that happened since this function was last called."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.input.handle_input(event)

    def _update(self):
        """Update Each of the Components in order"""
        active_trick = self.input.get_active_trick()
        active_grind = self.input.get_active_grind()

        self.level.update(self.dt)
        self.player.update(self.dt, active_trick, active_grind, self.level, self.tricks, self.graphics)
        self.score = self.tricks.update(self.dt)
        self.graphics.update(self.dt, self.player, self.score)

    def _draw(self):
        """Draw the current frame to the screen (From Back to Front)"""
        self.screen.fill((30, 30, 30)) # Clear the screen with a dark grey color

        self.level.draw() # Draw the level (Background)
        self.graphics.draw_player(self.player) # Draw the player
        self.graphics.draw_trick_display() # Draw the trick display
        self.graphics.draw_score(int(self.score)) # Draw the score

        pygame.display.flip() # Update the screen

    def run(self):
        """Main game loop"""
        while self.is_running:
            self.dt = self.clock.tick(config.FPS) / 1000.0 # Self.dt is the "Delta Time" (Seconds since last frame) to coordinate and sync the game

            self._process_events()
            self._update()
            self._draw()

        self._shutdown()

    def _shutdown(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Main()
    game.run()