import pygame
import random
import config

class Level:
    def __init__(self, screen):
        self.screen = screen
        
        # 1. Load the floor texture
        # Using a relative path as specified
        try:
            self.floor_image = pygame.image.load("./assets/level/floorChunk.png").convert_alpha()
        except pygame.error:
            print("Warning: Could not find floorChunk.png. Ensure you are running from the correct directory")
        try:
            self.rail_image = pygame.image.load("./assets/level/railBlend.png").convert_alpha()
        except pygame.error:
            print("Warning: Could not find railBlend.png. Ensure you are running from the correct directory")

        # 2. Level Properties
        self.chunks = []
        self.rail_chunks = []
        self.scroll_speed = 291  
        self.chunk_width = 291 # Match your texture width

        # spacing adjustments: reduce horizontal gap by 40 px and vertical gap by 20 px
        self.spacing_x = self.chunk_width - 41
        self.spacing_y = (self.spacing_x / 2)
        self.base_y = 100
        
        # Initialize chunks
        for i in range(5):
            x = i * self.spacing_x
            y = self.base_y + i * self.spacing_y
            self.chunks.append(self._generate_chunk(x, y))

    def _generate_chunk(self, x, y):
        """Creates a data structure for each floor segment."""
        return {
            "pos": pygame.Vector2(x, y),
            "type": random.choice([None, "rail", None, None])
        }

    def update(self, dt):
        """Move chunks based on delta time to create a conveyor belt effect."""
        for chunk in self.chunks:
            # Move X and Y based on isometric 2:1 ratio
            chunk["pos"].x -= self.scroll_speed * dt
            chunk["pos"].y -= (self.scroll_speed / 2) * dt

        # Recycle logic: If chunk is completely off screen, move to end
        if self.chunks[0]["pos"].x < -self.chunk_width:
            last_chunk_x = self.chunks[-1]["pos"].x
            last_chunk_y = self.chunks[-1]["pos"].y
            self.chunks.pop(0)
            
            if chunk["type"] == "rail":
                self.rail_chunks.pop(0)
                
                
            new_x = last_chunk_x + self.spacing_x
            new_y = last_chunk_y + self.spacing_y
            self.chunks.append(self._generate_chunk(new_x, new_y))

    def get_current_chunk_type(self):
        """Check what is under the player (assumed X position 150)."""
        player_x = 0
        for chunk in self.chunks:
            if chunk["pos"].x <= player_x <= chunk["pos"].x + self.chunk_width:
                return chunk["type"]
        return None

    def draw(self):
        """Draw the actual images to the screen."""
        for chunk in self.chunks:
            if chunk["type"] == "rail":
                self.rail_chunks.append(chunk)
                
            self.screen.blit(self.floor_image, (chunk["pos"].x, chunk["pos"].y))
            
        for rail_chunk in self.rail_chunks:
            
            if rail_chunk["pos"].x > -self.chunk_width: #Render the ones still on screen
                start = (rail_chunk["pos"].x + 50, rail_chunk["pos"].y + 25)
                end = (rail_chunk["pos"].x + 250, rail_chunk["pos"].y + 125)
                self.screen.blit(self.rail_image, (start, end))
                