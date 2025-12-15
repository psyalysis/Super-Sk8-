"""Skateboard rendering / controls module."""

import pygame
import os
import time
from core.state_manager import StateManager
from tricks import TrickManager
import config

# Hardcoded animation paths
ANIMATIONS_PATH = "assets/animations/flip/"
GRIND_ANIMATIONS_PATH = "assets/animations/grind/"

# Hardcoded trick controls
FLIP_CONTROLS = {
    "Kickflip": {"keys": [["left-left", False], ["right-down", False]]},
    "Heelflip": {"keys": [["left-left", False], ["right-up", False]]},
    "Varial Kickflip": {"keys": [["left-down", False], ["right-down", False]]},
    "Varial Heelflip": {"keys": [["left-up", False], ["right-up", False]]},
    "Hardflip": {"keys": [["left-up", False], ["right-down", False]]},
    "Inward Heelflip": {"keys": [["left-down", False], ["right-up", False]]},
    "BS-Shuv": {"keys": [["left-down", False], ["right-left", False]]},
    "FS-Shuv": {"keys": [["left-up", False], ["right-left", False]]}
}

GRIND_CONTROLS = {
    "50-50 Grind": ["left-left", "right-right"],
    "5-0 Grind": ["left-left", "right-left"],
    "Nose Grind": ["left-right", "right-right"],
    "Overcrooked Grind": ["left-up", "right-right"],
    "Crooked Grind": ["left-down", "right-right"],
    "Losi Grind": ["left-up", "right-right"],
    "Lazy Grind": ["left-down", "right-left"],
    "Salad Grind": ["left-left", "right-up"],
    "Suski Grind": ["left-left", "right-down"],
    "Feeble Grind": ["left-right", "right-up"],
    "Smith Grind": ["left-right", "right-down"],
    "Noseslide": ["left-up", "right-up"],
    "Tailslide": ["left-down", "right-down"],
    "Boardslide": ["left-down", "right-up"],
    "Lipslide": ["left-up", "right-down"],
}


