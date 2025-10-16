"""Skateboard rendering / controls module."""

import config
import pygame
import os


class Control:
    def __init__(self, display, main):
        self.keys_held = ["none", "none"]  # Left key, Right key
        self.previous_keys_held = ["none", "none"]
        self.main = main
        self.load_animations()
        
    def load_animations(self):
        """
        Loads the animations for the tricks.
        """
        
        self.animations = {}
        animations_path = config.ANIMATIONS
        for filename in os.listdir(animations_path):
            if filename.endswith(".png"):
                full_path = os.path.join(animations_path, filename)
                self.animations[filename] = pygame.image.load(full_path)

    def handle_key_down(self, key, player_state):
        """
        Handles the key press event by held down by the user and passes the action (if any) to the handle_control method.
        """
        if key in config.KEY_MAPPINGS:
            action = config.KEY_MAPPINGS[key]
            if "left-" in action:
                self.keys_held[0] = action
            if "right-" in action:
                self.keys_held[1] = action
            self.handle_control(self.keys_held, player_state)
            
    def handle_key_up(self, key, player_state):
        if key in config.KEY_MAPPINGS:
            action = config.KEY_MAPPINGS[key]
            if "left-" in action:
                self.keys_held[0] = "none"
            if "right-" in action:
                self.keys_held[1] = "none"
            self.handle_control(self.keys_held, player_state)
        
    def handle_control(self, action, player_state):
        if player_state == "rolling":
            self.handle_trick_combo(action)
        
    
    def update(self):
        # Check if both keys are held and combination has changed
        if self.keys_held[0] != "none" and self.keys_held[1] != "none":
            if self.keys_held != self.previous_keys_held:
                self.handle_control(self.keys_held, self.main.player_state)
            
        self.previous_keys_held = self.keys_held.copy()
    
    def handle_trick_combo(self, keys_held):
        """
        Handles the key combo for the game based on the action.
        Triggers tricks when specific key combinations are held.
        """
        left_key = keys_held[0]
        right_key = keys_held[1]
        
        # Check for trick combinations
        if left_key == "left-left" and right_key == "right-down":
            self.execute_trick("Kickflip")
        elif left_key == "left-left" and right_key == "right-up":
            self.execute_trick("Heelflip")
        elif left_key == "left-down" and right_key == "right-down":
            self.execute_trick("VKickflip")
        elif left_key == "left-up" and right_key == "right-up":
            self.execute_trick("VHeelflip")
        elif left_key == "left-down" and right_key == "right-left":
            self.execute_trick("BS-Shuv")
        elif left_key == "left-up" and right_key == "right-right":
            self.execute_trick("FS-Shuv")
    
    def execute_trick(self, trick_name):
        """
        Executes the specified trick.
        This is where you'd integrate with your game's trick system.
        """
        self.main.debug.info(f"Executing trick: {trick_name}")
        self.main.player_state = "airborne"

        animation = self.animations[trick_name]
        self.main.display.draw_animation(animation, self.main.player_position, self.main.player_angle)

        
        # Add your trick execution logic here
        # For example:
        # - Play trick animation
        # - Add points
        # - Play sound effects
        # - Update game state
        
        # Example integration points:
        if hasattr(self.main, 'skateboard'):
            # Trigger trick on skateboard object
            pass
        if hasattr(self.main, 'score'):
            # Add points for trick
            pass