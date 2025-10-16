"""Display/window module."""

import config
import pygame

class Display:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(config.FONT_PATH, config.FONT_SIZE_SMALL)
        self.debug_text_position = (10, 10) 
        self.skateboard_sprite = None
        # Position skateboard over middle of tiles on left side of window
        # Based on tile positioning: px = ((rows * 16 - y * 16) * zoom) - 150, py = (rows * 8 + y * 8) * zoom
        # With zoom=2, positioning at left side center of tile area
        self.skateboard_position = (200, 300)
        self.skateboard_angle = 0
        self.load_skateboard_sprite()
    
    def load_skateboard_sprite(self):
        """
        Load the skateboard sprite from file.
        """
        
        skateboard_path = "./animations/default.png"
        self.skateboard_sprite = pygame.image.load(skateboard_path)
        
        # Scale skateboard to match level resolution using camera zoom
        original_width, original_height = self.skateboard_sprite.get_size()
        scaled_size = (int(original_width * config.CAMERA_ZOOM), int(original_height * config.CAMERA_ZOOM))
        self.skateboard_sprite = pygame.transform.scale(self.skateboard_sprite, scaled_size)
        

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

        self.draw_skateboard()
        #self.draw_obstacles()
        
        
    def draw_skateboard(self):
        
        self.screen.blit(self.skateboard_sprite, self.skateboard_position)
        
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