"""Display/window module."""

import config
import pygame


class Display:
    def __init__(self, screen, resource_manager):
        self.screen = screen
        self.resource_manager = resource_manager
        self.font = self.resource_manager.load_font(config.FONT_PATH, config.FONT_SIZE_SMALL)
        self.debug_text_position = (10, 10) 
        self.skateboard_sprite = None
        self.level = None  # Will be set by main.py
        
        # Animation system
        self.current_animation = None
        self.current_trick = None
        self.animation_frames = []
        self.animation_frame = 0
        self.animation_running = False
        self.animation_loop = False
        self.last_frame_time = 0
        self.base_frame_duration = (1000 / config.ANIMATION_FRAME_RATE) / 2
        self.frame_duration = self.base_frame_duration
        self.frame_rate_limit = True  # Enable frame rate limiting
        self.max_frame_time = 1000 / 60  # Cap at 60 FPS
        
        # Calculate skateboard position based on screen size
        self.skateboard_base_position = (
            int(200 * config.SCALE_FACTOR),
            int(250 * config.SCALE_FACTOR)
        )
        self.load_skateboard_sprite()
    
    def load_skateboard_sprite(self):
        skateboard_path = "./animations/Default.png"
        self.skateboard_sprite = self.resource_manager.load_texture(skateboard_path, config.CAMERA_ZOOM)

    def clear_screen(self):
        self.screen.fill(config.COLORS['background'])
        
    def draw_scene(self):
        self.draw_skateboard()
        
    def draw_skateboard(self):
        if self.animation_running and self.current_animation and self.animation_frames:
            trick_position = (
                self.skateboard_base_position[0], 
                self.skateboard_base_position[1] - int(50 * config.SCALE_FACTOR)
            )
            
            current_time = pygame.time.get_ticks()
            time_since_last_frame = current_time - self.last_frame_time
            
            # Update animation frame if enough time has passed
            if time_since_last_frame >= self.frame_duration:
                if self.animation_loop:
                    self.animation_frame = (self.animation_frame + 1) % len(self.animation_frames)
                else:
                    if self.animation_frame < len(self.animation_frames) - 1:
                        self.animation_frame += 1
                    else:
                        self.stop_animation()
                        return
                self.last_frame_time = current_time
            
            # Always draw the current frame, regardless of frame rate limiting
            current_sprite = self.animation_frames[self.animation_frame]
            self.screen.blit(current_sprite, trick_position)
        else:
            # Skateboard stays in fixed screen position (in front of scrolling level)
            self.screen.blit(self.skateboard_sprite, self.skateboard_base_position)
        
    def start_animation(self, trick_name, animation_sprite, loop=False):
        self.current_trick = trick_name
        self.current_animation = animation_sprite
        
        self.set_trick_speed(trick_name)
        
        # Use cached frames instead of extracting each time
        self.animation_frames = self.resource_manager.get_animation_frames(trick_name)
        self.animation_frame = 0
        self.animation_running = True
        self.animation_loop = loop
        self.last_frame_time = pygame.time.get_ticks()
    
    
    def set_trick_speed(self, trick_name):
        self.frame_duration = self.base_frame_duration
        
        flip_tricks = ["Kickflip", "Heelflip"]
        shuv_tricks = ["BS-Shuv", "FS-Shuv"]
        double_shuv_tricks = ["Tre Flip", "Lazer Flip", "360 Hardflip", "360 Inward Heelflip"]
        varial_tricks = ["Varial Kickflip", "Varial Heelflip", "Inward Heelflip", "Hardflip"]

        if trick_name in flip_tricks:
            self.frame_duration *= 1
        elif trick_name in shuv_tricks:
            self.frame_duration *= 0.75
        elif trick_name in double_shuv_tricks:
            self.frame_duration *= 1.5
        elif trick_name in varial_tricks:
            self.frame_duration *= 1.2
    
    def stop_animation(self):
        self.animation_running = False
        self.current_animation = None
        self.current_trick = None
        self.animation_frames = []
        self.animation_frame = 0
    
    def set_frame_rate_limit(self, enabled, max_fps=60):
        """Enable/disable frame rate limiting for animations."""
        self.frame_rate_limit = enabled
        self.max_frame_time = 1000 / max_fps if enabled else 0

    def draw_debug(self, info):
        if info[1] == "success":
            color = config.COLORS['success']
        elif info[1] == "danger":
            color = config.COLORS['danger']
        elif info[1] == "warning":
            color = config.COLORS['warning']
        else:
            color = config.COLORS['info']
        
        text = self.font.render(info[0], True, color)
        self.screen.blit(text, self.debug_text_position)