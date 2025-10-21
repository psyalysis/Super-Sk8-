"""Clean input handling system separated from game logic."""

import time
import config
import pygame
from typing import Dict, List, Optional, Tuple


class DoubleTapTracker:
    def __init__(self, window_ms: float = 300):
        self.window_ms = window_ms
        self.last_key = ["none", 0]
        self.double_tapped_actions = set()
    
    def check_double_tap(self, key: int, action: str) -> bool:
        current_time = time.time()
        
        if (self.last_key[0] == key and 
            self.last_key[1] != 0 and 
            current_time - self.last_key[1] <= self.window_ms / 1000):
            
            self.double_tapped_actions.add(action)
            self.last_key = [key, current_time]
            return True
        
        self.last_key = [key, current_time]
        return False
    
    def clear_action(self, action: str):
        self.double_tapped_actions.discard(action)
    
    def is_action_double_tapped(self, action: str) -> bool:
        return action in self.double_tapped_actions


class InputHandler:
    def __init__(self):
        self.keys_held = [["none", False], ["none", False]]
        self.previous_keys_held = [["none", False], ["none", False]]
        self.double_tap_tracker = DoubleTapTracker()
    
    def process_key_down(self, key: int) -> Dict:
        if key not in config.KEY_MAPPINGS:
            return {}
        
        action = config.KEY_MAPPINGS[key]
        is_double_tap = self.double_tap_tracker.check_double_tap(key, action)
        
        if "left-" in action:
            self.keys_held[0] = [action, True]
        if "right-" in action:
            self.keys_held[1] = [action, True]
        
        return {
            'action': action,
            'is_double_tap': is_double_tap,
            'keys_held': self.keys_held.copy(),
            'double_tapped_actions': self.double_tap_tracker.double_tapped_actions.copy()
        }
    
    def process_key_up(self, key: int) -> Dict:
        if key not in config.KEY_MAPPINGS:
            return {}
        
        action = config.KEY_MAPPINGS[key]
        
        if "left-" in action:
            self.keys_held[0] = ["none", False]
            self.double_tap_tracker.clear_action(action)
        if "right-" in action:
            self.keys_held[1] = ["none", False]
            self.double_tap_tracker.clear_action(action)
        
        return {
            'action': action,
            'keys_held': self.keys_held.copy(),
            'double_tapped_actions': self.double_tap_tracker.double_tapped_actions.copy()
        }
    
    def get_active_combos(self) -> List[Tuple[str, str]]:
        left_key = self.keys_held[0][0] if self.keys_held[0][0] != "none" else "none"
        right_key = self.keys_held[1][0] if self.keys_held[1][0] != "none" else "none"
        
        if left_key != "none" and right_key != "none":
            return [(left_key, right_key)]
        return []
    
    def has_combo_changed(self) -> bool:
        if (self.keys_held[0][0] != "none" and self.keys_held[1][0] != "none"):
            return self.keys_held != self.previous_keys_held
        return False
    
    def update(self):
        self.previous_keys_held = self.keys_held.copy()