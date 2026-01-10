""" Handles keyboard controls for the system. """
import pygame
from enum import Enum, auto

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

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

class Control:
    def __init__(self):
        self.keys_held = {"left": None, "right": None}
        self.pressed_keys = {"left": [], "right": []}
    
    def handle_keydown(self, key):
        print(f"Key down: {key}")
        
        if key in KEY_MAP:
            hand, direction = KEY_MAP[key]
            # Add to end if not already in list
            if key not in self.pressed_keys[hand]:
                self.pressed_keys[hand].append(key)
            self.keys_held[hand] = direction.name
            print(f"Keys held: {self.keys_held}")
    
    def handle_keyup(self, key):
        print(f"Key up: {key}")
        
        if key in KEY_MAP:
            hand, direction = KEY_MAP[key]
            if key in self.pressed_keys[hand]:
                self.pressed_keys[hand].remove(key)
            
            # Fallback to next still held key 
            if self.pressed_keys[hand]:
                last_key = self.pressed_keys[hand][-1]
                _, new_direction = KEY_MAP[last_key]
                self.keys_held[hand] = new_direction.name
            else:
                self.keys_held[hand] = None
            
            print(f"Keys held: {self.keys_held}")