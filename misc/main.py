"""Main module for the skateboard game."""

import pygame
import config


class Main:
    def __init__(self):
        self.running = True
        
        try:
            pygame.init()
            
            width, height = config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT
            self.screen = pygame.display.set_mode((width, height))

            pygame.display.set_caption("Super Sk8!")
            self.clock = pygame.time.Clock()
            
            self.screen_width = width
            self.screen_height = height
            
        except Exception as e:
            print(f"Failed to initialize game: {e}")
            self.running = False

    def run(self):
        #Clear the screen at the start of each frame (This is what you usually do with the pygame library)
        self.display.clear_screen()
        
        while self.running:
            try:
                frame_start = pygame.time.get_ticks()
                self.clock.tick(config.FPS)
                
                # Handle all events
                for event in pygame.event.get():
                    
                    #Handle quit event
                    if event.type == pygame.QUIT:
                        self.running = False
                        
                    #Handle key down and up events
                    elif event.type == pygame.KEYDOWN:
                        pass
                    elif event.type == pygame.KEYUP:
                        pass
                
                # Update the pygame display
                pygame.display.update()
                
            except Exception as e:
                print(f"Runtime error: {e}")
                if self.debug:
                    self.debug.log_error(f"Runtime error: {e}")
        
        self.exit()
        
    def exit(self):
        self.running = False
        try:
            pygame.quit()
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    main = Main()
    
    if main.running:
        try:
            main.run()
        except Exception as e:
            print(f"Game error: {e}")
        
    main.exit()
    print("Game exited")
    