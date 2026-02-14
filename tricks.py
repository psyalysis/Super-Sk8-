"""Trick definitions and scoring logic."""
import config
from graphics import Graphics


class Tricks:
    def __init__(self, sound, graphics):
        self.sound = sound
        self.score = 0
        self.landed = False
        self.score_multiplier = 0
        self.flip_points = 0
        self.grind_points = 0
        self.graphics = graphics

    def flip_trick(self, trick, catch_frame):
        """Calculates the score for a flip trick"""
        # Frame 0/17 = "perfect" catch, 1/2/15/16 = good catch, else failed
        if catch_frame == 0 or catch_frame == 17:
            self.score_multiplier = 1.5
            self.sound.play_sound("Success.mp3")
        elif catch_frame == 1 or catch_frame == 2 or catch_frame == 15 or catch_frame == 16:
            self.score_multiplier = 1
            self.sound.play_sound("Success.mp3")
        else:
            self.score_multiplier = 0
            self.sound.play_sound("Fail.mp3")

        self.flip_points = config.TRICK_SCORE_MAP.get(trick, 0) * self.score_multiplier

        success = self.score_multiplier >= 1
        self.graphics.draw_text(f"{trick} {'caught' if success else 'failed'}{' perfectly!' if self.score_multiplier == 1.5 else ''} - +{self.flip_points}", success=success)
        
    def grind_trick(self, trick, duration):
        """Calculates the score for a grind trick"""
        self.grind_points = config.TRICK_SCORE_MAP.get(trick, 0) * (1 + duration / 100)
        self.sound.play_sound("Success.mp3")
        if trick:
            self.graphics.draw_text(f"{trick} grinded - +{int(self.grind_points)}")

    def update(self, dt):
        """Returns the current score"""
        return self.score

    def trick_landed(self):
        """Adds the score for the trick to the total score"""
        self.score += self.flip_points + self.grind_points
        self.flip_points = 0
        self.grind_points = 0
        self.sound.play_sound("Land_1.wav")