import pygame
import os
import config


class SpriteAnimation:
    
    def __init__(self, sprite_path, frame_count=None, scale_factor=1):
        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_duration = 1.0 / config.ANIMATION_FRAME_RATE
        self.is_looping = False
        self.has_finished = False
        
        self._load_sprite_sheet(sprite_path, frame_count, scale_factor)
    
    def _load_sprite_sheet(self, sprite_path, frame_count, scale_factor):
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
        self.current_frame = 0
        self.frame_timer = 0
        self.has_finished = False
    
    def get_current_frame(self):
        return self.frames[self.current_frame] if self.frames else None


class Graphics:
    
    SPRITE_SCALE = 1  # 0=original, 1=2x, 2=4x, 3=8x
    
    TRICK_DISPLAY_DURATION = 2000  # ms
    TRICK_FONT_PATH = "./assets/ui/ari-w9500-bold.ttf"
    SCORE_FONT_PATH = "./assets/ui/ari-w9500.ttf"

    def __init__(self, screen):
        self.screen = screen
        self.animations = {}
        self.current_animation_name = "Default"
        self.last_trick_text = None
        self.last_trick_color = (0, 255, 0)  # green
        self.last_trick_until = 0
        self._load_all_animations()
    
    def _load_all_animations(self):
        base_path = "./assets/animations"
        
        self.animations["Default"] = SpriteAnimation(f"{base_path}/Default.png", 1, self.SPRITE_SCALE)
        self.animations["Default"].is_looping = True
        
        self._load_animation_group(f"{base_path}/flip", config.TRICK_MAP, loop=False)
        self._load_animation_group(f"{base_path}/grind", config.GRIND_MAP, loop=True)
    
    def _load_animation_group(self, path, name_map, loop):
        for name in name_map.keys():
            sprite_file = f"{path}/{name}.png"
            if os.path.exists(sprite_file):
                self.animations[name] = SpriteAnimation(sprite_file, scale_factor=self.SPRITE_SCALE)
                self.animations[name].is_looping = loop
    
    def update(self, dt, player, score):
        animation_name = self._get_animation_for_player(player)
        
        if animation_name != self.current_animation_name:
            self.current_animation_name = animation_name
            if animation_name in self.animations:
                self.animations[animation_name].reset()
        
        if self.current_animation_name in self.animations:
            anim = self.animations[self.current_animation_name]
            anim.update(dt)
            if player.current_trick and self.current_animation_name in config.TRICK_MAP and anim.has_finished:
                anim.reset()
    
    def get_current_frame(self):
        if self.current_animation_name not in self.animations:
            return None
        return self.animations[self.current_animation_name].get_current_frame()

    def draw_score(self, score):
        """Draw the score on the screen"""
        font = pygame.font.Font(self.SCORE_FONT_PATH, 28)
        text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        rect = text_surface.get_rect(topleft=(10, 10))
        self.screen.blit(text_surface, rect)

    def draw_text(self, text, success=True):
        """Draw the trick text on the screen"""
        self.last_trick_text = text
        self.last_trick_color = (0, 255, 0) if success else (255, 0, 0)
        self.last_trick_until = pygame.time.get_ticks() + self.TRICK_DISPLAY_DURATION

    def draw_trick_display(self):
        """Draw the trick text on the screen"""
        now = pygame.time.get_ticks()
        if self.last_trick_text and now < self.last_trick_until:
            font = pygame.font.Font(self.TRICK_FONT_PATH, 28)
            text_surface = font.render(self.last_trick_text, True, self.last_trick_color)
            rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 80))
            self.screen.blit(text_surface, rect)
        elif self.last_trick_text:
            self.last_trick_text = None

    def get_current_frame_index(self):
        if self.current_animation_name not in self.animations:
            return None
        return self.animations[self.current_animation_name].current_frame

    def _get_animation_for_player(self, player):
        from player import PlayerState
        
        if player.state == PlayerState.GRINDING and player.trick_combo:
            for trick in reversed(player.trick_combo):
                if trick in config.GRIND_MAP and trick in self.animations:
                    return trick
        
        if player.current_trick and player.current_trick in self.animations:
            return player.current_trick

        if player.state == PlayerState.AIRBORNE and self.current_animation_name in self.animations:
            anim = self.animations[self.current_animation_name]
            if not anim.is_looping and not anim.has_finished:
                return self.current_animation_name
        
        return "Default"
    
    def draw_player(self, player):
        if self.current_animation_name not in self.animations:
            return
        
        frame = self.animations[self.current_animation_name].get_current_frame()
        if frame:
            sprite_rect = frame.get_rect(center=player.rect.center)
            self.screen.blit(frame, sprite_rect)
        