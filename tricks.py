"""Trick landing and scoring module."""

import pygame

TRICK_SCORES = {
    "Kickflip": 100,
    "Heelflip": 100,
    "Varial Kickflip": 150,
    "Varial Heelflip": 150,
    "Hardflip": 200,
    "Inward Heelflip": 200,
    "BS-Shuv": 100,
    "FS-Shuv": 100,
    "360 Hardflip": 300,
    "360 Inward Heelflip": 300,
    "Tre Flip": 250,
    "Lazer Flip": 250,
    "50-50 Grind": 150,
    "5-0 Grind": 150,
    "Nose Grind": 150,
    "Overcrooked Grind": 175,
    "Crooked Grind": 175,
    "Losi Grind": 200,
    "Lazy Grind": 200,
    "Salad Grind": 175,
    "Suski Grind": 175,
    "Feeble Grind": 150,
    "Smith Grind": 150,
    "Noseslide": 200,
    "Tailslide": 200,
    "Boardslide": 250,
    "Lipslide": 250,
}

PERFECT_RANGE = (0.95, 1.05)
GREAT_RANGE = (0.85, 1.15)
GOOD_RANGE = (0.7, 1.3)
FAIL_THRESHOLD = 1.5
MULTIPLIERS = {4: "PERFECT", 2: "GREAT", 1: "GOOD"}


class TrickManager:
    def __init__(self, display, state_manager, ui=None, sound_manager=None):
        self.display = display
        self.state_manager = state_manager
        self.ui = ui
        self.sound_manager = sound_manager
        
        self.current_trick = None
        self.trick_start_time = 0
        self.trick_completed = False
        self.total_frames = 0
        self.frame_duration = 0
        self.frames_elapsed = 0
    
    def start_trick(self, trick_name):
        self.current_trick = trick_name
        self.trick_start_time = pygame.time.get_ticks()
        self.trick_completed = False
        self.total_frames = len(self.display.animation_frames) if self.display.animation_frames else 0
        self.frame_duration = self.display.frame_duration
        self.frames_elapsed = 0
    
    def update_trick_progress(self):
        if not self.current_trick or not self.display.animation_running:
            return
        
        self.frames_elapsed += 1
        
        if self.get_trick_progress() >= FAIL_THRESHOLD:
            self.fail_trick()
    
    def get_trick_progress(self):
        if not self.current_trick or self.total_frames == 0:
            return 0.0
        return (self.frames_elapsed / 2) / self.total_frames
    
    def check_keys_released(self, keys_held):
        if self.trick_completed or not self.current_trick:
            return
        
        if keys_held[0][0] == "none" and keys_held[1][0] == "none":
            multiplier = self.calculate_score_multiplier()
            if multiplier > 0:
                self.complete_trick(multiplier)
    
    def calculate_score_multiplier(self):
        progress = self.get_trick_progress()
        
        if PERFECT_RANGE[0] <= progress <= PERFECT_RANGE[1]:
            return 4
        elif GREAT_RANGE[0] <= progress <= GREAT_RANGE[1]:
            return 2
        elif GOOD_RANGE[0] <= progress <= GOOD_RANGE[1]:
            return 1
        return 0
    
    def fail_trick(self):
        if self.trick_completed:
            return
        
        self.trick_completed = True
        
        if self.ui and self.current_trick:
            self.ui.show_trick_fail(self.current_trick)
        
        self.display.show_board_color_feedback('red')
        
        if self.sound_manager:
            self.sound_manager.play_fail_sound()
    
    def complete_trick(self, multiplier=1):
        if self.trick_completed:
            return
        
        self.trick_completed = True
        
        base_score = self.get_trick_score(self.current_trick)
        final_score = base_score * multiplier
        
        if self.sound_manager:
            self.sound_manager.play_success_sound()
        
        if self.ui:
            self.ui.show_trick_success(self.current_trick, final_score)
        
        self.display.show_board_color_feedback('green')
    
    def reset_trick(self):
        self.current_trick = None
        self.trick_start_time = 0
        self.trick_completed = False
        self.total_frames = 0
        self.frame_duration = 0
        self.frames_elapsed = 0
    
    def get_trick_score(self, trick_name):
        return TRICK_SCORES.get(trick_name, 50)  # Removed: get_current_score_info() method (unused)
