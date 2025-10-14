"""Level generation / management module."""

import config
import os
import pygame
import math

class Level:
    def __init__(self, display, main):
        self.display = display
        self.main = main
        self.load_textures()
        
        # Camera system
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.scroll_speed = 1.0  # pixels per frame
        self.scroll_angle = 45.0  # diagonal angle in degrees
        
        # Chunk management
        self.chunk_size = 8  # 8x8 tiles per chunk
        self.tile_size = 16  # pixel size of each tile
        self.loaded_chunks = {}  # Dictionary to store loaded chunks
        self.chunk_margin = 2  # Extra chunks to keep loaded around visible area
        
        # Calculate viewport bounds
        self.viewport_width = config.DISPLAY_WIDTH // config.CAMERA_ZOOM
        self.viewport_height = config.DISPLAY_HEIGHT // config.CAMERA_ZOOM

    def load_textures(self):
        """
        Load the textures for the level.

        """
        self.floor_texture_location = config.FLOOR_TEXTURES_PATH
        self.Tile1 = pygame.image.load(self.floor_texture_location + "Tile1.png")
        self.Tile2 = pygame.image.load(self.floor_texture_location + "Tile2.png")
        self.Tile3 = pygame.image.load(self.floor_texture_location + "Tile3.png")
        self.StairTile1 = pygame.image.load(self.floor_texture_location + "StairTile1.png")
        self.StairTile2 = pygame.image.load(self.floor_texture_location + "StairTile2.png")

                   
    def draw_level(self):
        #self.create_chunk()
        zoom = config.CAMERA_ZOOM
        for x in range(16):
            for y in range(5):
                tile = self.Tile2 if (x + y) % 2 == 0 else self.Tile3
                
                # Tile pos calculations
                px = (100 + x * 16 - y * 16) * zoom
                py = (100 + x * 8 + y * 8) * zoom
                
                scaled_tile = pygame.transform.scale(tile, (int(tile.get_width() * zoom), int(tile.get_height() * zoom)))
            
                self.display.screen.blit(scaled_tile, (px, py))
    def update_camera(self):
        camera_speed = config.CAMERA_SPEED