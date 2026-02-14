import pygame
import random
import config
from enum import Enum


class ChunkType(Enum):
    """Types of level chunks."""
    FLOOR = None
    RAIL = "rail"


class Level:
    """Manages level chunks and scrolling behavior."""

    def __init__(self, screen):
        self.screen = screen
        self._load_textures()
        self._initialize_properties()
        self._initialize_chunks()

    def _load_textures(self):
        self.floor_image = self._load_texture(
            "./assets/level/floorChunk.png",
            "floorChunk.png"
        )
        self.rail_image = self._load_texture(
            "./assets/level/railBlend.png",
            "railBlend.png"
        )
    
    def _load_texture(self, path, name):
        try:
            return pygame.image.load(path).convert_alpha()
        except pygame.error:
            print(f"Warning: Could not find {name}. Ensure you are running from the correct directory")
            return None

    def _initialize_properties(self):
        self.chunks = []
        self.rail_chunks = []
        
        # Level configuration constants
        self.scroll_speed = 350
        self.chunk_width = 291  # Width of floorChunk.png
        self.chunk_overlap = 41  # Overlap between chunks
        self.chunk_extra_offset = 1.5  # Extra chunk travel distance multiplier before recycled
        self.base_y = 100
        self.initial_chunk_count = 5
        
        # Calculated spacing
        self.spacing_x = self.chunk_width - self.chunk_overlap
        self.spacing_y = self.spacing_x / 2
        
        # Rail generation probability (25% chance: 1 rail in 4 chunks)
        self.rail_probability = 0.25

    def _initialize_chunks(self):
        for i in range(self.initial_chunk_count):
            x = i * self.spacing_x
            y = self.base_y + i * self.spacing_y
            self.chunks.append(self._generate_chunk(x, y))

    def _generate_chunk(self, x, y):
        chunk_type = ChunkType.RAIL.value if random.random() < self.rail_probability else ChunkType.FLOOR.value
        
        chunk = {
            "pos": pygame.Vector2(x, y),
            "type": chunk_type
        }
        if chunk["type"] == ChunkType.RAIL.value:
            self.rail_chunks.append(chunk)
        
        return chunk

    def update(self, dt):
        self._update_chunk_positions(dt)
        self._recycle_offscreen_chunks()

    def _update_chunk_positions(self, dt):
        for chunk in self.chunks:
            chunk["pos"].x -= self.scroll_speed * dt
            chunk["pos"].y -= (self.scroll_speed / 2) * dt

    def _recycle_offscreen_chunks(self):
        if not self.chunks:
            return
            
        first_chunk = self.chunks[0]
        recycle_threshold = -self.chunk_width * self.chunk_extra_offset
        
        if first_chunk["pos"].x < recycle_threshold:
            last_chunk = self.chunks[-1]
            chunk_to_remove = self.chunks.pop(0)
            if chunk_to_remove["type"] == ChunkType.RAIL.value and chunk_to_remove in self.rail_chunks:
                self.rail_chunks.remove(chunk_to_remove)
            new_x = last_chunk["pos"].x + self.spacing_x
            new_y = last_chunk["pos"].y + self.spacing_y
            self.chunks.append(self._generate_chunk(new_x, new_y))

    def get_current_chunk_type(self):
        player_x = 0
        for chunk in self.chunks:
            chunk_left = chunk["pos"].x
            chunk_right = chunk_left + self.chunk_width
            if chunk_left <= player_x <= chunk_right:
                return chunk["type"]
        return None

    def draw(self):
        self._draw_floor_chunks()
        self._draw_rail_chunks()

    def _draw_floor_chunks(self):
        if self.floor_image is None:
            return
            
        for chunk in self.chunks:
            self.screen.blit(self.floor_image, (chunk["pos"].x, chunk["pos"].y))

    def _draw_rail_chunks(self):
        if self.rail_image is None:
            return
            
        for rail_chunk in self.rail_chunks:
            if rail_chunk["pos"].x > -self.chunk_width:
                position = (rail_chunk["pos"].x, rail_chunk["pos"].y)
                self.screen.blit(self.rail_image, position)
                