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
        
        

        self.rows = 0
        # Calculate viewport bounds
        self.viewport_width = config.DISPLAY_WIDTH // config.CAMERA_ZOOM
        self.viewport_height = config.DISPLAY_HEIGHT // config.CAMERA_ZOOM
        
        self.tiles = []
        self.last_chunk_removed_at = -1  # Track when last chunk was removed
        self.frame_counter = 0  # Frame counter for chunk management
        
        #Create 5 starter chunks
        for starterChunks in range(8):
            self.create_chunk()

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
        
        """
        for x in range(42):
            for y in range(5):
                tile = self.Tile2 if (x + y) % 2 == 0 else self.Tile3
                
                # Tile pos calculations
                px = (x * 16 - y * 16) * self.zoom
                py = (100 + x * 8 + y * 8) * self.zoom
                
                scaled_tile = pygame.transform.scale(tile, (int(tile.get_width() * self.zoom), int(tile.get_height() * self.zoom)))
                
                #Move tiles according to camera position
                px += self.camera_x
                py += self.camera_y
                """
        
        #Draw Every Tile in their position     
        for tile in self.tiles:
            tile_x = tile[1] + self.camera_x
            tile_y = tile[2] + self.camera_y
            self.display.screen.blit(tile[0], (tile_x, tile_y))
        
    def create_chunk(self):
        for x in range(6):
            self.rows += 1
            for y in range(6):
                tile = self.Tile2 if (x + y) % 2 == 0 else self.Tile3
                
                px = ((self.rows * 16 - y * 16) * self.zoom) - 150
                py = (self.rows * 8 + y * 8) * self.zoom
                
                # Use pre-scaled texture (no runtime scaling needed)
                # Use tuple for better performance than list
                self.tiles.append((tile, px, py))
                
    def remove_old_chunk(self):
        # Each chunk has 6x6 = 36 tiles, so remove 36 tiles
        self.tiles = self.tiles[36:]
        
    def update_camera(self):
        camera_speed = config.CAMERA_SPEED
        #Scroll the camera by the camera speed (subtract because the level goes backwards).
        #Camera Y location is divided by 2 due to isometric view
        self.camera_x -= camera_speed
        self.camera_y -= camera_speed / 2 
        
        # Increment frame counter
        self.frame_counter += 1
        
        # Calculate chunk management frequency based on camera speed
        # Higher speeds need more frequent chunk management
        chunk_check_frequency = max(1, 8 - (camera_speed // 3))
        
        # Manage chunks based on camera speed
        if self.frame_counter % chunk_check_frequency == 0:
            #Calculate how many tiles have been scrolled
            tiles_scrolled_x = self.camera_x // 16
            tiles_scrolled_y = self.camera_y // 8
            
            #Use pythagorean theorem to calculate the total tiles scrolled!! Maths coming in handy
            tiles_scrolled = int(math.sqrt(tiles_scrolled_x**2 + tiles_scrolled_y**2))
            
            # Create chunks more aggressively - check if we need a new chunk
            # Instead of exact modulo, check if we've scrolled enough since last chunk
            tiles_since_last_chunk = tiles_scrolled - self.last_chunk_removed_at
            if tiles_since_last_chunk >= 16:
                self.last_chunk_removed_at = tiles_scrolled
                self.create_chunk()
                self.remove_old_chunk()
            
        