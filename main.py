"""Main module for the skateboard game."""

import pygame
import display
import level
import control
import ui
import debug
from core.state_manager import StateManager
from core.input_handler import InputHandler
from core.resource_manager import ResourceManager
from core.sound_manager import SoundManager

# Display settings
DISPLAY_WIDTH = 1100
DISPLAY_HEIGHT = 750
FPS = 60



class Main:
    def __init__(self):
        self.running = True
        
        pygame.init()
        
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Super Sk8!")
        self.clock = pygame.time.Clock()

        # Initialize core systems
        self.state_manager = StateManager()
        self.input_handler = InputHandler()
        self.resource_manager = ResourceManager()
        self.sound_manager = SoundManager()
        
        # Preload animations
        self.resource_manager.preload_animation_frames("assets/animations/flip/")
        self.resource_manager.preload_animation_frames("assets/animations/grind/")
        
        # Initialize game modules
        self.display = display.Display(self.screen, self.resource_manager)
        self.debug = debug.Debug()
        self.level = level.Level(self.display, self.resource_manager, self.state_manager)
        self.display.level = self.level
        self.ui = ui.UI(self.display)
        self.control = control.Control(self.display, self.state_manager, self.input_handler, self.debug, self.ui, self.sound_manager, self.level)

    def run(self):
        self.display.clear_screen()
        
        while self.running:
            self.clock.tick(FPS)
            
            # Process events (keypresses and exits)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    input_data = self.input_handler.process_key_down(event.key)
                    if input_data:
                        self.control.handle_input(input_data)
                elif event.type == pygame.KEYUP:
                    input_data = self.input_handler.process_key_up(event.key)
                    if input_data:
                        self.control.handle_input(input_data)
            
            # Update systems
            self.input_handler.update()
            self.control.update()
            
            # Render
            self.display.clear_screen()
            self.level.update_camera()
            self.level.draw_level()
            self.display.draw_scene()
            
            # Draw appropriate UI elements
            if self.state_manager.is_in_menu():
                self.ui.draw_menu()
            else:
                self.ui.draw_hud()
            
            self.ui.draw_trick_display()
            
            pygame.display.update()
        
        self.exit()
        
    def exit(self):
        self.running = False
        self.resource_manager.cleanup()
        self.sound_manager.cleanup()
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.run()
    print("Game exited")
