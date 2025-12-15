"""Display/window module."""

import pygame

# Hardcoded display settings
FONT_PATH = "assets/ui/ari-w9500.ttf"
FONT_SIZE_SMALL = 16
CAMERA_ZOOM = 1.25
SKATEBOARD_OFFSET_X = 150
SKATEBOARD_OFFSET_Y = 165
ANIMATION_FRAME_RATE = 30
FPS = 60
GRIND_SPEED = 1.0

COLORS = {
    'background': (0, 0, 0),
    'white': (236, 240, 241),
    'black': (22, 22, 22),
    'gray': (127, 140, 141),
    'success': (39, 174, 96),
    'danger': (192, 57, 43),
    'warning': (241, 196, 15),
}

FLIP_SPEEDS = {
    "Kickflip": 1.5,
    "Heelflip": 1.5,
    "Varial Kickflip": 1.75,
    "Varial Heelflip": 1.75,
    "Hardflip": 1.85,
    "Inward Heelflip": 1.85,
    "BS-Shuv": 1.7,
    "FS-Shuv": 1.7,
    "360 Hardflip": 1.8,
    "360 Inward Heelflip": 1.8,
    "Tre Flip": 1.4,
    "Lazer Flip": 1.4,
}


class Display:
    def __init__(self, screen, resource_manager):
        self.screen = screen
        self.resource_manager = resource_manager
        self.font = self.resource_manager.load_font(FONT_PATH, FONT_SIZE_SMALL)
        self.debug_text_position = (10, 10)
        self.skateboard_sprite = None
        self.skateboard_green_sprite = None
        self.skateboard_red_sprite = None
        self.explode_sprite = None
        self.level = None
        self.skateboard_visible = False
        self.explode_visible = False
        
        # Board color feedback
        self.board_color_timer = 0
        self.board_color_timer_start = 0
        self.board_color_duration = 200
        self.board_color_type = None
        
        # Animation system
        self.current_animation = None
        self.current_trick = None
        self.animation_frames = []
        self.animation_frame = 0
        self.animation_running = False
        self.animation_loop = False
        self.last_frame_time = 0
        self.frame_duration = 1000 / ANIMATION_FRAME_RATE
        
        # Skateboard position
        self.skateboard_base_position = (SKATEBOARD_OFFSET_X, SKATEBOARD_OFFSET_Y)
        self.trick_jump_height = 50
        
        self.load_skateboard_sprite()
        self.load_explode_sprite()
    
    def load_skateboard_sprite(self):
        self.skateboard_sprite = self.resource_manager.load_texture("./assets/animations/Default.png", CAMERA_ZOOM * 2)
        self.skateboard_green_sprite = self.resource_manager.load_texture("./assets/animations/DefaultGreen.png", CAMERA_ZOOM * 2)
        self.skateboard_red_sprite = self.resource_manager.load_texture("./assets/animations/DefaultRed.png", CAMERA_ZOOM * 2)
    
    def load_explode_sprite(self):
        self.explode_sprite = self.resource_manager.load_texture("./assets/animations/Explode.png", CAMERA_ZOOM * 2)

    def clear_screen(self):
        self.screen.fill(COLORS['background'])
    
    def draw_scene(self):
        self.update_board_color_timer()
        
        if self.skateboard_visible:
            self.draw_skateboard()
        if self.explode_visible and self.explode_sprite:
            self.draw_explode_animation()
    
    def draw_skateboard(self):
        pad_height_offset = -10 if (self.level and self.level.get_current_chunk_type() == 'pad') else 0
        
        if self.animation_running and self.current_animation and self.animation_frames:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_duration:
                if self.animation_loop:
                    self.animation_frame = (self.animation_frame + 1) % len(self.animation_frames)  # Simplified: Removed cached_frame_count, use len() directly
                else:
                    if self.animation_frame < len(self.animation_frames) - 1:
                        self.animation_frame += 1
                    else:
                        self.stop_animation()
                        return
                self.last_frame_time = current_time
            
            current_sprite = self.animation_frames[self.animation_frame]
            position = (
                self.skateboard_base_position[0],
                self.skateboard_base_position[1] - self.trick_jump_height + pad_height_offset
            )
            self.screen.blit(current_sprite, position)
        else:
            sprite_to_use = self.get_board_sprite()
            position = (
                self.skateboard_base_position[0],
                self.skateboard_base_position[1] + pad_height_offset
            )
            self.screen.blit(sprite_to_use, position)
    
    def draw_explode_animation(self):
        if self.animation_running and self.current_trick == "Explode" and self.animation_frames:
            pad_height_offset = -10 if (self.level and self.level.get_current_chunk_type() == 'pad') else 0
            
            position = (
                self.skateboard_base_position[0],
                self.skateboard_base_position[1] + 30 + pad_height_offset
            )
            self.screen.blit(self.animation_frames[self.animation_frame], position)
    
    def start_animation(self, trick_name, animation_sprite, loop=False):
        self.current_trick = trick_name
        self.current_animation = animation_sprite
        self.set_trick_speed(trick_name)
        
        self.animation_frames = self.resource_manager.get_animation_frames(trick_name)
        # Fixed: Check if frames were loaded, if not try extracting from sprite directly
        if not self.animation_frames and animation_sprite:
            self.animation_frames = self.resource_manager.extract_animation_frames(animation_sprite, CAMERA_ZOOM * 2)
            if self.animation_frames:
                self.resource_manager.animation_frames_cache[trick_name] = self.animation_frames
        
        if not self.animation_frames:
            print(f"Warning: No animation frames found for {trick_name}")
            return
        
        self.animation_frame = 0
        self.animation_running = True
        self.animation_loop = loop
        self.last_frame_time = pygame.time.get_ticks()
    
    def set_trick_speed(self, trick_name):
        self.frame_duration = 1000 / ANIMATION_FRAME_RATE
        
        if trick_name in FLIP_SPEEDS:
            speed_multiplier = FLIP_SPEEDS.get(trick_name, 1.0)
        else:
            speed_multiplier = GRIND_SPEED
        
        self.frame_duration /= speed_multiplier
    
    def stop_animation(self):
        was_explode = self.current_trick == "Explode"
        self.animation_running = False
        self.current_animation = None
        self.current_trick = None
        self.animation_frames = []
        self.animation_frame = 0
        
        if was_explode:
            self.explode_visible = False

    def show_skateboard(self):
        self.skateboard_visible = True
        self.explode_visible = True
        self.start_animation("Explode", self.explode_sprite, loop=False)
    
    def hide_skateboard(self):
        self.skateboard_visible = False
        self.explode_visible = False
    
    def update_board_color_timer(self):  # Fixed: Corrected timer calculation (was using incorrect elapsed calculation)
        if self.board_color_timer > 0:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.board_color_timer_start
            remaining = max(0, self.board_color_duration - elapsed)
            self.board_color_timer = remaining
            if remaining <= 0:
                self.board_color_type = None
    
    def get_board_sprite(self):
        if self.board_color_type == 'green' and self.skateboard_green_sprite:
            return self.skateboard_green_sprite
        elif self.board_color_type == 'red' and self.skateboard_red_sprite:
            return self.skateboard_red_sprite
        return self.skateboard_sprite
    
    def show_board_color_feedback(self, color_type):
        self.board_color_type = color_type
        self.board_color_timer = self.board_color_duration
        self.board_color_timer_start = pygame.time.get_ticks()

    def draw_debug(self, info):
        color = COLORS.get(info[1], COLORS['success'])
        text = self.font.render(info[0], True, color)
        self.screen.blit(text, self.debug_text_position)
