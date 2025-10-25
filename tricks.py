"""Trick landing and scoring module."""

import pygame
import config
import os


class TrickManager:
    def __init__(self, display, state_manager, ui=None, sound_manager=None):
        self.display = display
        self.state_manager = state_manager
        self.ui = ui
        self.sound_manager = sound_manager
        
        # Trick tracking
        self.current_trick = None
        self.trick_start_time = 0
        self.trick_completed = False
        self.total_frames = 0
        self.frame_duration = 0  # Duration of each frame in milliseconds
        self.frames_elapsed = 0  # Track total frames since trick started
    
    def load_sounds(self):
        """Load sound effects."""
        # Sound loading is now handled by SoundManager
        pass
    
    def start_trick(self, trick_name):
        """Called when a trick animation starts."""
        self.current_trick = trick_name
        self.trick_start_time = pygame.time.get_ticks()
        self.trick_completed = False
        self.total_frames = len(self.display.animation_frames) if self.display.animation_frames else 0
        self.frame_duration = self.display.frame_duration
        self.frames_elapsed = 0
    
    def update_trick_progress(self):
        """Update trick progress and detect failure at 1.5 loops."""
        if not self.current_trick or not self.display.animation_running:
            return
        
        # Increment frame counter each time this is called
        self.frames_elapsed += 1
        
        # Calculate current trick progress
        current_progress = self.get_trick_progress()
        
        # Check for trick failure at 1.5 progress (1.5 loops)
        if current_progress >= 1.5:
            self.fail_trick()
            return
    
    def get_trick_progress(self):
        """Calculate how much of the trick animation has been completed."""
        if not self.current_trick or self.total_frames == 0:
            return 0.0
        
        # Use frames_elapsed to calculate progress
        # frames_elapsed counts at 60 FPS, but animation runs at 30 FPS
        # So we need to divide by 2 to get actual animation frames
        actual_animation_frames = self.frames_elapsed / 2
        
        # 1.0 = exactly one complete loop
        # 1.5 = one and a half loops
        progress = actual_animation_frames / self.total_frames
        
        return progress
    
    def check_keys_released(self, keys_held):
        """Check if keys have been released and calculate score multiplier."""
        if not self.current_trick or self.trick_completed:
            return
        
        # Check if no keys are held
        left_key = keys_held[0][0] if keys_held[0][0] != "none" else "none"
        right_key = keys_held[1][0] if keys_held[1][0] != "none" else "none"
        
        keys_released = (left_key == "none" and right_key == "none")
        
        if not keys_released:
            return
        
        # Calculate score multiplier based on trick progress
        multiplier = self.calculate_score_multiplier()
        
        if multiplier > 0:
            self.complete_trick(multiplier)
    
    def calculate_score_multiplier(self):
        """Calculate score multiplier based on trick progress."""
        progress = self.get_trick_progress()
        
        # Perfect landing: exactly 1.0 progress (4x multiplier)
        if 0.95 <= progress <= 1.05:  # Small tolerance for perfect timing
            return 4
        
        # Great landing: close to perfect (2x multiplier)
        elif 0.85 <= progress <= 1.15:
            return 2
        
        # Good landing: reasonable timing (1x multiplier)
        elif 0.7 <= progress <= 1.3:
            return 1
        
        # Too early or too late: no multiplier
        else:
            return 0
    
    def fail_trick(self):
        """Fail the trick due to timing miss."""
        if self.trick_completed:
            return
        
        self.trick_completed = True
        
        # Show fail message in UI
        if self.ui and self.current_trick:
            self.ui.show_trick_fail(self.current_trick)
        
        # Show red board feedback
        self.display.show_board_color_feedback('red')
        
        # Play fail sound
        if self.sound_manager:
            self.sound_manager.play_fail_sound()
        
        # Log trick failure
        print(f"Trick failed: {self.current_trick} - Missed timing (1.5 loops)")
    
    def complete_trick(self, multiplier=1):
        """Complete the trick and play success sound."""
        if self.trick_completed:
            return
        
        self.trick_completed = True
        
        # Calculate final score
        base_score = self.get_trick_score(self.current_trick)
        final_score = base_score * multiplier
        
        # Play success sound
        if self.sound_manager:
            self.sound_manager.play_success_sound()
        
        # Show success in UI
        if self.ui:
            self.ui.show_trick_success(self.current_trick, final_score)
        
        # Show green board feedback
        self.display.show_board_color_feedback('green')
        
        self.display.add_camera_shake(2.0, 0.2)
        
        # Log successful trick completion with score info
        multiplier_text = {4: "PERFECT", 2: "GREAT", 1: "GOOD"}
        print(f"Trick completed: {self.current_trick} - {multiplier_text.get(multiplier, 'OK')} ({multiplier}x) - Score: {final_score}")
    
    def reset_trick(self):
        """Reset trick tracking."""
        self.current_trick = None
        self.trick_start_time = 0
        self.trick_completed = False
        self.total_frames = 0
        self.frame_duration = 0
        self.frames_elapsed = 0
    
    def get_trick_score(self, trick_name):
        """Get score for a completed trick."""
        # Basic scoring system - can be expanded
        trick_scores = {
            "Kickflip": 100,
            "Heelflip": 100,
            "Varial Kickflip": 150,
            "Varial Heelflip": 150,
            "Hardflip": 200,
            "Inward Heelflip": 200,
            "BS-Shuv": 80,
            "FS-Shuv": 80,
            "360 Hardflip": 300,
            "360 Inward Heelflip": 300,
            "Tre Flip": 250,
            "Lazer Flip": 250,
        }
        
        return trick_scores.get(trick_name, 50)  # Default score
    
    def get_current_score_info(self):
        """Get current trick score information for display."""
        if not self.current_trick:
            return None
        
        base_score = self.get_trick_score(self.current_trick)
        progress = self.get_trick_progress()
        multiplier = self.calculate_score_multiplier()
        
        return {
            'trick_name': self.current_trick,
            'base_score': base_score,
            'multiplier': multiplier,
            'progress': progress,
            'total_frames': self.total_frames
        }
