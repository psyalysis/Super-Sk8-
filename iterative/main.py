import pygame
import sys
import config
from level import Level
from player import Player # Assuming you move player logic here
from input import Input

class Main:
    def __init__(self):
        """Initialize game engine and core components."""
        pygame.init()
        
        # 1. Display Setup
        self.screen = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        pygame.display.set_caption("Super-Sk8!")
        
        # 2. Timing & Synchronization
        self.clock = pygame.time.Clock()
        self.dt = 0 # Delta time: time passed since last frame
        
        # 3. Component Initialization
        # We pass 'self' or specific dependencies to allow modules to communicate
        self.level = Level(self.screen)
        self.player = Player() 
        self.input = Input()
        
        self.is_running = True

    def _process_events(self):
        """Handle system-level events (Quit, Resize) and delegate input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                
            # Delegate keyboard events to the input module
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.input.handle_input(event)

    def _update(self):
        """Update game physics and logic using delta time."""
        # Check for trick inputs from the controller
        active_trick = self.input.get_active_trick()
        
        # Update level (conveyor belt)
        self.level.update(self.dt)
        
        # Update player logic (physics, trick state, collisions)
        self.player.update(self.dt, active_trick, self.level)

    def _draw(self):
        """Render the current frame."""
        # Clear screen (Standard background color)
        self.screen.fill((30, 30, 30)) 
        
        # Draw layers in order (Background -> Level -> Player -> UI)
        self.level.draw()
        self.player.draw(self.screen)
        
        # Final buffer swap
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        print("Super-Sk8! engine started.")
        
        while self.is_running:
            # Calculate Delta Time (seconds passed since last frame)
            # This ensures the game runs at the same speed on all computers
            self.dt = self.clock.tick(config.FPS) / 1000.0
            
            self._process_events()
            self._update()
            self._draw()

        self._shutdown()

    def _shutdown(self):
        """Clean up resources before exiting."""
        print("Shutting down...")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Main()
    game.run()