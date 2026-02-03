import pygame
import sys

import config
from level import Level
from player import Player
from input import Input
from graphics import Graphics


class Main:
    """Core game engine managing initialization, game loop, and shutdown."""

    def __init__(self):
        """Initialize pygame and core game components."""
        pygame.init()

        self._setup_display()
        self._setup_timing()
        self._initialize_components()

        self.is_running = True

    def _setup_display(self):
        """Configure pygame display settings."""
        self.screen = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        pygame.display.set_caption("Super-Sk8!")

    def _setup_timing(self):
        """Initialize timing and clock for delta time calculations."""
        self.clock = pygame.time.Clock()
        self.dt = 0  # Delta time in seconds

    def _initialize_components(self):
        """Create and initialize game components."""
        self.level = Level(self.screen)
        self.player = Player()
        self.input = Input()
        self.graphics = Graphics(self.screen)

    def _process_events(self):
        """Handle system events and delegate input to input handler."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.input.handle_input(event)

    def _update(self):
        """Update game state and physics."""
        active_trick = self.input.get_active_trick()
        active_grind = self.input.get_active_grind()

        self.level.update(self.dt)
        self.player.update(self.dt, active_trick, active_grind, self.level)
        self.graphics.update(self.dt, self.player)

    def _draw(self):
        """Render the current frame."""
        self.screen.fill((30, 30, 30))

        self.level.draw()
        self.graphics.draw_player(self.player)

        pygame.display.flip()

    def run(self):
        """Execute the main game loop."""
        print("Super-Sk8! engine started.")

        while self.is_running:
            self.dt = self.clock.tick(config.FPS) / 1000.0

            self._process_events()
            self._update()
            self._draw()

        self._shutdown()

    def _shutdown(self):
        """Clean up resources and exit the game."""
        print("Shutting down...")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Main()
    game.run()