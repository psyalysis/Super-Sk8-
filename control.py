"""Skateboard rendering / controls module."""

import config
import pygame
import os
import time
import random


class Control:
    def __init__(self, display, main):
        self.keys_held = [["none", False], ["none", False]]  # Left key, Right key
        self.previous_keys_held = [["none", False], ["none", False]]
        self.main = main

        # Simple double-tap tracking
        self.last_key = ["none", 0]  # [key, timestamp]
        self.double_tap_window = 0.3  # 300ms window
        self.is_double_tap = False
        
        # Track which actions have been double-tapped (persistent until keys released)
        self.double_tapped_actions = set()
        
        self.trigger_key_combo = [["none", False], ["none", False]]
        
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
                # Use trick name without extension as key
                trick_name = filename[:-4]  # Remove .png extension
                self.animations[trick_name] = pygame.image.load(full_path)
        
        print(f"Loaded animations: {list(self.animations.keys())}")

    def handle_key_down(self, key, player_state):
        """
        Handles the key press event by held down by the user and passes the action (if any) to the handle_control method.
        """
        if key in config.KEY_MAPPINGS:
            action = config.KEY_MAPPINGS[key]
            current_time = time.time()
            
            # Check for double-tap
            if (self.last_key[0] == key and 
                self.last_key[1] != 0 and 
                current_time - self.last_key[1] <= self.double_tap_window):
                
                # Double tap detected!
                self.is_double_tap = True
                self.double_tapped_actions.add(action)  # Remember this action was double-tapped
                print(f"Double tap detected for key {key} ({action})")
                
                # Set the appropriate key as held
                if "left-" in action:
                    self.keys_held[0] = [action, True]
                if "right-" in action:
                    self.keys_held[1] = [action, True]
                
                # Trigger trick combo check with double tap info
                self.handle_control(self.keys_held, player_state, is_double_tap=True, key=key)
            else:
                # Single tap or first tap
                self.is_double_tap = False
                
                # Set the appropriate key as held
                if "left-" in action:
                    self.keys_held[0] = [action, True]
                if "right-" in action:
                    self.keys_held[1] = [action, True]
                
                # Check for trick combos (including non-double-tap tricks)
                print(f"Single tap: {action}, Current double-tapped: {self.double_tapped_actions}")
                self.handle_control(self.keys_held, player_state, is_double_tap=False, key=key)
            
            # Update last key tracking
            self.last_key = [key, current_time]
            
    def handle_key_up(self, key, player_state):
        if key in config.KEY_MAPPINGS:
            action = config.KEY_MAPPINGS[key]
            if "left-" in action:
                self.keys_held[0] = ["none", False]
                # Clear double-tap state for this action when released
                self.double_tapped_actions.discard(action)
            if "right-" in action:
                self.keys_held[1] = ["none", False]
                # Clear double-tap state for this action when released
                self.double_tapped_actions.discard(action)
            self.handle_control(self.keys_held, player_state, key=key)
        
    def handle_control(self, action, player_state, is_double_tap=False, key=None):
        if player_state == "rolling":
            self.handle_trick_combo(action, is_double_tap, key)
        if player_state == "airborne":
            self.handle_trick_combo_end(action, key)
        
    
    def update(self):
        # Reset double tap state after window expires
        current_time = time.time()
        if self.last_key[1] != 0 and current_time - self.last_key[1] > self.double_tap_window:
            self.is_double_tap = False
        
        # Check if both keys are held and combination has changed
        if self.keys_held[0][0] != "none" and self.keys_held[1][0] != "none":
            if self.keys_held != self.previous_keys_held:
                print(f"UPDATE: Both keys held - {self.keys_held[0][0]} + {self.keys_held[1][0]}, Double-tapped: {self.double_tapped_actions}")
                self.handle_control(self.keys_held, self.main.player_state)
            
        self.previous_keys_held = self.keys_held.copy()
    
    def get_pygame_key_from_action(self, action):
        """
        Helper method to get pygame key from action string.
        """
        for pygame_key, action_string in config.KEY_MAPPINGS.items():
            if action_string == action:
                return pygame_key
        return None
    
    def handle_trick_combo(self, keys_held, is_double_tap=False, key=None):
        """
        Handles the key combo for the game based on the action.
        Triggers tricks when specific key combinations are held.
        """
        left_key = keys_held[0][0] if keys_held[0][0] != "none" else "none"
        right_key = keys_held[1][0] if keys_held[1][0] != "none" else "none"
        
        # Get the action string for the double-tapped key
        double_tapped_action = config.KEY_MAPPINGS.get(key, None) if is_double_tap else None
        
        # Check each trick configuration
        # First pass: Check double-tap tricks (prioritize them)
        double_tap_tricks = []
        regular_tricks = []
        
        for trick_name, config_data in config.FLIP_CONTROLS.items():
            required_keys = config_data["keys"]
            left_needs_double = required_keys[0][1]
            right_needs_double = required_keys[1][1]
            
            # Categorize tricks
            if left_needs_double or right_needs_double:
                double_tap_tricks.append((trick_name, config_data))
            else:
                regular_tricks.append((trick_name, config_data))
        
        print(f"Checking tricks for combo: {left_key} + {right_key}")
        print(f"Double-tap tricks to check: {[name for name, _ in double_tap_tricks]}")
        print(f"Regular tricks to check: {[name for name, _ in regular_tricks]}")
        
        # Check double-tap tricks first
        for trick_name, config_data in double_tap_tricks:
            required_keys = config_data["keys"]
            
            # Extract key names and double-tap requirements
            left_required = required_keys[0][0]  # Key name
            left_needs_double = required_keys[0][1]  # Boolean
            right_required = required_keys[1][0]  # Key name  
            right_needs_double = required_keys[1][1]  # Boolean
            
            # Check if current key combination matches this trick
            if left_key == left_required and right_key == right_required:
                # Check double-tap requirements using persistent tracking
                left_double_ok = not left_needs_double or (left_required in self.double_tapped_actions)
                right_double_ok = not right_needs_double or (right_required in self.double_tapped_actions)
                
                if left_double_ok and right_double_ok:
                    print(f"✅ DOUBLE-TAP TRICK TRIGGERED: {trick_name}")
                    print(f"   Key combo: {left_key}{' (double)' if left_needs_double else ''} + {right_key}{' (double)' if right_needs_double else ''}")
                    print(f"   Double-tapped actions: {self.double_tapped_actions}")
                    self.trigger_key_combo = [left_key, right_key]
                    self.execute_trick(trick_name)
                    return
                else:
                    print(f"❌ Double-tap trick {trick_name} failed:")
                    print(f"   Required: {left_required}{' (double)' if left_needs_double else ''} + {right_required}{' (double)' if right_needs_double else ''}")
                    print(f"   Current: {left_key}{' (double)' if left_needs_double else ''} + {right_key}{' (double)' if right_needs_double else ''}")
                    print(f"   Left OK: {left_double_ok}, Right OK: {right_double_ok}")
                    print(f"   Double-tapped actions: {self.double_tapped_actions}")
        
        # Then check regular tricks
        for trick_name, config_data in regular_tricks:
            required_keys = config_data["keys"]
            
            # Extract key names and double-tap requirements
            left_required = required_keys[0][0]  # Key name
            left_needs_double = required_keys[0][1]  # Boolean
            right_required = required_keys[1][0]  # Key name  
            right_needs_double = required_keys[1][1]  # Boolean
            
            # Check if current key combination matches this trick
            if left_key == left_required and right_key == right_required:
                # Check double-tap requirements using persistent tracking
                left_double_ok = not left_needs_double or (left_required in self.double_tapped_actions)
                right_double_ok = not right_needs_double or (right_required in self.double_tapped_actions)
                
                if left_double_ok and right_double_ok:
                    print(f"✅ REGULAR TRICK TRIGGERED: {trick_name}")
                    print(f"   Key combo: {left_key}{' (double)' if left_needs_double else ''} + {right_key}{' (double)' if right_needs_double else ''}")
                    print(f"   Double-tapped actions: {self.double_tapped_actions}")
                    self.trigger_key_combo = [left_key, right_key]
                    self.execute_trick(trick_name)
                    return
                else:
                    print(f"❌ Regular trick {trick_name} failed:")
                    print(f"   Required: {left_required}{' (double)' if left_needs_double else ''} + {right_required}{' (double)' if right_needs_double else ''}")
                    print(f"   Current: {left_key}{' (double)' if left_needs_double else ''} + {right_key}{' (double)' if right_needs_double else ''}")
                    print(f"   Left OK: {left_double_ok}, Right OK: {right_double_ok}")
                    print(f"   Double-tapped actions: {self.double_tapped_actions}")
    
    def handle_trick_combo_end(self, keys_held, key=None):
        """
        Handle when trick combo keys are released.
        """
        # Check if any of the currently held keys were part of the triggered combo
        if key and key in config.KEY_MAPPINGS:
            action = config.KEY_MAPPINGS[key]
            if action in self.trigger_key_combo:
                self.trigger_key_combo = ["none", "none"]
                self.main.player_state = "rolling"
                self.main.display.stop_animation()
                pygame.mixer.Sound(config.SOUND_PATHS["land"] + str(random.randint(1, 5)) + ".wav").play()
                self.main.debug.info(f"Trick combo ended with key {key}")
        elif keys_held[0][0] == "none" and keys_held[1][0] == "none":
            # Both keys released
            self.trigger_key_combo = ["none", "none"]
            self.main.player_state = "rolling"
            self.main.display.stop_animation()
            pygame.mixer.Sound(config.SOUND_PATHS["land"] + str(random.randint(1, 5)) + ".wav").play()
            self.main.debug.info("Trick combo ended - both keys released")
    
    def execute_trick(self, trick_name):
        """
        Executes the specified trick.
        """
        self.main.player_state = "airborne"

        # Get the animation sprite for this trick
        if trick_name not in self.animations:
            print(f"❌ ERROR: Animation not found for trick '{trick_name}'")
            print(f"Available animations: {list(self.animations.keys())}")
            return
        
        animation = self.animations[trick_name]
        
        # Start the animation with looping enabled (will loop while keys are held)
        self.main.display.start_animation(trick_name, animation, loop=True)

        # Play a random SFX/pop_(1-6).wav
        random_sfx = random.randint(1, 6)
        pygame.mixer.Sound(config.SOUND_PATHS["pop"] + str(random_sfx) + ".wav").play()
        
        print(f"Executing trick: {trick_name}")
        
        # Add your trick execution logic here
        # For example:
        # - Add points
        # - Update game state
        # - Trigger effects
        
        # Example integration points:
        if hasattr(self.main, 'skateboard'):
            # Trigger trick on skateboard object
            pass
        if hasattr(self.main, 'score'):
            # Add points for trick
            pass