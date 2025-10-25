"""Basic resource management with caching."""

import pygame
import os
from typing import Dict, Optional, List
import config


class ResourceManager:
    def __init__(self):
        self.textures: Dict[str, pygame.Surface] = {}
        self.scaled_textures: Dict[str, pygame.Surface] = {}  # Cache for scaled textures
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.animation_frames_cache: Dict[str, List[pygame.Surface]] = {}
        
        pygame.mixer.init()
    
    def load_texture(self, path: str, scale_factor: Optional[float] = None) -> Optional[pygame.Surface]:
        """Load a texture with optional scaling."""
        if path in self.textures:
            texture = self.textures[path]
        else:
            try:
                texture = pygame.image.load(path)
                self.textures[path] = texture
            except pygame.error as e:
                print(f"Warning: Failed to load texture {path}: {e}")
                return None
            except Exception as e:
                print(f"Error: Unexpected error loading texture {path}: {e}")
                return None
        
        if scale_factor and scale_factor != 1.0:
            # Create cache key for scaled texture
            cache_key = f"{path}_{scale_factor}"
            
            # Return cached scaled texture if available
            if cache_key in self.scaled_textures:
                return self.scaled_textures[cache_key]
            
            try:
                original_size = texture.get_size()
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                scaled_texture = pygame.transform.scale(texture, new_size)
                
                # Cache the scaled texture
                self.scaled_textures[cache_key] = scaled_texture
                return scaled_texture
            except Exception as e:
                print(f"Error: Failed to scale texture {path}: {e}")
                return texture
        
        return texture
    
    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """Load a sound file."""
        if path in self.sounds:
            return self.sounds[path]
        
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(config.SOUND_VOLUME)
            self.sounds[path] = sound
            return sound
        except pygame.error as e:
            print(f"Warning: Failed to load sound {path}: {e}")
            return None
        except Exception as e:
            print(f"Error: Unexpected error loading sound {path}: {e}")
            return None
    
    def load_font(self, path: str, size: int) -> Optional[pygame.font.Font]:
        """Load a font file."""
        cache_key = f"{path}_{size}"
        if cache_key in self.fonts:
            return self.fonts[cache_key]
        
        try:
            font = pygame.font.Font(path, size)
            self.fonts[cache_key] = font
            return font
        except pygame.error as e:
            print(f"Warning: Failed to load font {path}: {e}")
            # Fallback to default font
            try:
                return pygame.font.Font(None, size)
            except:
                return None
        except Exception as e:
            print(f"Error: Unexpected error loading font {path}: {e}")
            return None
    
    def preload_animation_frames(self, animations_path: str) -> Dict[str, List[pygame.Surface]]:
        """Pre-extract and cache all animation frames at startup."""
        if not os.path.exists(animations_path):
            return {}
        
        for filename in os.listdir(animations_path):
            if filename.endswith(".png"):
                trick_name = filename[:-4]
                spritemap_path = os.path.join(animations_path, filename)
                
                # Load spritemap
                spritemap = self.load_texture(spritemap_path)
                if spritemap:
                    # Extract and cache frames
                    frames = self.extract_animation_frames(spritemap, config.CAMERA_ZOOM * 2)
                    self.animation_frames_cache[trick_name] = frames
        
        return self.animation_frames_cache
    
    def extract_animation_frames(self, spritemap: pygame.Surface, zoom_factor: float) -> List[pygame.Surface]:
        """Extract frames from spritemap with scaling."""
        frames = []
        spritemap_width, spritemap_height = spritemap.get_size()
        frame_width = spritemap_height
        frame_count = spritemap_width // frame_width
        
        # Pre-calculate scaled dimensions
        scaled_width = int(frame_width * zoom_factor)
        scaled_height = int(spritemap_height * zoom_factor)
        
        for i in range(frame_count):
            frame_x = i * frame_width
            
            # Create frame surface
            frame_surface = pygame.Surface((frame_width, spritemap_height), pygame.SRCALPHA)
            frame_surface.blit(spritemap, (0, 0), (frame_x, 0, frame_width, spritemap_height))
            
            # Scale frame
            scaled_frame = pygame.transform.scale(frame_surface, (scaled_width, scaled_height))
            frames.append(scaled_frame)
        
        return frames
    
    def get_animation_frames(self, trick_name: str) -> List[pygame.Surface]:
        """Get cached animation frames for a trick."""
        return self.animation_frames_cache.get(trick_name, [])
    
    def precalculate_common_scaled_textures(self):
        """Pre-calculate commonly used scaled textures."""
        common_textures = [
            ("./animations/Default.png", config.CAMERA_ZOOM),
            ("./objects/Tile1.png", config.CAMERA_ZOOM),
            ("./objects/Tile2.png", config.CAMERA_ZOOM),
            ("./objects/Tile3.png", config.CAMERA_ZOOM),
            ("./objects/StairTile1.png", config.CAMERA_ZOOM),
            ("./objects/StairTile2.png", config.CAMERA_ZOOM),
        ]
        
        for path, scale_factor in common_textures:
            if os.path.exists(path):
                self.load_texture(path, scale_factor)
    
    def cleanup(self):
        """Clean up resources."""
        self.textures.clear()
        self.scaled_textures.clear()
        self.sounds.clear()
        self.fonts.clear()
        self.animation_frames_cache.clear()