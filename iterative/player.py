import pygame
import config
from enum import Enum


class PlayerState(Enum):
    """Player movement states."""
    GROUNDED = "grounded"
    AIRBORNE = "airborne"
    GRINDING = "grinding"


class Player:
    # Player configuration constants
    INITIAL_X = 100
    INITIAL_Y = 100
    JUMP_OFFSET = -80  # Vertical offset when jumping (pixels)
    MAX_HANG_TIME = 1.5  # Maximum air time (seconds)
    GRIND_WINDOW = 0.5  # Time window to input grind when near rail (seconds)
    LANDING_WINDOW = 0  # Time window after releasing trick input before landing (seconds)
    PLAYER_WIDTH = 40
    PLAYER_HEIGHT = 60
    
    # Visual state colors
    COLOR_GROUNDED = (0, 255, 0)  # Green
    COLOR_AIRBORNE = (255, 255, 0)  # Yellow
    COLOR_GRINDING = (255, 0, 0)  # Red
    
    def __init__(self):
        self.iso_pos = pygame.Vector2(self.INITIAL_X, self.INITIAL_Y)
        
        self.state = PlayerState.GROUNDED
        self.air_timer = 0.0
        self.landing_timer = 0.0
        
        self.current_trick = None
        self.previous_trick = None
        self.trick_combo = []
        
        self.rect = pygame.Rect(0, 0, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)

    def _pop(self):
        """Switch to airborne state and initialize trick combo."""
        self.state = PlayerState.AIRBORNE
        self.air_timer = self.MAX_HANG_TIME
        self.landing_timer = 0
        self.trick_combo = [self.current_trick] if self.current_trick else []
        print(f"Start: {self.current_trick}")

    def update(self, dt, active_trick, active_grind, level):
        """Update player state and physics."""
        trick_released = self.previous_trick is not None and active_trick is None
        self.previous_trick = active_trick
        self.current_trick = active_trick

        if active_trick and self.state == PlayerState.GROUNDED:
            self._pop()

        chunk_type = level.get_current_chunk_type()
        
        if self.state == PlayerState.AIRBORNE:
            self._update_airborne_state(dt, chunk_type, active_grind, trick_released)
        elif self.state == PlayerState.GRINDING:
            self._update_grinding_state(chunk_type, active_grind)
        
        self._calculate_screen_position()
    
    def _update_airborne_state(self, dt, chunk_type, active_grind, trick_released):
        """Handle airborne state updates."""
        self.air_timer -= dt

        #config.print_debug(f"\n \n \nAir timer: {self.air_timer} \n Chunk type: {chunk_type} \n Trick released: {trick_released} \n Active grind: {active_grind}")

        if trick_released:
            if chunk_type == "rail":
                self.landing_timer = self.GRIND_WINDOW
            else:
                self.landing_timer = 0
                self.air_timer = 0

        # Check for grind during landing window (after trick is released)
        if chunk_type == "rail" and active_grind and self.landing_timer > 0:
            self._start_grind(active_grind)
            print(f"Start grind: {active_grind}")
            return
        
        if self.landing_timer > 0:
            self.landing_timer -= dt
            if self.landing_timer <= 0:
                self._land()
                return
        
        if self.air_timer <= 0:
            self._land()
            return
    
    def _update_grinding_state(self, chunk_type, active_grind):
        """Handle grinding state updates."""
        if chunk_type != "rail" or not active_grind:
            self._land()
    
    def _start_grind(self, active_grind):
        """Transition from airborne to grinding state."""
        self.state = PlayerState.GRINDING
        self.trick_combo.append(active_grind)
        self.landing_timer = 0

    def _land(self):
        """Land on the ground and reset state."""
        self.state = PlayerState.GROUNDED
        self.air_timer = 0
        self.landing_timer = 0
        self.current_trick = None
        self.previous_trick = None
        print(f"Land: {self.trick_combo}")

    def _calculate_screen_position(self):
        """Update screen position based on current state."""
        draw_y = self.iso_pos.y + (self.JUMP_OFFSET if self.state == PlayerState.AIRBORNE else 0)
        self.rect.topleft = (self.iso_pos.x, draw_y)

    def draw(self, screen, graphics=None):
        """Draw the player - delegates to graphics if available."""
        if graphics:
            # Graphics handles sprite rendering
            return
        
        # Fallback: colored rectangle (for debugging)
        color_map = {
            PlayerState.GROUNDED: self.COLOR_GROUNDED,
            PlayerState.AIRBORNE: self.COLOR_AIRBORNE,
            PlayerState.GRINDING: self.COLOR_GRINDING,
        }
        player_color = color_map.get(self.state, self.COLOR_GROUNDED)
        pygame.draw.rect(screen, player_color, self.rect)