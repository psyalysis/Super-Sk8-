"""Level generation / management module."""

import random
from collections import namedtuple

# Hardcoded level settings
CAMERA_ZOOM = 1.25
CAMERA_SPEED = 8
DISPLAY_WIDTH = 1100
FLOOR_TEXTURES_PATH = "./assets/level/"

# Chunk generation constants
RAIL_CHANCE = 6  # 1 in 6
PAD_CHANCE = 8  # 1 in 8
GRIND_SPEED_MULTIPLIER = 1.3
CHUNK_REPOSITION_THRESHOLD = 1.5
CHUNK_TYPE_CHECK_OFFSET = 50

Chunk = namedtuple('Chunk', ['x', 'y', 'has_rail', 'has_pad'])


class Level:
    def __init__(self, display, resource_manager, state_manager=None):
        self.display = display
        self.resource_manager = resource_manager
        self.state_manager = state_manager
        
        self.zoom = CAMERA_ZOOM
        self.load_textures()
        
        self.camera_x = 0.0
        self.camera_y = 100.0
        
        self.chunk_spacing = 316
        self.scroll_speed = CAMERA_SPEED
        
        self.chunk_queue = []
        self.max_chunks = int(DISPLAY_WIDTH / (self.chunk_spacing * self.zoom)) + 2
        self.init_chunk_queue()

    def load_textures(self):
        base_path = FLOOR_TEXTURES_PATH
        self.chunk_texture = self.resource_manager.load_texture(f"{base_path}floorBlend.png", self.zoom)
        self.rail_texture = self.resource_manager.load_texture(f"{base_path}railBlend.png", self.zoom)
        self.pad_texture = self.resource_manager.load_texture(f"{base_path}padBlend.png", self.zoom)
    
    def _generate_chunk_features(self):
        """Generate random rail/pad features for a chunk."""
        has_rail = random.randint(1, RAIL_CHANCE) == 1
        has_pad = not has_rail and random.randint(1, PAD_CHANCE) == 1
        return has_rail, has_pad
    
    def init_chunk_queue(self):
        for i in range(self.max_chunks):
            x = i * self.chunk_spacing
            y = i * (self.chunk_spacing // 2)
            has_rail, has_pad = self._generate_chunk_features()
            self.chunk_queue.append(Chunk(x, y, has_rail, has_pad))
                   
    def draw_level(self):
        offset_x = self.camera_x
        offset_y = self.camera_y
        
        for chunk in self.chunk_queue:
            pos = (chunk.x + offset_x, chunk.y + offset_y)
            self.display.screen.blit(self.chunk_texture, pos)
            
            if chunk.has_rail:
                self.display.screen.blit(self.rail_texture, pos)
            elif chunk.has_pad:
                self.display.screen.blit(self.pad_texture, pos)
        
    def cycle_chunks(self):
        speed_multiplier = GRIND_SPEED_MULTIPLIER if (self.state_manager and self.state_manager.is_player_grinding()) else 1.0
        move_x = -self.scroll_speed * speed_multiplier
        move_y = -self.scroll_speed / 2 * speed_multiplier
        threshold = -(self.chunk_spacing * CHUNK_REPOSITION_THRESHOLD)
        
        chunks_to_reposition = []
        
        # Update chunk positions
        for i, chunk in enumerate(self.chunk_queue):
            new_x = chunk.x + move_x
            if new_x < threshold:
                chunks_to_reposition.append(i)
            else:
                self.chunk_queue[i] = Chunk(new_x, chunk.y + move_y, chunk.has_rail, chunk.has_pad)
        
        # Reposition chunks in reverse order (to maintain indices)
        for i in reversed(chunks_to_reposition):
            last_chunk = self.chunk_queue[-1]
            new_x = last_chunk.x + self.chunk_spacing
            new_y = last_chunk.y + (self.chunk_spacing // 2)
            has_rail, has_pad = self._generate_chunk_features()
            
            self.chunk_queue.pop(i)
            self.chunk_queue.append(Chunk(new_x, new_y, has_rail, has_pad))
        
    def get_current_chunk_type(self):
        check_x = -self.camera_x
        for chunk in self.chunk_queue:
            chunk_start = chunk.x - CHUNK_TYPE_CHECK_OFFSET
            if chunk_start <= check_x <= chunk_start + self.chunk_spacing:
                if chunk.has_rail:
                    return 'rail'
                if chunk.has_pad:
                    return 'pad'
        return None
    
    def update_camera(self):
        self.cycle_chunks()
