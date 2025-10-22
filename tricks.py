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
        self.trick_start_frame = 0
        self.trick_loop_count = 0
        self.keys_released_after_loop = False
        self.trick_completed = False
        self.total_frames = 0
    
    def load_sounds(self):
        """Load sound effects."""
        # Sound loading is now handled by SoundManager
        pass
    
    def start_trick(self, trick_name):
        """Called when a trick animation starts."""
        self.current_trick = trick_name
        self.trick_start_frame = self.display.animation_frame
        self.trick_loop_count = 0
        self.keys_released_after_loop = False
        self.trick_completed = False
        self.last_frame = self.display.animation_frame
        self.total_frames = len(self.display.animation_frames) if self.display.animation_frames else 0
    
    def update_trick_progress(self):
        """Update trick progress and detect loop completion."""
        if not self.current_trick or not self.display.animation_running:
            return
        
        # Track when we complete a full loop by detecting frame 0 after starting
        current_frame = self.display.animation_frame
        
        # If we're at frame 0 and we've been tracking this trick
        if current_frame == 0 and self.trick_loop_count == 0:
            # Check if we've moved from a non-zero frame to frame 0 (indicating loop completion)
            if hasattr(self, 'last_frame') and self.last_frame > 0:
                self.trick_loop_count = 1
        elif current_frame == 0 and self.trick_loop_count > 0:
            # Additional loops after the first one
            if hasattr(self, 'last_frame') and self.last_frame > 0:
                self.trick_loop_count += 1
        
        # Store current frame for next update
        self.last_frame = current_frame
    
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
        
        current_frame = self.display.animation_frame
        
        # Calculate score multiplier based on landing timing
        multiplier = self.calculate_score_multiplier(current_frame)
        
        if multiplier > 0:
            self.complete_trick(multiplier)
    
    def calculate_score_multiplier(self, current_frame):
        """Calculate score multiplier based on landing frame timing."""
        # Perfect landing frames (4x multiplier):
        # 1. Penultimate frame (second to last frame)
        # 2. First frame on the 1st time looping (frame 0 after first loop)
        # 3. Second frame on the 1st loop (frame 1 after first loop)
        
        perfect_frames = []
        
        # Penultimate frame
        if self.total_frames > 1:
            perfect_frames.append(self.total_frames - 2)
        
        # First frame on 1st loop
        if self.trick_loop_count == 1:
            perfect_frames.extend([0, 1])
        
        # Check if current frame is perfect (4x multiplier)
        if current_frame in perfect_frames:
            return 4
        
        # Check for adjacent frames (2x multiplier)
        adjacent_frames = []
        for perfect_frame in perfect_frames:
            # Add frames before and after perfect frames
            if perfect_frame > 0:
                adjacent_frames.append(perfect_frame - 1)
            if perfect_frame < self.total_frames - 1:
                adjacent_frames.append(perfect_frame + 1)
        
        if current_frame in adjacent_frames:
            return 2
        
        # Check for frames 2 away (1x multiplier)
        two_away_frames = []
        for perfect_frame in perfect_frames:
            # Add frames 2 before and 2 after perfect frames
            if perfect_frame >= 2:
                two_away_frames.append(perfect_frame - 2)
            if perfect_frame <= self.total_frames - 3:
                two_away_frames.append(perfect_frame + 2)
        
        if current_frame in two_away_frames:
            return 1
        
        # No multiplier for other frames
        return 0
    
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
        
        self.display.level.add_camera_shake(2.0, 0.2)
        
        # Log successful trick completion with score info
        multiplier_text = {4: "PERFECT", 2: "GREAT", 1: "GOOD"}
        print(f"Trick completed: {self.current_trick} - {multiplier_text.get(multiplier, 'OK')} ({multiplier}x) - Score: {final_score}")
    
    def reset_trick(self):
        """Reset trick tracking."""
        self.current_trick = None
        self.trick_start_frame = 0
        self.trick_loop_count = 0
        self.keys_released_after_loop = False
        self.trick_completed = False
        self.last_frame = 0
        self.total_frames = 0
    
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
        current_frame = self.display.animation_frame
        multiplier = self.calculate_score_multiplier(current_frame)
        
        return {
            'trick_name': self.current_trick,
            'base_score': base_score,
            'multiplier': multiplier,
            'current_frame': current_frame,
            'total_frames': self.total_frames,
            'loop_count': self.trick_loop_count
        }
