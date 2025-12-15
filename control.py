"""Skateboard rendering / controls module."""

import config
import pygame
import os
import time
import random
from core.state_manager import StateManager
from tricks import TrickManager


class Control:
    def __init__(self, display, state_manager, input_handler, debug=None, ui=None, sound_manager=None, level=None):
        self.display = display
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.debug = debug
        self.ui = ui
        self.sound_manager = sound_manager
        self.level = level
        
        # Initialize trick manager
        self.trick_manager = TrickManager(display, state_manager, ui, sound_manager)
        
        # Grind window timer
        self.grind_window_start = None
        self.grind_window_duration = 0.25  # 0.25 seconds
        
        # Track if last trick was successful (needed for grind entry)
        self.last_trick_successful = False
        
        # Track grind grace period for transitioning between rails
        self.grind_off_rail_timer = None
        self.grind_off_rail_duration = 0.15  # 0.15 seconds grace period
        
        self.load_animations()
        
    def load_animations(self):
        self.animations = {}
        
        # Load flip trick animations
        flip_path = config.ANIMATIONS
        for filename in os.listdir(flip_path):
            if filename.endswith(".png"):
                full_path = os.path.join(flip_path, filename)
                trick_name = filename[:-4]
                self.animations[trick_name] = pygame.image.load(full_path)
        
        # Load grind trick animations
        grind_path = config.GRIND_ANIMATIONS
        for filename in os.listdir(grind_path):
            if filename.endswith(".png"):
                full_path = os.path.join(grind_path, filename)
                trick_name = filename[:-4]
                self.animations[trick_name] = pygame.image.load(full_path)

    def handle_input(self, input_data):
        if self.state_manager.is_in_menu():
            self.handle_menu_input(input_data)
        elif self.state_manager.is_player_rolling():
            self.handle_trick_combo(input_data)
        elif self.state_manager.is_player_airborne():
            # Check if on rail, last trick was successful, and can grind
            if (self.level and self.level.get_current_chunk_type() == 'rail' and 
                self.last_trick_successful and self.grind_window_start is not None):
                self.handle_grind_combo(input_data)
            else:
                self.handle_trick_combo_end(input_data)
        elif self.state_manager.is_player_grinding():
            self.handle_grind_exit(input_data)

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
        
        # Reset completed grinds that have finished
        if (self.state_manager.is_player_rolling() and 
            self.trick_manager.trick_completed and 
            self.trick_manager.current_trick and
            "Grind" in self.trick_manager.current_trick):
            self.trick_manager.reset_trick()
        
        # Check if trick failed due to timing (1.5 loops)
        # Skip this check for grinds as they always succeed
        if (self.trick_manager.current_trick and 
            self.trick_manager.trick_completed and 
            self.state_manager.is_player_airborne() and
            not self.state_manager.is_player_grinding() and
            self.trick_manager.get_trick_progress() >= 1.5):
            # Trick failed automatically - end the trick
            self.last_trick_successful = False
            
            self.state_manager.end_trick()
            self.display.stop_animation()
            self.trick_manager.reset_trick()
            
            # Play landing sound using sound manager
            if self.sound_manager:
                self.sound_manager.play_land_sound()
        
        # Check grind window timer - land if window expired
        if (self.grind_window_start is not None and 
            self.state_manager.is_player_airborne() and
            self.trick_manager.trick_completed):
            elapsed = time.time() - self.grind_window_start
            if elapsed >= self.grind_window_duration:
                # Window expired - land
                self.last_trick_successful = False
                
                self.state_manager.end_trick()
                self.display.stop_animation()
                self.trick_manager.reset_trick()
                self.grind_window_start = None
                
                # Play landing sound
                if self.sound_manager:
                    self.sound_manager.play_land_sound()
        
        # Check if reached end of rail (with grace period for multiple rails)
        if self.state_manager.is_player_grinding():
            on_rail = self.level.get_current_chunk_type() == 'rail' if self.level else False
            
            if not on_rail:
                # Start timer for being off rail
                if self.grind_off_rail_timer is None:
                    self.grind_off_rail_timer = time.time()
            else:
                # On rail - reset timer
                self.grind_off_rail_timer = None
            
            # Check if grace period expired
            if self.grind_off_rail_timer is not None:
                elapsed = time.time() - self.grind_off_rail_timer
                if elapsed >= self.grind_off_rail_duration:
                    # Been off rail too long - end grind
                    # Force complete grind as successful
                    grind_just_completed = False
                    if self.trick_manager.current_trick and not self.trick_manager.trick_completed:
                        self.trick_manager.complete_trick(1)
                        grind_just_completed = True
                    
                    self.last_trick_successful = False
                    
                    if self.sound_manager:
                        self.sound_manager.stop_rail_sound()
                        self.sound_manager.play_land_sound()
                    
                    self.state_manager.end_grind()
                    self.display.stop_animation()
                    
                    # Don't reset trick immediately if just completed - let success message show
                    if not grind_just_completed:
                        self.trick_manager.reset_trick()
        
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
                # Trick was successful
                self.last_trick_successful = True
                
                # UI already updated by trick manager
                # Check if on rail - if so, stay airborne to allow grind input
                if self.level and self.level.get_current_chunk_type() == 'rail':
                    # Stay airborne - start grind window timer
                    self.grind_window_start = time.time()
                else:
                    # Not on rail - land normally
                    self.last_trick_successful = False
                    
                    self.state_manager.end_trick()
                    self.display.stop_animation()
                    self.trick_manager.reset_trick()
                    
                    # Play landing sound using sound manager
                    if self.sound_manager:
                        self.sound_manager.play_land_sound()
            else:
                # Trick failed - land immediately, no grinding allowed
                self.last_trick_successful = False
                
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
        # Reset success flag for new trick
        self.last_trick_successful = False
        
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
    
    def handle_grind_combo(self, input_data):
        """Handle grind trick combinations (simpler than flip tricks, no double-tap)."""
        keys_held = input_data.get('keys_held', [["none", False], ["none", False]])
        double_tapped_actions = input_data.get('double_tapped_actions', set())
        
        left_key = keys_held[0][0] if keys_held[0][0] != "none" else "none"
        right_key = keys_held[1][0] if keys_held[1][0] != "none" else "none"
        
        # Check grind controls (simpler format - just keys, no double-tap)
        for grind_name, required_keys in config.GRIND_CONTROLS.items():
            left_required = required_keys[0]
            right_required = required_keys[1]
            
            if left_key == left_required and right_key == right_required:
                self.execute_grind(grind_name)
                return
    
    def handle_grind_exit(self, input_data):
        """Handle exiting grind when keys are released."""
        keys_held = input_data.get('keys_held', [["none", False], ["none", False]])
        
        # Exit grind when all keys released
        if keys_held[0][0] == "none" and keys_held[1][0] == "none":
            # Force complete grind as successful if not already completed
            if self.trick_manager.current_trick and not self.trick_manager.trick_completed:
                # Grinds always succeed with GOOD multiplier
                self.trick_manager.complete_trick(1)
            
            self.last_trick_successful = False
            
            # Reset off-rail timer
            self.grind_off_rail_timer = None
            
            self.state_manager.end_grind()
            self.display.stop_animation()
            self.trick_manager.reset_trick()
            
            # Stop rail sound and play landing sound
            if self.sound_manager:
                self.sound_manager.stop_rail_sound()
                self.sound_manager.play_land_sound()
    
    def execute_grind(self, grind_name):
        """Execute a grind trick."""
        # Reset grind window timer
        self.grind_window_start = None
        
        # Reset off-rail timer
        self.grind_off_rail_timer = None
        
        # Start grinding state
        self.state_manager.start_grind()

        if grind_name not in self.animations:
            return
        
        animation = self.animations[grind_name]
        self.display.start_animation(grind_name, animation, loop=True)
        
        # Start tracking this grind
        self.trick_manager.start_trick(grind_name)
        
        # Show grind start in UI
        if self.ui:
            self.ui.show_trick_start(grind_name)

        # Play rail sound in a loop
        if self.sound_manager:
            self.sound_manager.play_rail_sound()
        
        # Log grind execution
        if self.debug:
            self.debug.log_trick(grind_name)
    
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