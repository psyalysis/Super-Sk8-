"""Display/window module."""

import config
import pygame

class Display:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(config.FONT_PATH, config.FONT_SIZE_SMALL)
        self.debug_text_position = (10, 10) 
        
    def clear_screen(self):
        """
        Clears the entire screen by filling it with the background color,
        ensuring no previous elements remain before the next frame is drawn.
        """
        self.screen.fill(config.COLORS['background'])
        
    def draw_scene(self):
        """
        Draw everything on the screen. This includes:
        - Black background
        - Level/World
        - Skateboard (in correct anim frame)
        - Obstacles
        - UI elements
        """
        #self.clear_screen()
        self.draw_level()
        self.draw_skateboard()
        self.draw_obstacles()
        self.draw_ui()
        
    def draw_level(self):
        """
        Draw the level/world.
        """
        
        
    def draw_skateboard(self):
        """
        Draw the skateboard.
        """
        pass
        
    def draw_obstacles(self):
        """
        Draw the obstacles.
        """
        pass
        
    def draw_ui(self):
        """
        Draw the UI elements.
        """
        pass
    
    def draw_debug(self, info):
        """
        Draw the debug information for testing purposes.
        Info will be a 2 string list in the format: [Message, Type]
        Type can be: "success", "danger", "warning", "info"
        """
        
        #Set the color of the text based on the type
        if info[1] == "success":
            color = config.COLORS['success']
        elif info[1] == "danger":
            color = config.COLORS['danger']
        elif info[1] == "warning":
            color = config.COLORS['warning']
        else:
            color = config.COLORS['info']
        
        #Draw the text
        text = self.font.render(info[0], True, color)
        self.screen.blit(text, self.debug_text_position)
        
    def update(self):
        self.clear_screen()
        self.draw_scene()
        if config.DEBUG_TEXT_VISIBLE:
            self.draw_debug(config.DEBUG_TEXT)
        pygame.display.flip()