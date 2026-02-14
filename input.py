"""Keyboard input handling."""
import pygame
from enum import Enum, auto
import config


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

# Maps all the keys to which foot and what direction
KEY_MAP = {
    pygame.K_w: ('left', Direction.UP),
    pygame.K_s: ('left', Direction.DOWN),
    pygame.K_a: ('left', Direction.LEFT),
    pygame.K_d: ('left', Direction.RIGHT),
    pygame.K_i: ('right', Direction.UP),
    pygame.K_k: ('right', Direction.DOWN),
    pygame.K_j: ('right', Direction.LEFT),
    pygame.K_l: ('right', Direction.RIGHT),
}


class Input:
    def __init__(self):
        """Initialize the Input class with the keys held and all the pressed keys"""
        self.keys_held = {"left": None, "right": None}
        self.pressed_keys = {"left": [], "right": []}

    def get_active_trick(self):
        """Get the flip trick key combination that is currently being held"""
        return self.check_trick_input()
    
    def get_active_grind(self):
        """Get the grind key combination that is currently being held"""
        return self.check_grind_input()

    def handle_input(self, event):
        """Handle the input event - Called by the main loop"""
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)
        elif event.type == pygame.KEYUP:
            self.handle_keyup(event.key)

    def handle_keydown(self, key):
        """Handles Pressing a Key Down"""
        if key in KEY_MAP:
            hand, direction = KEY_MAP[key]

            if key not in self.pressed_keys[hand]:
                self.pressed_keys[hand].append(key)
            self.keys_held[hand] = direction.name

    def handle_keyup(self, key):
        """Handles Releasing a Key"""
        if key in KEY_MAP:
            hand, direction = KEY_MAP[key]

            if key in self.pressed_keys[hand]:
                self.pressed_keys[hand].remove(key)

            if self.pressed_keys[hand]:
                last_key = self.pressed_keys[hand][-1]
                _, new_direction = KEY_MAP[last_key]
                self.keys_held[hand] = new_direction

            else:
                self.keys_held[hand] = None

    def check_trick_input(self):
        """[Iteration] Check if current input matches any FLIP TRICK pattern."""
        return next((trick for trick, pattern in config.TRICK_MAP.items() if self.keys_held == pattern), None)

    def check_grind_input(self):
        """[Iteration] Check if current input matches any GRIND pattern."""
        return next((grind for grind, pattern in config.GRIND_MAP.items() if self.keys_held == pattern), None)