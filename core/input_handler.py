"""Clean input handling system."""

import time
import config
import pygame


class InputHandler:
    def __init__(self):
        self.keys_held = [["none", False], ["none", False]]
        self.previous_keys_held = [["none", False], ["none", False]]
    
    def process_key_down(self, key):
        if key not in config.KEY_MAPPINGS:
            return {}
        
        action = config.KEY_MAPPINGS[key]
        
        if "left-" in action:
            self.keys_held[0] = [action, True]
        if "right-" in action:
            self.keys_held[1] = [action, True]
        
        return {
            'action': action,
            'keys_held': self.keys_held.copy()
        }
    
    def process_key_up(self, key):
        if key not in config.KEY_MAPPINGS:
            return {}
        
        action = config.KEY_MAPPINGS[key]
        
        if "left-" in action:
            self.keys_held[0] = ["none", False]
        if "right-" in action:
            self.keys_held[1] = ["none", False]
        
        return {
            'action': action,
            'keys_held': self.keys_held.copy()
        }
    
    def get_active_combos(self):
        left_key = self.keys_held[0][0] if self.keys_held[0][0] != "none" else "none"
        right_key = self.keys_held[1][0] if self.keys_held[1][0] != "none" else "none"
        
        if left_key != "none" and right_key != "none":
            return [(left_key, right_key)]
        return []
    
    def has_combo_changed(self):  # Fixed: Restored comparison with previous_keys_held to only trigger on actual combo changes
        if (self.keys_held[0][0] != "none" and self.keys_held[1][0] != "none"):
            return self.keys_held != self.previous_keys_held
        return False
    
    def update(self):  # Fixed: Restored previous_keys_held update to track combo changes
        self.previous_keys_held = self.keys_held.copy()
