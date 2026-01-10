"""Sound management with volume control."""

import pygame
import random
import os

# Hardcoded sound settings
MASTER_VOLUME = 0.1
SOUND_PATHS = {
    "land": "assets/sfx/land_",
    "pop": "assets/sfx/pop_"
}


class SoundManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.sounds = {}
        self.master_volume = MASTER_VOLUME
        self.rail_channel = None
        self.preload_common_sounds()
    
    def set_master_volume(self, volume):
        self.master_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.master_volume)
    
    def load_sound(self, name, path):
        """Load a sound file and cache it."""
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.master_volume)
            self.sounds[name] = sound
            return sound
        except Exception as e:
            print(f"Failed to load sound {path}: {e}")
            return None
    
    def play_sound(self, name):
        """Play a loaded sound."""
        if name in self.sounds:
            try:
                self.sounds[name].play()
                return True
            except Exception as e:
                print(f"Error playing sound {name}: {e}")
        return False
    
    def play_random_sound(self, sound_prefix, count):
        """Play a random sound from a numbered sequence."""
        sound_num = random.randint(1, count)
        sound_name = f"{sound_prefix}_{sound_num}"
        
        if sound_name not in self.sounds:
            for ext in [".wav", ".mp3"]:
                sound_path = f"{SOUND_PATHS.get(sound_prefix, 'assets/sfx/')}{sound_num}{ext}"
                if os.path.exists(sound_path):
                    self.load_sound(sound_name, sound_path)
                    break
        
        return self.play_sound(sound_name)
    
    def play_land_sound(self):
        return self.play_random_sound("land", 5)
    
    def play_pop_sound(self):
        return self.play_random_sound("pop", 6)
    
    def play_success_sound(self):
        if "success" not in self.sounds:
            self.load_sound("success", "assets/sfx/Success.mp3")
        return self.play_sound("success")
    
    def play_fail_sound(self):
        if "fail" not in self.sounds:
            self.load_sound("fail", "assets/sfx/Fail.mp3")
        return self.play_sound("fail")
    
    def play_rail_sound(self):
        """Play rail grinding sound in a loop."""
        if "rail" not in self.sounds:
            self.load_sound("rail", "assets/sfx/Rail.wav")
        
        if self.rail_channel is not None:
            self.rail_channel.stop()
        
        try:
            self.rail_channel = self.sounds["rail"].play(-1)
            self.rail_channel.set_volume(self.master_volume)
            return True
        except Exception as e:
            print(f"Error playing rail sound: {e}")
            return False
    
    def stop_rail_sound(self):
        """Stop rail grinding sound."""
        if self.rail_channel is not None:
            self.rail_channel.stop()
            self.rail_channel = None
    
    def preload_common_sounds(self):
        """Preload commonly used sounds."""
        common_sounds = [
            ("success", "assets/sfx/Success.mp3"),
            ("fail", "assets/sfx/Fail.mp3"),
        ]
        
        for name, path in common_sounds:
            if os.path.exists(path):
                self.load_sound(name, path)
    
    def cleanup(self):
        self.sounds.clear()
