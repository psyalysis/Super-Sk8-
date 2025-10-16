"""Main module for the skateboard game."""

import pygame
import config
import display
import level
import control
import ui
import debug



class Main:
    def __init__(self):
        self.running = True
        
        self.game_state = "menu"
        self.player_state = "rolling"
        
        pygame.init()
        self.screen = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        pygame.display.set_caption("Super-Sk8!")
        
        self.clock = pygame.time.Clock()

        # --- Initialize the modules ---
        self.main = self
        self.display = display.Display(self.screen)
        self.debug = debug.Debug(self.main)
        self.level = level.Level(self.display, self.main)
        self.control = control.Control(self.display, self.main)
        self.ui = ui.UI(self.display)
        
        
        

    def run(self):
        
        self.display.clear_screen()
        
        while self.running:
            self.clock.tick(config.FPS) #Set the pygame clock to the FPS
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.control.handle_key_down(event.key, self.player_state)
                elif event.type == pygame.KEYUP:
                    self.control.handle_key_up(event.key, self.player_state)
            
            # Clear screen for next frame
            self.display.clear_screen()
            
            self.level.draw_level()
            self.level.update_camera()
            self.control.update()

            self.display.draw_scene()
            
            if self.game_state == "menu":
                self.ui.draw_menu()
            
            # Draw debug message if active
            if config.DEBUG_TEXT_VISIBLE:
                debug_msg = self.debug.get_current_message()
                if debug_msg:
                    self.display.draw_debug(debug_msg)
            
            pygame.display.update()
        self.exit()
        
    def exit(self):
        self.running = False
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    
    try:
        main.run()
    except Exception as e:
        print(e)
        
    main.exit()
    print("Game exited")
    