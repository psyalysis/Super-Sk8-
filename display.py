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
        
        self.skateboard_base_position = (200, 300)
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
            trick_position = (self.skateboard_base_position[0], self.skateboard_base_position[1] - 50)
            
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_duration:
                if self.animation_loop:
                    self.animation_frame = (self.animation_frame + 1) % len(self.animation_frames)
                else:
                    if self.animation_frame < len(self.animation_frames) - 1:
                        self.animation_frame += 1
                    else:
                        self.stop_animation()
                        return
                self.last_frame_time = current_time
            
            current_sprite = self.animation_frames[self.animation_frame]
            self.screen.blit(current_sprite, trick_position)
        else:
            self.screen.blit(self.skateboard_sprite, self.skateboard_base_position)
        
    def start_animation(self, trick_name, animation_sprite, loop=False):
        self.current_trick = trick_name
        self.current_animation = animation_sprite
        
        self.set_trick_speed(trick_name)
        
        self.animation_frames = self.extract_frames_from_spritemap(animation_sprite)
        self.animation_frame = 0
        self.animation_running = True
        self.animation_loop = loop
        self.last_frame_time = pygame.time.get_ticks()
    
    def extract_frames_from_spritemap(self, spritemap):
        frames = []
        
        spritemap_width, spritemap_height = spritemap.get_size()
        estimated_frame_width = spritemap_height
        estimated_frame_count = spritemap_width // estimated_frame_width
        
        for i in range(estimated_frame_count):
            frame_x = i * estimated_frame_width
            frame_y = 0
            frame_width = estimated_frame_width
            frame_height = spritemap_height
            
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(spritemap, (0, 0), (frame_x, frame_y, frame_width, frame_height))
            
            original_width, original_height = frame_surface.get_size()
            scaled_size = (int(original_width * config.CAMERA_ZOOM), int(original_height * config.CAMERA_ZOOM))
            scaled_frame = pygame.transform.scale(frame_surface, scaled_size)
            
            frames.append(scaled_frame)
        
        return frames
    
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