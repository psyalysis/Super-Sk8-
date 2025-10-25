"""Skateboard rendering / controls module."""

import config
import pygame
import os
import time
import random
from core.state_manager import StateManager
from tricks import TrickManager


class Control:
    def __init__(self, display, state_manager, input_handler, debug=None, ui=None, sound_manager=None):
        self.display = display
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.debug = debug
        self.ui = ui
        self.sound_manager = sound_manager
        
        # Initialize trick manager
        self.trick_manager = TrickManager(display, state_manager, ui, sound_manager)
        
        self.load_animations()
        
    def load_animations(self):
        self.animations = {}
        animations_path = config.ANIMATIONS
        for filename in os.listdir(animations_path):
            if filename.endswith(".png"):
                full_path = os.path.join(animations_path, filename)
                trick_name = filename[:-4]
                self.animations[trick_name] = pygame.image.load(full_path)

    def handle_input(self, input_data):
        if self.state_manager.is_in_menu():
            self.handle_menu_input(input_data)
        elif self.state_manager.is_player_rolling():
            self.handle_trick_combo(input_data)
        elif self.state_manager.is_player_airborne():
            self.handle_trick_combo_end(input_data)

    def update(self):
        if self.input_handler.has_combo_changed():
            combos = self.input_handler.get_active_combos()
            if combos:
                input_data = {
                    'keys_held': self.input_handler.keys_held,
                    'double_tapped_actions': self.input_handler.double_tap_tracker.double_tapped_actions
                }
                self.handle_trick_combo(input_data)
        
        # Update trick progress
        self.trick_manager.update_trick_progress()
        
        # Check if trick failed due to timing (1.5 loops)
        if (self.trick_manager.current_trick and 
            self.trick_manager.trick_completed and 
            self.state_manager.is_player_airborne()):
            # Trick failed automatically - end the trick
            self.state_manager.end_trick()
            self.display.stop_animation()
            self.trick_manager.reset_trick()
            
            # Play landing sound using sound manager
            if self.sound_manager:
                self.sound_manager.play_land_sound()
        
        # Update UI trick display
        if self.ui:
            self.ui.update_trick_display()
    
    def handle_trick_combo(self, input_data):
        keys_held = input_data.get('keys_held', [["none", False], ["none", False]])
        double_tapped_actions = input_data.get('double_tapped_actions', set())
        
        left_key = keys_held[0][0] if keys_held[0][0] != "none" else "none"
        right_key = keys_held[1][0] if keys_held[1][0] != "none" else "none"
        
        # Check double-tap tricks first
        double_tap_tricks = []
        regular_tricks = []
        
        for trick_name, config_data in config.FLIP_CONTROLS.items():
            required_keys = config_data["keys"]
            left_needs_double = required_keys[0][1]
            right_needs_double = required_keys[1][1]
            
            if left_needs_double or right_needs_double:
                double_tap_tricks.append((trick_name, config_data))
            else:
                regular_tricks.append((trick_name, config_data))
        
        # Check double-tap tricks first
        for trick_name, config_data in double_tap_tricks:
            required_keys = config_data["keys"]
            left_required = required_keys[0][0]
            left_needs_double = required_keys[0][1]
            right_required = required_keys[1][0]
            right_needs_double = required_keys[1][1]
            
            if left_key == left_required and right_key == right_required:
                left_double_ok = not left_needs_double or (left_required in double_tapped_actions)
                right_double_ok = not right_needs_double or (right_required in double_tapped_actions)
                
                if left_double_ok and right_double_ok:
                    self.execute_trick(trick_name)
                    return
        
        # Check regular tricks
        for trick_name, config_data in regular_tricks:
            required_keys = config_data["keys"]
            left_required = required_keys[0][0]
            left_needs_double = required_keys[0][1]
            right_required = required_keys[1][0]
            right_needs_double = required_keys[1][1]
            
            if left_key == left_required and right_key == right_required:
                left_double_ok = not left_needs_double or (left_required in double_tapped_actions)
                right_double_ok = not right_needs_double or (right_required in double_tapped_actions)
                
                if left_double_ok and right_double_ok:
                    self.execute_trick(trick_name)
                    return
    
    def handle_trick_combo_end(self, input_data):
        keys_held = input_data.get('keys_held', [["none", False], ["none", False]])
        
        # Check for successful trick completion
        self.trick_manager.check_keys_released(keys_held)
        
        if keys_held[0][0] == "none" and keys_held[1][0] == "none":
            # Check if trick was successful or failed
            if self.trick_manager.trick_completed:
                # Trick was successful - UI already updated by trick manager
                pass
            else:
                # Trick failed - show fail message
                if self.ui and self.trick_manager.current_trick:
                    self.ui.show_trick_fail(self.trick_manager.current_trick)
                
                # Show red board feedback
                self.display.show_board_color_feedback('red')
            
            self.state_manager.end_trick()
            self.display.stop_animation()
            self.trick_manager.reset_trick()
            
            # Play landing sound using sound manager
            if self.sound_manager:
                self.sound_manager.play_land_sound()
    
    def execute_trick(self, trick_name):
        self.state_manager.start_trick()

        if trick_name not in self.animations:
            return
        
        animation = self.animations[trick_name]
        self.display.start_animation(trick_name, animation, loop=True)
        
        # Start tracking this trick
        self.trick_manager.start_trick(trick_name)
        
        # Show trick start in UI
        if self.ui:
            self.ui.show_trick_start(trick_name)

        # Play pop sound using sound manager
        if self.sound_manager:
            self.sound_manager.play_pop_sound()
        
        
        # Log trick execution
        if self.debug:
            self.debug.log_trick(trick_name)
    
    def handle_menu_input(self, input_data):
        """Handle input when in menu state."""
        action = input_data.get('action', '')
        
        if action == 'enter':
            # Start the game
            self.state_manager.start_game()
            # Show skateboard and trigger camera shake
            self.display.show_skateboard()
            self.display.add_camera_shake(5.0, 0.5)  # Intensity 5, duration 0.5 seconds
            print("Game started!")
        elif action == 'escape':
            # Exit the game
            import pygame
            pygame.event.post(pygame.event.Event(pygame.QUIT))