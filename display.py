"""Display/window module."""

import config
import pygame

class Display:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(config.FONT_PATH, config.FONT_SIZE_SMALL)
        self.debug_text_position = (10, 10) 
        self.skateboard_sprite = None
        
        # Animation system state
        self.current_animation = None
        self.current_trick = None
        self.animation_frames = []
        self.animation_frame = 0
        self.animation_running = False
        self.animation_loop = False
        self.last_frame_time = 0
        self.base_frame_duration = (1000 / config.ANIMATION_FRAME_RATE) / 2  # milliseconds per frame (2x speed)
        self.frame_duration = self.base_frame_duration
        
        # Position skateboard over middle of tiles on left side of window
        # Based on tile positioning: px = ((rows * 16 - y * 16) * zoom) - 150, py = (rows * 8 + y * 8) * zoom
        # With zoom=2, positioning at left side center of tile area
        self.skateboard_base_position = (200, 300)
        self.skateboard_position = self.skateboard_base_position
        self.load_skateboard_sprite()
    
    def load_skateboard_sprite(self):
        """
        Load the skateboard sprite from file.
        """
        
        skateboard_path = "./animations/Default.png"
        self.skateboard_sprite = pygame.image.load(skateboard_path)
        
        # Scale skateboard to match level resolution using camera zoom
        original_width, original_height = self.skateboard_sprite.get_size()
        scaled_size = (int(original_width * (config.CAMERA_ZOOM)), int(original_height * (config.CAMERA_ZOOM)))
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
        """
        Draw the skateboard sprite. Shows default animation or current trick animation.
        """
        if self.animation_running and self.current_animation and self.animation_frames:
            # Raise skateboard 100px when doing tricks
            trick_position = (self.skateboard_base_position[0], self.skateboard_base_position[1] - 50) # Jump 50px
            
            # Draw current animation frame
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_duration:
                if self.animation_loop:
                    # Loop animation while keys are held
                    self.animation_frame = (self.animation_frame + 1) % len(self.animation_frames)
                else:
                    # Play animation once
                    if self.animation_frame < len(self.animation_frames) - 1:
                        self.animation_frame += 1
                    else:
                        # Animation finished, stop it
                        self.stop_animation()
                        return
                self.last_frame_time = current_time
            
            # Use current frame from animation_frames list
            current_sprite = self.animation_frames[self.animation_frame]
            self.screen.blit(current_sprite, trick_position)
        else:
            # Draw default skateboard sprite at normal position
            self.screen.blit(self.skateboard_sprite, self.skateboard_base_position)
        
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
    
    def start_animation(self, trick_name, animation_sprite, loop=False):
        """
        Start playing a trick animation by extracting frames from spritemap.
        
        Args:
            trick_name (str): Name of the trick
            animation_sprite: Horizontal spritemap image containing all frames
            loop (bool): Whether to loop the animation while keys are held
        """
        self.current_trick = trick_name
        self.current_animation = animation_sprite
        
        # Set frame duration based on trick type
        self.set_trick_speed(trick_name)
        
        # Extract individual frames from the horizontal spritemap
        self.animation_frames = self.extract_frames_from_spritemap(animation_sprite)
        self.animation_frame = 0
        self.animation_running = True
        self.animation_loop = loop
        self.last_frame_time = pygame.time.get_ticks()
        
        print(f"Started animation: {trick_name} with {len(self.animation_frames)} frames (loop: {loop}, speed: {self.frame_duration}ms)")
    
    def extract_frames_from_spritemap(self, spritemap):
        """
        Extract individual frames from a horizontal spritemap image.
        
        Args:
            spritemap: Pygame surface containing horizontal sprite sheet
            
        Returns:
            List of pygame surfaces, each representing one frame
        """
        frames = []
        
        # Get spritemap dimensions
        spritemap_width, spritemap_height = spritemap.get_size()
        
        # Estimate frame count based on typical frame width
        # Most skateboard sprites are roughly square, so we can estimate
        estimated_frame_width = spritemap_height  # Assume square frames
        estimated_frame_count = spritemap_width // estimated_frame_width
        
        # Extract frames
        for i in range(estimated_frame_count):
            # Calculate frame position
            frame_x = i * estimated_frame_width
            frame_y = 0
            frame_width = estimated_frame_width
            frame_height = spritemap_height
            
            # Create frame surface
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            
            # Extract frame from spritemap
            frame_surface.blit(spritemap, (0, 0), (frame_x, frame_y, frame_width, frame_height))
            
            # Scale frame to match skateboard size
            original_width, original_height = frame_surface.get_size()
            scaled_size = (int(original_width * config.CAMERA_ZOOM), int(original_height * config.CAMERA_ZOOM))
            scaled_frame = pygame.transform.scale(frame_surface, scaled_size)
            
            frames.append(scaled_frame)
        
        print(f"Extracted {len(frames)} frames from spritemap")
        return frames
    
    def set_trick_speed(self, trick_name):
        """
        Set the frame duration based on the trick type.
        
        Args:
            trick_name (str): Name of the trick
        """
        # Reset to base speed first
        self.frame_duration = self.base_frame_duration
        
        # Apply speed multipliers based on trick type
        if "360" in trick_name:
            # 360 shuv tricks are 2x slower
            self.frame_duration *= 2.0
        elif any(x in trick_name.lower() for x in ["shuv", "flip"]) and ("180" in trick_name or "varial" in trick_name):
            # 180 shuv/flip tricks are 1.5x slower
            self.frame_duration *= 1.5
    
    def stop_animation(self):
        """
        Stop the current animation and return to default sprite.
        """
        self.animation_running = False
        self.current_animation = None
        self.current_trick = None
        self.animation_frames = []
        self.animation_frame = 0
        print("Stopped animation - returning to default")

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