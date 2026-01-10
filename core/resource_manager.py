"""Resource management with caching."""

import pygame
import os

# Hardcoded resource settings
CAMERA_ZOOM = 1.25


class ResourceManager:
    def __init__(self):
        self.textures = {}  # Simplified: Consolidated scaled_textures into textures dict (single cache layer)
        self.sounds = {}
        self.fonts = {}
        self.animation_frames_cache = {}
        pygame.mixer.init()
    
    def load_texture(self, path, scale_factor=None):
        """Load a texture with optional scaling."""
        cache_key = f"{path}_{scale_factor}" if scale_factor else path  # Simplified: Single cache key system instead of separate scaled_textures dict
        
        if cache_key in self.textures:
            return self.textures[cache_key]
        
        try:
            texture = pygame.image.load(path)
            if scale_factor and scale_factor != 1.0:
                size = (int(texture.get_width() * scale_factor), 
                       int(texture.get_height() * scale_factor))
                texture = pygame.transform.scale(texture, size)
            self.textures[cache_key] = texture
            return texture
        except Exception as e:  # Simplified: Single exception handler instead of separate pygame.error and generic Exception
            print(f"Failed to load texture {path}: {e}")
            return None
    
    def load_font(self, path, size):
        """Load a font file."""
        cache_key = f"{path}_{size}"
        if cache_key in self.fonts:
            return self.fonts[cache_key]
        
        try:
            font = pygame.font.Font(path, size)
            self.fonts[cache_key] = font
            return font
        except Exception:  # Simplified: Removed separate pygame.error handler and verbose error messages
            return pygame.font.Font(None, size)
    
    def preload_animation_frames(self, animations_path):
        """Pre-extract and cache all animation frames."""
        if not os.path.exists(animations_path):
            return {}
        
        for filename in os.listdir(animations_path):
            if filename.endswith(".png"):
                trick_name = filename[:-4]
                spritemap_path = os.path.join(animations_path, filename)
                spritemap = self.load_texture(spritemap_path)
                if spritemap:
                    frames = self.extract_animation_frames(spritemap, CAMERA_ZOOM * 2)
                    self.animation_frames_cache[trick_name] = frames
        
        return self.animation_frames_cache
    
    def extract_animation_frames(self, spritemap, zoom_factor):
        """Extract frames from spritemap with scaling."""
        frames = []
        spritemap_width, spritemap_height = spritemap.get_size()
        frame_width = spritemap_height
        frame_count = spritemap_width // frame_width
        
        scaled_width = int(frame_width * zoom_factor)
        scaled_height = int(spritemap_height * zoom_factor)
        
        for i in range(frame_count):
            frame_x = i * frame_width
            frame_surface = pygame.Surface((frame_width, spritemap_height), pygame.SRCALPHA)
            frame_surface.blit(spritemap, (0, 0), (frame_x, 0, frame_width, spritemap_height))
            scaled_frame = pygame.transform.scale(frame_surface, (scaled_width, scaled_height))
            frames.append(scaled_frame)
        
        return frames
    
    def get_animation_frames(self, trick_name):
        """Get cached animation frames for a trick."""
        return self.animation_frames_cache.get(trick_name, [])
    
    def cleanup(self):
        """Clean up resources."""
        self.textures.clear()  # Removed: precalculate_common_scaled_textures() method (unnecessary pre-calculation)
        self.sounds.clear()
        self.fonts.clear()
        self.animation_frames_cache.clear()
