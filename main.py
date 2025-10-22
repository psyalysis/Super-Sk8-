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
from core.sound_manager import SoundManager



class Main:
    def __init__(self):
        self.running = True
        
        try:
            pygame.init()
            # Use best available resolution
            width, height = config.BEST_RESOLUTION
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Super-Sk8!")
            self.clock = pygame.time.Clock()
            
            # Store actual screen dimensions
            self.screen_width = width
            self.screen_height = height

            # Initialize core systems
            self.state_manager = StateManager()
            self.input_handler = InputHandler()
            self.resource_manager = ResourceManager()
            self.sound_manager = SoundManager()
            
            # Preload animation frames for better performance
            try:
                self.resource_manager.preload_animation_frames(config.ANIMATIONS)
            except Exception as e:
                print(f"Warning: Failed to preload animations: {e}")
            
            # Pre-calculate common scaled textures
            try:
                self.resource_manager.precalculate_common_scaled_textures()
            except Exception as e:
                print(f"Warning: Failed to pre-calculate scaled textures: {e}")
            
            # Initialize game modules
            self.display = display.Display(self.screen, self.resource_manager)
            self.debug = debug.Debug()
            self.level = level.Level(self.display, self.resource_manager)
            self.display.level = self.level  # Set level reference for camera shake
            self.ui = ui.UI(self.display)
            self.control = control.Control(self.display, self.state_manager, self.input_handler, self.debug, self.ui, self.sound_manager)
            
        except Exception as e:
            print(f"Failed to initialize game: {e}")
            self.running = False

    def run(self):
        self.display.clear_screen()
        
        while self.running:
            try:
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
                self.level.update_camera()
                self.level.draw_level()
                self.display.draw_scene()
                
                if self.state_manager.is_in_menu():
                    self.ui.draw_menu()
                else:
                    # Draw HUD elements when in game
                    self.ui.draw_hud()
                
                # Draw trick display
                self.ui.draw_trick_display()
                
                pygame.display.update()
                
            except Exception as e:
                print(f"Runtime error: {e}")
                if self.debug:
                    self.debug.log_error(f"Runtime error: {e}")
                # Continue running despite errors
        
        self.exit()
        
    def exit(self):
        self.running = False
        try:
            self.resource_manager.cleanup()
            self.sound_manager.cleanup()
            pygame.quit()
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    main = Main()
    
    if main.running:  # Only run if initialization was successful
        try:
            main.run()
        except Exception as e:
            print(f"Game error: {e}")
            if main.debug:
                main.debug.log_error(f"Game error: {e}")
        
    main.exit()
    print("Game exited")
    