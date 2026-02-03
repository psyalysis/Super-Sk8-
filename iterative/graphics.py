import pygame
import os
import config


class SpriteAnimation:
    """Loads and animates sprite sheets."""
    
    def __init__(self, sprite_path, frame_count=None, scale_factor=1):
        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_duration = 1.0 / config.ANIMATION_FRAME_RATE
        self.is_looping = False
        self.has_finished = False
        
        self._load_sprite_sheet(sprite_path, frame_count, scale_factor)
    
    def _load_sprite_sheet(self, sprite_path, frame_count, scale_factor):
        """Load and split sprite sheet into individual frames."""
        try:
            sheet = pygame.image.load(sprite_path).convert_alpha()
            sheet_width, sheet_height = sheet.get_size()
            
            if frame_count is None:
                frame_width = sheet_height
                frame_count = sheet_width // frame_width
            else:
                frame_width = sheet_width // frame_count
            
            for i in range(frame_count):
                frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, sheet_height))
                for _ in range(scale_factor):
                    frame = pygame.transform.scale2x(frame)
                self.frames.append(frame)
                
        except pygame.error as e:
            print(f"Warning: Could not load sprite {sprite_path}: {e}")
            placeholder_size = 40 * (2 ** scale_factor)
            placeholder = pygame.Surface((placeholder_size, placeholder_size))
            placeholder.fill((255, 0, 255))
            self.frames = [placeholder]
    
    def update(self, dt):
        """Update animation frame."""
        if len(self.frames) <= 1:
            return
        
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.is_looping:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.has_finished = True
    
    def reset(self):
        """Reset animation."""
        self.current_frame = 0
        self.frame_timer = 0
        self.has_finished = False
    
    def get_current_frame(self):
        """Return current frame surface."""
        return self.frames[self.current_frame] if self.frames else None


class Graphics:
    """Manages sprite animations and rendering."""
    
    SPRITE_SCALE = 1  # 0=original, 1=2x, 2=4x, 3=8x
    
    def __init__(self, screen):
        self.screen = screen
        self.animations = {}
        self.current_animation_name = "Default"
        self._load_all_animations()
    
    def _load_all_animations(self):
        """Load all sprite animations."""
        base_path = "./assets/animations"
        
        self.animations["Default"] = SpriteAnimation(f"{base_path}/Default.png", 1, self.SPRITE_SCALE)
        self.animations["Default"].is_looping = True
        
        self._load_animation_group(f"{base_path}/flip", config.TRICK_MAP, loop=False)
        self._load_animation_group(f"{base_path}/grind", config.GRIND_MAP, loop=True)
    
    def _load_animation_group(self, path, name_map, loop):
        """Load a group of animations."""
        for name in name_map.keys():
            sprite_file = f"{path}/{name}.png"
            if os.path.exists(sprite_file):
                self.animations[name] = SpriteAnimation(sprite_file, scale_factor=self.SPRITE_SCALE)
                self.animations[name].is_looping = loop
    
    def update(self, dt, player):
        """Update current animation."""
        animation_name = self._get_animation_for_player(player)
        
        if animation_name != self.current_animation_name:
            self.current_animation_name = animation_name
            if animation_name in self.animations:
                self.animations[animation_name].reset()
        
        if self.current_animation_name in self.animations:
            self.animations[self.current_animation_name].update(dt)
    
    def _get_animation_for_player(self, player):
        """Determine which animation to play."""
        from player import PlayerState
        
        if player.state == PlayerState.GRINDING and player.trick_combo:
            for trick in reversed(player.trick_combo):
                if trick in config.GRIND_MAP and trick in self.animations:
                    return trick
        
        if player.current_trick and player.current_trick in self.animations:
            return player.current_trick
        
        return "Default"
    
    def draw_player(self, player):
        """Draw player sprite."""
        if self.current_animation_name not in self.animations:
            return
        
        frame = self.animations[self.current_animation_name].get_current_frame()
        if frame:
            sprite_rect = frame.get_rect(center=player.rect.center)
            self.screen.blit(frame, sprite_rect)