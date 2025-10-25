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
        
        # Camera position for shake
        self.camera_x = 0.0
        self.camera_y = 0.0
        
        # Chunk size system
        self.chunk_width = 32*8
        self.chunk_height = 32*4
        self.chunk_spacing = 32*8 * self.zoom - 1
        self.scroll_speed = config.CAMERA_SPEED
        
        # Queue-based chunk system
        self.chunk_queue = []
        
        # Calculate number of chunks to fill the view (+1 for safety)
        self.max_chunks = int(config.DISPLAY_WIDTH / (self.chunk_spacing * self.zoom)) + 2
        
        # Loaded chunks dictionary
        self.loaded_chunks = {}
        self.init_chunk_queue()
        

    def load_textures(self):
        self.floor_texture_location = config.FLOOR_TEXTURES_PATH
        
        # Load the chunk.png image instead of individual tiles
        self.chunk_texture = self.resource_manager.load_texture(self.floor_texture_location + "chunk.png", self.zoom)
        
        # Keep stair tiles for potential future use
        self.StairTile1 = self.resource_manager.load_texture(self.floor_texture_location + "StairTile1.png", self.zoom)
        self.StairTile2 = self.resource_manager.load_texture(self.floor_texture_location + "StairTile2.png", self.zoom)
    
    def init_chunk_queue(self):
        """Initialize chunk queue with fixed start position"""
        # Start position for chunks
        start_x = 0
        start_y = 0
        
        for i in range(self.max_chunks):
            x = start_x + (i * self.chunk_spacing)
            y = start_y + (i * (self.chunk_spacing // 2))
            self.chunk_queue.append((x, y))
            self.loaded_chunks[i] = [(self.chunk_texture, x, y)]
                   
    def draw_level(self):
        """Draw level chunks"""
        # Get camera shake offset from display
        shake_x, shake_y = self.display.get_camera_shake_offset()
        
        for chunk_data in self.loaded_chunks.values():
            chunk_texture, chunk_x, chunk_y = chunk_data[0]
            self.display.screen.blit(chunk_texture, 
                                   (chunk_x + self.camera_x + shake_x, chunk_y + self.camera_y + shake_y))
        
    def cycle_chunks(self):
        """Conveyor belt system - chunks move diagonally in isometric direction"""
        # Move all chunks in isometric direction (to the left and upward (half the speed))
        move_x = -self.scroll_speed  # X Movement
        move_y = -self.scroll_speed / 2  # Y Movement
        
        # Update chunk positions
        for i in range(len(self.chunk_queue)):
            x, y = self.chunk_queue[i]
            new_x = x + move_x
            new_y = y + move_y
            
            #If chunk has moved enough distance, reposition to the start
            #Slightly more than 1 full chunk space to avoid seeing chunks unload
            if new_x < -(self.chunk_spacing * 1.5): 
                # Move chunk to the right side (end of queue)
                last_chunk_x, last_chunk_y = self.chunk_queue[-1]
                new_x = last_chunk_x + self.chunk_spacing
                new_y = last_chunk_y + (self.chunk_spacing // 2)
                
                # Remove from current position and add to end
                self.chunk_queue.pop(i)
                self.chunk_queue.append((new_x, new_y))
            else:
                # Update position normally
                self.chunk_queue[i] = (new_x, new_y)
        
        # Update loaded chunks with new positions
        for i, (x, y) in enumerate(self.chunk_queue):
            self.loaded_chunks[i] = [(self.chunk_texture, x, y)]
        
    def update_camera(self):
        """Update camera - chunks move continuously"""
        # Camera stays fixed, chunks move every frame
        self.cycle_chunks()