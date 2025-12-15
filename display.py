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
        self.skateboard_green_sprite = None
        self.skateboard_red_sprite = None
        self.explode_sprite = None
        self.level = None
        self.skateboard_visible = False
        self.explode_visible = False
        
        # Board color feedback system
        self.board_color_timer = 0
        self.board_color_duration = 200  # 0.2 seconds in milliseconds
        self.board_color_type = None  # 'green', 'red', or None
        
        # Animation system
        self.current_animation = None
        self.current_trick = None
        self.animation_frames = []
        self.animation_frame = 0
        self.animation_running = False
        self.animation_loop = False
        self.last_frame_time = 0
        self.base_frame_duration = 1000 / config.ANIMATION_FRAME_RATE
        self.frame_duration = self.base_frame_duration
        self.frame_rate_limit = False
        self.max_frame_time = 1000 / 60
        
        # Calculate skateboard position based on screen size and config offset
        self.skateboard_base_position = (config.SKATEBOARD_OFFSET_X, config.SKATEBOARD_OFFSET_Y)
        
        # Pre-calculate animation positions for better performance
        self.trick_jump_height = 50
        self.cached_trick_position = (
            self.skateboard_base_position[0], 
            self.skateboard_base_position[1] - self.trick_jump_height
        )
        
        # Cache frame count to avoid repeated len() calls
        self.cached_frame_count = 0
        
        # Camera shake system
        self.camera_shake_x = 0.0
        self.camera_shake_y = 0.0
        self.shake_intensity = 0.0
        self.shake_duration = 0.0
        self.shake_timer = 0.0
        
        self.load_skateboard_sprite()
        self.load_explode_sprite()
    
    def load_skateboard_sprite(self):
        skateboard_path = "./assets/animations/Default.png"
        self.skateboard_sprite = self.resource_manager.load_texture(skateboard_path, config.CAMERA_ZOOM * 2)
        
        # Load colored versions
        green_path = "./assets/animations/DefaultGreen.png"
        red_path = "./assets/animations/DefaultRed.png"
        self.skateboard_green_sprite = self.resource_manager.load_texture(green_path, config.CAMERA_ZOOM * 2)
        self.skateboard_red_sprite = self.resource_manager.load_texture(red_path, config.CAMERA_ZOOM * 2)
    
    def load_explode_sprite(self):
        explode_path = "./assets/animations/Explode.png"
        self.explode_sprite = self.resource_manager.load_texture(explode_path, config.CAMERA_ZOOM * 2)

    def clear_screen(self):
        self.screen.fill(config.COLORS['background'])
        
    def draw_scene(self):
        # Update board color timer
        self.update_board_color_timer()
        
        if self.skateboard_visible:
            self.draw_skateboard()
        if self.explode_visible and self.explode_sprite:
            self.draw_explode_animation()
        
    def draw_skateboard(self):
        # Get camera shake offset
        shake_x, shake_y = self.get_camera_shake_offset()
        
        # Check if on pad chunk for vertical adjustment
        pad_height_offset = 0
        if self.level and self.level.get_current_chunk_type() == 'pad':
            pad_height_offset = -10  # Raise player by 10px
        
        if self.animation_running and self.current_animation and self.animation_frames:
            current_time = pygame.time.get_ticks()
            time_since_last_frame = current_time - self.last_frame_time
            
            # Update animation frame if enough time has passed
            if time_since_last_frame >= self.frame_duration:
                if self.animation_loop:
                    # Use cached frame count to avoid len() call
                    if self.cached_frame_count == 0:
                        self.cached_frame_count = len(self.animation_frames)
                    self.animation_frame = (self.animation_frame + 1) % self.cached_frame_count
                else:
                    if self.animation_frame < self.cached_frame_count - 1:
                        self.animation_frame += 1
                    else:
                        self.stop_animation()
                        return
                self.last_frame_time = current_time
            
            # Apply camera shake and pad offset to animation position
            current_sprite = self.animation_frames[self.animation_frame]
            shake_position = (
                self.cached_trick_position[0] + shake_x,
                self.cached_trick_position[1] + shake_y + pad_height_offset
            )
            self.screen.blit(current_sprite, shake_position)
        else:
            # Skateboard stays in fixed screen position (in front of scrolling level)
            # Choose sprite based on board color feedback
            sprite_to_use = self.get_board_sprite()
            # Apply camera shake and pad offset to base position
            shake_position = (
                self.skateboard_base_position[0] + shake_x,
                self.skateboard_base_position[1] + shake_y + pad_height_offset
            )
            self.screen.blit(sprite_to_use, shake_position)
    
    def draw_explode_animation(self):
        """Draw the explode animation underneath the skateboard."""
        if self.animation_running and self.current_trick == "Explode" and self.animation_frames:
            # Get camera shake offset
            shake_x, shake_y = self.get_camera_shake_offset()
            
            # Check if on pad chunk for vertical adjustment
            pad_height_offset = 0
            if self.level and self.level.get_current_chunk_type() == 'pad':
                pad_height_offset = -10  # Raise player by 10px
            
            # Position explode animation underneath the skateboard
            explode_position = (
                self.skateboard_base_position[0] + shake_x, 
                self.skateboard_base_position[1] + 30 + shake_y + pad_height_offset  # Offset below skateboard
            )
            current_sprite = self.animation_frames[self.animation_frame]
            self.screen.blit(current_sprite, explode_position)
        
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
        
        # Reset cached frame count for new animation
        self.cached_frame_count = len(self.animation_frames) if self.animation_frames else 0
    
    
    def set_trick_speed(self, trick_name):
        self.frame_duration = self.base_frame_duration
        
        # Check if it's a flip trick or grind trick
        if trick_name in config.FLIP_SPEEDS:
            speed_multiplier = config.FLIP_SPEEDS.get(trick_name, 1.0)
        else:
            # Grind tricks use GRIND_SPEED
            speed_multiplier = config.GRIND_SPEED
        
        self.frame_duration /= speed_multiplier
    
    def stop_animation(self):
        # Store current trick before clearing it
        was_explode = self.current_trick == "Explode"
        
        self.animation_running = False
        self.current_animation = None
        self.current_trick = None
        self.animation_frames = []
        self.animation_frame = 0
        self.cached_frame_count = 0  # Reset cached frame count
        
        # If explode animation finished, hide it
        if was_explode:
            self.explode_visible = False
    
    def set_frame_rate_limit(self, enabled, max_fps=60):
        """Enable/disable frame rate limiting for animations."""
        self.frame_rate_limit = enabled
        self.max_frame_time = 1000 / max_fps if enabled else 0
    
    def show_skateboard(self):
        """Make the skateboard visible and start explode animation."""
        self.skateboard_visible = True
        self.explode_visible = True
        # Start explode animation (non-looping)
        self.start_animation("Explode", self.explode_sprite, loop=False)
    
    def hide_skateboard(self):
        """Hide the skateboard."""
        self.skateboard_visible = False
        self.explode_visible = False
    
    def update_board_color_timer(self):
        """Update the board color timer."""
        if self.board_color_timer > 0:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.board_color_timer_start
            self.board_color_timer = max(0, self.board_color_duration - elapsed)
            if self.board_color_timer <= 0:
                self.board_color_type = None
    
    def get_board_sprite(self):
        """Get the appropriate board sprite based on color feedback."""
        if self.board_color_type == 'green' and self.skateboard_green_sprite:
            return self.skateboard_green_sprite
        elif self.board_color_type == 'red' and self.skateboard_red_sprite:
            return self.skateboard_red_sprite
        else:
            return self.skateboard_sprite
    
    def show_board_color_feedback(self, color_type):
        """Show board color feedback for 0.2 seconds."""
        self.board_color_type = color_type
        self.board_color_timer = self.board_color_duration
        self.board_color_timer_start = pygame.time.get_ticks()

    def add_camera_shake(self, intensity, duration):
        """Add camera shake effect."""
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_timer = 0.0
    
    def update_camera_shake(self):
        """Update camera shake effect."""
        if self.shake_timer < self.shake_duration:
            self.shake_timer += 1.0 / config.FPS
            
            # Only calculate new shake values every few frames to reduce random() calls
            if int(self.shake_timer * config.FPS) % 3 == 0:  # Every 3 frames
                import random
                self.camera_shake_x = random.uniform(-self.shake_intensity, self.shake_intensity)
                self.camera_shake_y = random.uniform(-self.shake_intensity, self.shake_intensity)
        else:
            # Reset shake variables when shake ends
            self.shake_intensity = 0.0
            self.camera_shake_x = 0.0
            self.camera_shake_y = 0.0
    
    def get_camera_shake_offset(self):
        """Get current camera shake offset."""
        return (self.camera_shake_x, self.camera_shake_y)

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