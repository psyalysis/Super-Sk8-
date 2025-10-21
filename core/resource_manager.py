"""Centralized resource management with caching."""

import pygame
import os
from typing import Dict, Optional, Any
import config


class ResourceManager:
    def __init__(self):
        self.textures: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.scaled_textures: Dict[str, pygame.Surface] = {}
        
        pygame.mixer.init()
    
    def load_texture(self, path: str, scale_factor: Optional[float] = None) -> Optional[pygame.Surface]:
        if path in self.textures:
            texture = self.textures[path]
        else:
            try:
                texture = pygame.image.load(path)
                self.textures[path] = texture
            except pygame.error as e:
                return None
        
        if scale_factor and scale_factor != 1.0:
            cache_key = f"{path}_{scale_factor}"
            if cache_key in self.scaled_textures:
                return self.scaled_textures[cache_key]
            
            original_size = texture.get_size()
            new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
            scaled_texture = pygame.transform.scale(texture, new_size)
            self.scaled_textures[cache_key] = scaled_texture
            return scaled_texture
        
        return texture
    
    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        if path in self.sounds:
            return self.sounds[path]
        
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(config.SOUND_VOLUME)
            self.sounds[path] = sound
            return sound
        except pygame.error as e:
            return None
    
    def load_font(self, path: str, size: int) -> Optional[pygame.font.Font]:
        cache_key = f"{path}_{size}"
        if cache_key in self.fonts:
            return self.fonts[cache_key]
        
        try:
            font = pygame.font.Font(path, size)
            self.fonts[cache_key] = font
            return font
        except pygame.error as e:
            return None
    
    def preload_animations(self, animations_path: str) -> Dict[str, pygame.Surface]:
        animations = {}
        
        if not os.path.exists(animations_path):
            return animations
        
        for filename in os.listdir(animations_path):
            if filename.endswith(".png"):
                full_path = os.path.join(animations_path, filename)
                trick_name = filename[:-4]
                
                texture = self.load_texture(full_path)
                if texture:
                    animations[trick_name] = texture
        
        return animations
    
    def preload_level_textures(self, textures_path: str, zoom_factor: float) -> Dict[str, pygame.Surface]:
        textures = {}
        
        if not os.path.exists(textures_path):
            return textures
        
        texture_files = ["Tile1.png", "Tile2.png", "Tile3.png", "StairTile1.png", "StairTile2.png"]
        
        for filename in texture_files:
            full_path = os.path.join(textures_path, filename)
            if os.path.exists(full_path):
                texture_name = filename[:-4]
                texture = self.load_texture(full_path, zoom_factor)
                if texture:
                    textures[texture_name] = texture
        
        return textures
    
    def get_texture(self, path: str, scale_factor: Optional[float] = None) -> Optional[pygame.Surface]:
        if scale_factor and scale_factor != 1.0:
            cache_key = f"{path}_{scale_factor}"
            return self.scaled_textures.get(cache_key)
        return self.textures.get(path)
    
    def get_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        return self.sounds.get(path)
    
    def get_font(self, path: str, size: int) -> Optional[pygame.font.Font]:
        cache_key = f"{path}_{size}"
        return self.fonts.get(cache_key)
    
    def cleanup(self):
        self.textures.clear()
        self.sounds.clear()
        self.fonts.clear()
        self.scaled_textures.clear()
    
    def get_memory_usage(self) -> Dict[str, int]:
        return {
            'textures': len(self.textures),
            'scaled_textures': len(self.scaled_textures),
            'sounds': len(self.sounds),
            'fonts': len(self.fonts)
        }