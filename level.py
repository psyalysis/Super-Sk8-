"""Level generation / management module."""

import config
import os
import pygame
import math
import random


class Level:
    def __init__(self, display, resource_manager, state_manager=None):
        self.display = display
        self.resource_manager = resource_manager
        self.state_manager = state_manager
        
        self.zoom = config.CAMERA_ZOOM
        
        self.load_textures()
        
        # Camera position for shake
        self.camera_x = 0.0
        self.camera_y = 100.0
        
        # Chunk size system
        self.chunk_width = 32*8
        self.chunk_height = 32*4
        # Use actual texture width to eliminate gaps
        self.chunk_spacing = 316  # Actual texture width
        self.scroll_speed = config.CAMERA_SPEED
        
        # Queue-based chunk system - store (x, y, has_rail, has_pad) tuples
        self.chunk_queue = []
        
        # Calculate number of chunks to fill the view (+1 for safety)
        self.max_chunks = int(config.DISPLAY_WIDTH / (self.chunk_spacing * self.zoom)) + 2
        self.init_chunk_queue()
        
        # Track current chunk info
        self.current_chunk_index = None
        

    def load_textures(self):
        self.floor_texture_location = config.FLOOR_TEXTURES_PATH
        
        # Load the floorBlend.png image instead of chunk.png
        # Use the same zoom factor as before - the resource manager will handle scaling
        self.chunk_texture = self.resource_manager.load_texture(self.floor_texture_location + "floorBlend.png", self.zoom)
        
        # Load rail texture for layering on chunks
        self.rail_texture = self.resource_manager.load_texture(self.floor_texture_location + "railBlend.png", self.zoom)
        
        # Load manny pad texture for layering on chunks
        self.pad_texture = self.resource_manager.load_texture(self.floor_texture_location + "padBlend.png", self.zoom)
        
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
            
            # Assign rail or manny pad with mutual exclusion
            has_rail = False
            has_pad = False
            
            # 1/6 chance of having a rail
            if random.randint(1, 6) == 1:
                has_rail = True
            # 1/8 chance of having a manny pad (only if no rail)
            elif random.randint(1, 8) == 1:
                has_pad = True
            
            self.chunk_queue.append((x, y, has_rail, has_pad))
                   
    def draw_level(self):
        """Draw level chunks"""
        # Get camera shake offset from display
        shake_x, shake_y = self.display.get_camera_shake_offset()
        
        for chunk_data in self.chunk_queue:
            chunk_x, chunk_y, has_rail, has_pad = chunk_data
            
            # Draw floor chunk
            self.display.screen.blit(self.chunk_texture, 
                                   (chunk_x + self.camera_x + shake_x, chunk_y + self.camera_y + shake_y))
            
            # Draw rail texture on top if chunk has rail
            if has_rail:
                self.display.screen.blit(self.rail_texture, 
                                       (chunk_x + self.camera_x + shake_x, chunk_y + self.camera_y + shake_y))
            
            # Draw manny pad texture on top if chunk has manny pad
            if has_pad:
                self.display.screen.blit(self.pad_texture, 
                                       (chunk_x + self.camera_x + shake_x, chunk_y + self.camera_y + shake_y))
        
    def cycle_chunks(self):
        """Conveyor belt system - chunks move diagonally in isometric direction"""
        # Apply speed multiplier when grinding
        speed_multiplier = 1.3 if (self.state_manager and self.state_manager.is_player_grinding()) else 1.0
        
        # Move all chunks in isometric direction (to the left and upward (half the speed))
        move_x = -self.scroll_speed * speed_multiplier  # X Movement
        move_y = -self.scroll_speed / 2 * speed_multiplier  # Y Movement
        
        # Track which chunks need to be repositioned
        chunks_to_reposition = []
        
        # Update chunk positions
        for i in range(len(self.chunk_queue)):
            x, y, has_rail, has_pad = self.chunk_queue[i]
            new_x = x + move_x
            new_y = y + move_y
            
            #If chunk has moved enough distance bring it back to the start
            if new_x < -(self.chunk_spacing * 1.5): 
                chunks_to_reposition.append(i)
            else:
                # Update position normally, preserve rail and pad info
                self.chunk_queue[i] = (new_x, new_y, has_rail, has_pad)
        
        # Handle repositioned chunks in reverse order
        for i in reversed(chunks_to_reposition):
            # Move chunk to the right side (end of queue)
            last_chunk_x, last_chunk_y, _, _ = self.chunk_queue[-1]
            new_x = last_chunk_x + self.chunk_spacing
            new_y = last_chunk_y + (self.chunk_spacing // 2)
            
            # Remove from current position and add to end with new rail/pad chance
            self.chunk_queue.pop(i)
            
            # Assign rail or manny pad with mutual exclusion
            has_rail = False
            has_pad = False
            
            # 1/6 chance of having a rail
            if random.randint(1, 6) == 1:
                has_rail = True
            # 1/8 chance of having a manny pad (only if no rail)
            elif random.randint(1, 8) == 1:
                has_pad = True
            
            self.chunk_queue.append((new_x, new_y, has_rail, has_pad))
        
    def get_current_chunk_type(self):
        """Get the chunk type at the camera position."""
        # Find which chunk the player (camera) is currently over
        for chunk_data in self.chunk_queue:
            chunk_x, chunk_y, has_rail, has_pad = chunk_data
            chunk_x = chunk_x - 50
            # Check if camera position falls within chunk bounds
            chunk_end_x = chunk_x + self.chunk_spacing
            
            # Check if the camera is within this chunk's X range
            if chunk_x <= -self.camera_x <= chunk_end_x:
                if has_rail:
                    return 'rail'
                elif has_pad:
                    return 'pad'
                else:
                    return None
        return None
    
    
    
    def update_camera(self):
        """Update camera - chunks move continuously"""
        # Camera stays fixed, chunks move every frame
        self.cycle_chunks()
        
        