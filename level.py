"""Level generation / management module."""

import config
import os
import pygame
import math

class Level:
    def __init__(self, display, main):
        self.display = display
        self.main = main
        
        self.zoom = config.CAMERA_ZOOM
        
        self.load_textures()
        
        # Camera system
        self.camera_x = 0.0
        self.camera_y = 0.0
        
        # Chunk system - proper infinite terrain approach
        self.chunk_size = 8  # 8x8 tiles per chunk
        self.loaded_chunks = {}  # Dictionary: (chunk_x, chunk_y) -> tiles
        self.chunk_load_distance = 3  # Load chunks within 3 chunks of camera
        
        # Calculate viewport bounds
        self.viewport_width = config.DISPLAY_WIDTH // config.CAMERA_ZOOM
        self.viewport_height = config.DISPLAY_HEIGHT // config.CAMERA_ZOOM
        
        # Initialize with chunks around origin
        self.update_chunks()

    def load_textures(self):
        """Load and pre-scale textures for better performance"""
        self.floor_texture_location = config.FLOOR_TEXTURES_PATH
        
        # Load base textures
        base_tile1 = pygame.image.load(self.floor_texture_location + "Tile1.png")
        base_tile2 = pygame.image.load(self.floor_texture_location + "Tile2.png")
        base_tile3 = pygame.image.load(self.floor_texture_location + "Tile3.png")
        
        # Pre-scale textures to avoid runtime scaling
        scaled_size = (int(base_tile1.get_width() * self.zoom), int(base_tile1.get_height() * self.zoom))
        self.Tile1 = pygame.transform.scale(base_tile1, scaled_size)
        self.Tile2 = pygame.transform.scale(base_tile2, scaled_size)
        self.Tile3 = pygame.transform.scale(base_tile3, scaled_size)
        
        # Load stair textures if needed
        self.StairTile1 = pygame.image.load(self.floor_texture_location + "StairTile1.png")
        self.StairTile2 = pygame.image.load(self.floor_texture_location + "StairTile2.png")
        
                   
    def draw_level(self):
        """Draw all visible tiles from loaded chunks"""
        for chunk_key, tiles in self.loaded_chunks.items():
            for tile_data in tiles:
                tile_texture, tile_x, tile_y = tile_data
                # Apply camera offset
                screen_x = tile_x + self.camera_x
                screen_y = tile_y + self.camera_y
                
                # Only draw tiles that are potentially visible
                if (screen_x > -64 and screen_x < config.DISPLAY_WIDTH + 64 and 
                    screen_y > -64 and screen_y < config.DISPLAY_HEIGHT + 64):
                    self.display.screen.blit(tile_texture, (screen_x, screen_y))
        
    def get_camera_chunk_coords(self):
        """Convert camera position to chunk coordinates"""
        # Based on the original coordinate system from the commented code
        # Original: px = (x * 16 - y * 16) * zoom, py = (100 + x * 8 + y * 8) * zoom
        
        # Convert camera position to approximate grid coordinates
        # Since camera moves at speed 6 horizontally and 3 vertically
        # We need to reverse the isometric projection
        
        # Approximate conversion based on the original system
        # The original system used: rows (x) and y coordinates
        # Camera moves backwards, so we calculate which "row" we're at
        approximate_row = int(-self.camera_x / (16 * self.zoom))
        
        # Convert to chunk coordinates
        chunk_x = approximate_row // self.chunk_size
        chunk_y = 0  # For now, keep it simple with single row chunks
        
        return chunk_x, chunk_y
    
    def create_chunk(self, chunk_x, chunk_y):
        """Create a chunk at specific coordinates using original coordinate system"""
        tiles = []
        
        # Calculate the starting row for this chunk
        start_row = chunk_x * self.chunk_size
        
        for local_x in range(self.chunk_size):
            row = start_row + local_x
            for local_y in range(self.chunk_size):
                # Use the original coordinate system
                tile = self.Tile2 if (row + local_y) % 2 == 0 else self.Tile3
                
                # Original coordinate calculation
                px = ((row * 16 - local_y * 16) * self.zoom) - 150
                py = (row * 8 + local_y * 8) * self.zoom
                
                tiles.append((tile, px, py))
        
        return tiles
    
    def update_chunks(self):
        """Update loaded chunks based on camera position"""
        camera_chunk_x, camera_chunk_y = self.get_camera_chunk_coords()
        
        # For the original system, we mainly need chunks ahead and behind
        # Load chunks ahead (positive x) and behind (negative x) the camera
        chunks_to_load = set()
        for dx in range(-self.chunk_load_distance, self.chunk_load_distance + 1):
            chunk_x = camera_chunk_x + dx
            chunk_y = camera_chunk_y  # Keep y at 0 for now
            chunks_to_load.add((chunk_x, chunk_y))
        
        # Remove chunks that are no longer needed
        chunks_to_remove = []
        for chunk_key in self.loaded_chunks.keys():
            if chunk_key not in chunks_to_load:
                chunks_to_remove.append(chunk_key)
        
        for chunk_key in chunks_to_remove:
            del self.loaded_chunks[chunk_key]
        
        # Load new chunks
        for chunk_x, chunk_y in chunks_to_load:
            chunk_key = (chunk_x, chunk_y)
            if chunk_key not in self.loaded_chunks:
                self.loaded_chunks[chunk_key] = self.create_chunk(chunk_x, chunk_y)
        
    def update_camera(self):
        camera_speed = config.CAMERA_SPEED
        #Scroll the camera by the camera speed (subtract because the level goes backwards).
        #Camera Y location is divided by 2 due to isometric view
        self.camera_x -= camera_speed
        self.camera_y -= camera_speed / 2 
        
        # Update chunks based on new camera position
        self.update_chunks()
            
        