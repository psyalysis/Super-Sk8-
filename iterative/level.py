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

        # 2. Level Properties
        self.chunks = []
        self.scroll_speed = 300  
        self.chunk_width = 291 # Match your texture width
        
        # Initialize chunks
        for i in range(5):
            self.chunks.append(self._generate_chunk(i * self.chunk_width))

    def _generate_chunk(self, x):
        """Creates a data structure for each floor segment."""
        # Isometric Y calculation to keep the path tilted
        y = (x // 2) + 300 
        return {
            "pos": pygame.Vector2(x, y),
            "type": random.choice([None, "rail", None])
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
            self.chunks.pop(0)
            self.chunks.append(self._generate_chunk(last_chunk_x + self.chunk_width))

    def get_current_chunk_type(self):
        """Check what is under the player (assumed X position 150)."""
        player_x = 150
        for chunk in self.chunks:
            if chunk["pos"].x <= player_x <= chunk["pos"].x + self.chunk_width:
                return chunk["type"]
        return None

    def draw(self):
        """Draw the actual images to the screen."""
        for chunk in self.chunks:
            self.screen.blit(self.floor_image, (chunk["pos"].x, chunk["pos"].y))
            
            # Debug: Draw a red line if it's a rail chunk
            if chunk["type"] == "rail":
                # Offset the line so it looks like it's 'on' the isometric chunk
                start = (chunk["pos"].x + 50, chunk["pos"].y + 25)
                end = (chunk["pos"].x + 250, chunk["pos"].y + 125)
                pygame.draw.line(self.screen, (255, 0, 0), start, end, 5)