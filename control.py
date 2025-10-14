"""Skateboard rendering / controls module."""

import config
import pygame

# Left key, Right key
keys_held = ["none", "none"]

keys_held_duration = 0

previous_keys_held = ["none", "none"]

class Control:
    def __init__(self, display, main):
        self.keys_held = []
        self.main = main
        
    def handle_key_down(self, key):
        """
        Handles the key press event by held down by the user and passes the action (if any) to the handle_control method.
        """
        if key in config.KEY_MAPPINGS:
            action = config.KEY_MAPPINGS[key]
            if "left-" in action:
                keys_held[0] = action
            if "right-" in action:
                keys_held[1] = action
            self.handle_control(keys_held)
            
    def handle_key_up(self, key):
        if key in config.KEY_MAPPINGS:
            action = config.KEY_MAPPINGS[key]
            if action in keys_held:
                if "left-" in action:
                    keys_held[0] = "none"
                if "right-" in action:
                    keys_held[1] = "none"
                self.handle_control(keys_held)
        
    def handle_control(self, action):
        """
        Handles the controls for the game based on the action.

        Actions are:
        - right-up
        - right-down
        - right-left
        - right-right
        
        - left-up
        - left-down
        - left-left
        - left-right
        
        - enter
        - escape
        """
        
        self.main.debug.info("Handling control: " + str(keys_held))
    
    def update(self):
        if keys_held[0] != "none" and keys_held[1] != "none":
            if keys_held != previous_keys_held:
                keys_held_duration = 0
            else:
                keys_held_duration += 1
                self.handle_key_combo(self, keys_held, keys_held_duration)
        previous_keys_held = keys_held
    
    def handle_key_combo(self, keys_held):
        """
        Handles the key combo for the game based on the action.
        """
        if keys_held[0] == "left-left" and keys_held[1] == "right-down":
            trick = "Kickflip"
        elif keys_held[0] == "left-left" and keys_held[1] == "right-up":
            trick = "Heelflip"
        elif keys_held[0] == "left-down" and keys_held[1] == "right-down":
            trick = "Varial Kickflip"
        elif keys_held[0] == "left-up" and keys_held[1] == "right-up":
            trick = "Varial Heelflip"
        elif keys_held[0] == "left-up" and keys_held[1] == "right-down":
            trick = "Nollie Kickflip"
        elif keys_held[0] == "left-up" and keys_held[1] == "right-up":
            trick = "Nollie Heelflip"
            