class Control:
    def __init__(self, display, state_manager, input_handler, debug=None, ui=None, sound_manager=None, level=None):
        self.display = display
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.debug = debug
        self.ui = ui
        self.sound_manager = sound_manager
        self.level = level
        
        self.trick_manager = TrickManager(display, state_manager, ui, sound_manager)
        
        self.grind_window_start = None
        self.grind_window_duration = 0.25
        self.last_trick_successful = False
        self.grind_off_rail_timer = None
        self.grind_off_rail_duration = 0.15
        
        self.load_animations()
        
    def load_animations(self):
        self.animations = {}
        
        for path in [ANIMATIONS_PATH, GRIND_ANIMATIONS_PATH]:
            for filename in os.listdir(path):
                if filename.endswith(".png"):
                    full_path = os.path.join(path, filename)
                    trick_name = filename[:-4]
                    self.animations[trick_name] = pygame.image.load(full_path)

    def handle_input(self, input_data):
        if self.state_manager.is_in_menu():
            self.handle_menu_input(input_data)
        elif self.state_manager.is_player_rolling():
            self.handle_trick_combo(input_data)
        elif self.state_manager.is_player_airborne():
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
                    'keys_held': self.input_handler.keys_held
                }
                self.handle_trick_combo(input_data)
        
        self.trick_manager.update_trick_progress()
        
        # Reset completed grinds  # Simplified: Consolidated timer checks and removed redundant state checks
        if (self.state_manager.is_player_rolling() and 
            self.trick_manager.trick_completed and 
            self.trick_manager.current_trick and
            "Grind" in self.trick_manager.current_trick):
            self.trick_manager.reset_trick()
        
        # Check trick failure
        if (self.trick_manager.current_trick and 
            self.trick_manager.trick_completed and 
            self.state_manager.is_player_airborne() and
            not self.state_manager.is_player_grinding() and
            self.trick_manager.get_trick_progress() >= 1.5):
            self.last_trick_successful = False
            self.state_manager.end_trick()
            self.display.stop_animation()
            self.trick_manager.reset_trick()
            if self.sound_manager:
                self.sound_manager.play_land_sound()
        
        # Check grind window timer  # Simplified: Removed elapsed variable, direct time comparison
        if (self.grind_window_start is not None and 
            self.state_manager.is_player_airborne() and
            self.trick_manager.trick_completed):
            if time.time() - self.grind_window_start >= self.grind_window_duration:
                self.last_trick_successful = False
                self.state_manager.end_trick()
                self.display.stop_animation()
                self.trick_manager.reset_trick()
                self.grind_window_start = None
                if self.sound_manager:
                    self.sound_manager.play_land_sound()
        
        # Check rail exit
        if self.state_manager.is_player_grinding():
            on_rail = self.level.get_current_chunk_type() == 'rail' if self.level else False
            
            if not on_rail:
                if self.grind_off_rail_timer is None:
                    self.grind_off_rail_timer = time.time()
            else:
                self.grind_off_rail_timer = None
            
            if self.grind_off_rail_timer is not None:
                if time.time() - self.grind_off_rail_timer >= self.grind_off_rail_duration:
                    if self.trick_manager.current_trick and not self.trick_manager.trick_completed:
                        self.trick_manager.complete_trick(1)
                    
                    self.last_trick_successful = False
                    
                    if self.sound_manager:
                        self.sound_manager.stop_rail_sound()
                        self.sound_manager.play_land_sound()
                    
                    self.state_manager.end_grind()
                    self.display.stop_animation()
                    self.trick_manager.reset_trick()
        
        if self.ui:
            self.ui.update_trick_display()
    
    def handle_trick_combo(self, input_data):
        keys_held = input_data.get('keys_held', [["none", False], ["none", False]])
        
        left_key = keys_held[0][0] if keys_held[0][0] != "none" else "none"
        right_key = keys_held[1][0] if keys_held[1][0] != "none" else "none"
        
        for trick_name, config_data in FLIP_CONTROLS.items():
            required_keys = config_data["keys"]
            left_required = required_keys[0][0]
            right_required = required_keys[1][0]
            
            if left_key == left_required and right_key == right_required:
                self.execute_trick(trick_name)
                return
    
    def handle_trick_combo_end(self, input_data):
        keys_held = input_data.get('keys_held', [["none", False], ["none", False]])
        
        self.trick_manager.check_keys_released(keys_held)
        
        if keys_held[0][0] == "none" and keys_held[1][0] == "none":
            if self.trick_manager.trick_completed:
                self.last_trick_successful = True
                
                if self.level and self.level.get_current_chunk_type() == 'rail':
                    self.grind_window_start = time.time()
                else:
                    self.last_trick_successful = False
                    self.state_manager.end_trick()
                    self.display.stop_animation()
                    self.trick_manager.reset_trick()
                    if self.sound_manager:
                        self.sound_manager.play_land_sound()
            else:
                self.last_trick_successful = False
                
                if self.ui and self.trick_manager.current_trick:
                    self.ui.show_trick_fail(self.trick_manager.current_trick)
                
                self.display.show_board_color_feedback('red')
                self.state_manager.end_trick()
                self.display.stop_animation()
                self.trick_manager.reset_trick()
                
                if self.sound_manager:
                    self.sound_manager.play_land_sound()
    
    def execute_trick(self, trick_name):
        # Fixed: Prevent executing new trick if already performing one
        if self.state_manager.is_player_airborne() or self.state_manager.is_player_grinding():
            return
        
        self.last_trick_successful = False
        
        self.state_manager.start_trick()

        if trick_name not in self.animations:
            return
        
        animation = self.animations[trick_name]
        self.display.start_animation(trick_name, animation, loop=True)
        
        self.trick_manager.start_trick(trick_name)
        
        if self.ui:
            self.ui.show_trick_start(trick_name)

        if self.sound_manager:
            self.sound_manager.play_pop_sound()
        
        if self.debug:
            self.debug.log_trick(trick_name)
    
    def handle_grind_combo(self, input_data):
        keys_held = input_data.get('keys_held', [["none", False], ["none", False]])
        
        left_key = keys_held[0][0] if keys_held[0][0] != "none" else "none"
        right_key = keys_held[1][0] if keys_held[1][0] != "none" else "none"
        
        for grind_name, required_keys in GRIND_CONTROLS.items():
            if left_key == required_keys[0] and right_key == required_keys[1]:
                self.execute_grind(grind_name)
                return
    
    def handle_grind_exit(self, input_data):
        keys_held = input_data.get('keys_held', [["none", False], ["none", False]])
        
        if keys_held[0][0] == "none" and keys_held[1][0] == "none":
            if self.trick_manager.current_trick and not self.trick_manager.trick_completed:
                self.trick_manager.complete_trick(1)
            
            self.last_trick_successful = False
            self.grind_off_rail_timer = None
            
            self.state_manager.end_grind()
            self.display.stop_animation()
            self.trick_manager.reset_trick()
            
            if self.sound_manager:
                self.sound_manager.stop_rail_sound()
                self.sound_manager.play_land_sound()
    
    def execute_grind(self, grind_name):
        self.grind_window_start = None
        self.grind_off_rail_timer = None
        
        self.state_manager.start_grind()

        if grind_name not in self.animations:
            return
        
        animation = self.animations[grind_name]
        self.display.start_animation(grind_name, animation, loop=True)
        
        self.trick_manager.start_trick(grind_name)
        
        if self.ui:
            self.ui.show_trick_start(grind_name)

        if self.sound_manager:
            self.sound_manager.play_rail_sound()
        
        if self.debug:
            self.debug.log_trick(grind_name)
    
    def handle_menu_input(self, input_data):
        action = input_data.get('action', '')
        
        if action == 'enter':
            self.state_manager.start_game()
            self.display.show_skateboard()
        elif action == 'escape':
            pygame.event.post(pygame.event.Event(pygame.QUIT))
