"""Level generation / management module."""

import config
import os
import pygame
import math


class Level:
    def __init__(self, display, resource_manager):
        self.display = display
        self.resource_manager = resource_manager
        
        self.zoom = config.CAMERA_ZOOM
        
        self.load_textures()
        
        # Camera system
        self.camera_x = 0.0
        self.camera_y = 0.0
        
        # Chunk system
        self.chunk_size = 8
        self.loaded_chunks = {}
        self.chunk_load_distance = 6
        
        # Viewport bounds
        self.viewport_width = config.DISPLAY_WIDTH // config.CAMERA_ZOOM
        self.viewport_height = config.DISPLAY_HEIGHT // config.CAMERA_ZOOM
        
        self.update_chunks()

    def load_textures(self):
        self.floor_texture_location = config.FLOOR_TEXTURES_PATH
        
        self.Tile1 = self.resource_manager.load_texture(self.floor_texture_location + "Tile1.png", self.zoom)
        self.Tile2 = self.resource_manager.load_texture(self.floor_texture_location + "Tile2.png", self.zoom)
        self.Tile3 = self.resource_manager.load_texture(self.floor_texture_location + "Tile3.png", self.zoom)
        
        self.StairTile1 = self.resource_manager.load_texture(self.floor_texture_location + "StairTile1.png", self.zoom)
        self.StairTile2 = self.resource_manager.load_texture(self.floor_texture_location + "StairTile2.png", self.zoom)
                   
    def draw_level(self):
        for chunk_key, tiles in self.loaded_chunks.items():
            for tile_data in tiles:
                tile_texture, tile_x, tile_y = tile_data
                screen_x = tile_x + self.camera_x
                screen_y = tile_y + self.camera_y
                
                if (screen_x > -64 and screen_x < config.DISPLAY_WIDTH + 64 and 
                    screen_y > -64 and screen_y < config.DISPLAY_HEIGHT + 64):
                    self.display.screen.blit(tile_texture, (screen_x, screen_y))
        
    def get_camera_chunk_coords(self):
        approximate_row = int(-self.camera_x / (16 * self.zoom))
        chunk_x = approximate_row // self.chunk_size
        chunk_y = 0
        return chunk_x, chunk_y
    
    def create_chunk(self, chunk_x, chunk_y):
        tiles = []
        start_row = chunk_x * self.chunk_size
        
        for local_x in range(self.chunk_size):
            row = start_row + local_x
            for local_y in range(self.chunk_size):
                tile = self.Tile2 if (row + local_y) % 2 == 0 else self.Tile3
                
                px = ((row * 16 - local_y * 16) * self.zoom) - 150
                py = (row * 8 + local_y * 8) * self.zoom
                
                tiles.append((tile, px, py))
        
        return tiles
    
    def update_chunks(self):
        camera_chunk_x, camera_chunk_y = self.get_camera_chunk_coords()
        
        chunks_to_load = set()
        for dx in range(-self.chunk_load_distance, self.chunk_load_distance + 1):
            chunk_x = camera_chunk_x + dx
            chunk_y = camera_chunk_y
            chunks_to_load.add((chunk_x, chunk_y))
        
        chunks_to_remove = []
        for chunk_key in self.loaded_chunks.keys():
            if chunk_key not in chunks_to_load:
                chunks_to_remove.append(chunk_key)
        
        for chunk_key in chunks_to_remove:
            del self.loaded_chunks[chunk_key]
        
        for chunk_x, chunk_y in chunks_to_load:
            chunk_key = (chunk_x, chunk_y)
            if chunk_key not in self.loaded_chunks:
                self.loaded_chunks[chunk_key] = self.create_chunk(chunk_x, chunk_y)
        
    def update_camera(self):
        camera_speed = config.CAMERA_SPEED
        self.camera_x -= camera_speed
        self.camera_y -= camera_speed / 2 
        self.update_chunks()