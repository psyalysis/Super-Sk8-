import pygame
import config

# State Constants
GROUNDED = "grounded"
AIRBORNE = "airborne"
GRINDING = "grinding"

class Player:
    def __init__(self):
        # Isometric Position (The "Shadow" position on the floor)
        self.iso_pos = pygame.Vector2(150, 450)
        
        # Instant Jump Settings
        self.jump_offset = -80  # How many pixels up the player "pops"
        self.hang_time = 0.6    # How many seconds they stay in the air
        
        # State Management
        self.state = GROUNDED
        self.air_timer = 0.0
        
        # Trick Data
        self.current_trick = None
        
        # Visuals
        self.width, self.height = 40, 60
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def handle_input(self, event):
        """Discrete event handling."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.state == GROUNDED:
                self._pop_up()

    def _pop_up(self):
        """Instantly switch to air state."""
        self.state = AIRBORNE
        self.air_timer = self.hang_time
        print("Pop!")

    def update(self, dt, active_trick, level):
        """Logic loop."""
        if self.state == AIRBORNE:
            # Countdown the hang time
            self.air_timer -= dt
            
            # Record trick while in air
            if active_trick:
                self.current_trick = active_trick
            
            # Check if it's time to land
            if self.air_timer <= 0:
                self._land(level)
        
        self._calculate_screen_position()

    def _land(self, level):
        """Snap back to ground and check for obstacles."""
        self.state = GROUNDED
        self.air_timer = 0
        
        # Ask level what we landed on
        chunk_type = level.get_current_chunk_type()
        
        if self.current_trick:
            print(f"Landed {self.current_trick} on {chunk_type if chunk_type else 'flat ground'}!")
        
        if chunk_type == 'rail':
            self.state = GRINDING
        
        self.current_trick = None

    def _calculate_screen_position(self):
        """Updates the rect for Pygame drawing."""
        # Start at the floor position
        draw_x = self.iso_pos.x
        draw_y = self.iso_pos.y
        
        # If jumping, instantly subtract the jump offset
        if self.state == AIRBORNE:
            draw_y += self.jump_offset
            
        self.rect.topleft = (draw_x, draw_y)

    def draw(self, screen):
        # Draw a small shadow to show ground position
        shadow_color = (50, 50, 50)
        pygame.draw.ellipse(screen, shadow_color, (self.iso_pos.x, self.iso_pos.y + 50, 40, 15))

        # Draw the player
        player_color = (0, 255, 0) # Default
        if self.state == AIRBORNE: player_color = (255, 255, 0)
        if self.state == GRINDING: player_color = (255, 0, 0)

        pygame.draw.rect(screen, player_color, self.rect)