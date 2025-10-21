"""Main module for the skateboard game."""

import pygame
import config
import display
import level
import control
import ui
import debug
from core.state_manager import StateManager
from core.input_handler import InputHandler
from core.resource_manager import ResourceManager



class Main:
    def __init__(self):
        self.running = True
        
        pygame.init()
        self.screen = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        pygame.display.set_caption("Super-Sk8!")
        self.clock = pygame.time.Clock()

        # Initialize core systems
        self.state_manager = StateManager()
        self.input_handler = InputHandler()
        self.resource_manager = ResourceManager()
        
        # Preload animation frames for better performance
        self.resource_manager.preload_animation_frames(config.ANIMATIONS)
        
        # Initialize game modules
        self.display = display.Display(self.screen, self.resource_manager)
        self.debug = debug.Debug()
        self.level = level.Level(self.display, self.resource_manager)
        self.ui = ui.UI(self.display)
        self.control = control.Control(self.display, self.state_manager, self.input_handler, self.debug, self.ui)

    def run(self):
        self.display.clear_screen()
        
        while self.running:
            frame_start = pygame.time.get_ticks()
            self.clock.tick(config.FPS)
            
            # Process events
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
            self.level.draw_level()
            self.level.update_camera()
            self.display.draw_scene()
            
            if self.state_manager.is_in_menu():
                self.ui.draw_menu()
            
            # Draw trick display
            self.ui.draw_trick_display()
            
            pygame.display.update()
            
        
        self.exit()
        
    def exit(self):
        self.running = False
        self.resource_manager.cleanup()
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    
    try:
        main.run()
    except Exception as e:
        print(f"Game error: {e}")
        
    main.exit()
    print("Game exited")
    