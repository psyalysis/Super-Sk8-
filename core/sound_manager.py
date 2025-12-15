"""Sound management with volume control."""

import pygame
import config
import random
import os
from typing import Optional, Dict


class SoundManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # Dictionary to store all loaded sounds so we can access them by name
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.master_volume = config.MASTER_VOLUME
        
        # Queue of sounds to load on startup
        self.preload_queue = []
        self.loading_in_progress = False
        
        # Seperate channel for rail sound so that we can stop it when we want independently of other sounds
        self.rail_channel = None
        
        # Preload common sounds
        self.preload_common_sounds()
    
    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0).
        Parameters:
            volume: float - The new master volume (0.0 to 1.0)
            
        Updates all sound volumes based on the new master volume clamped between 0.0 and 1.0.
        """
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()
    
    def _update_all_volumes(self):
        """Update all sound volumes based on master volume."""
        for sound in self.sounds.values():
            sound.set_volume(self.master_volume)
    
    def load_sound(self, name: str, path: str) -> Optional[pygame.mixer.Sound]:
        """Load a sound file and cache it."""
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.master_volume)
            self.sounds[name] = sound
            return sound
        except pygame.error as e:
            print(f"Warning: Failed to load sound {path}: {e}")
            return None
    
    def play_sound(self, name: str) -> bool:
        """Play a loaded sound."""
        if name in self.sounds:
            try:
                channel = self.sounds[name].play()
                channel.set_volume(self.master_volume)
                return True
            except Exception as e:
                print(f"Error playing sound {name}: {e}")
                return False
        return False
    
    def play_random_sound(self, sound_prefix: str, count: int) -> bool:
        """Play a random sound from a numbered sequence."""
        sound_num = random.randint(1, count)
        sound_name = f"{sound_prefix}_{sound_num}"
        
        # Try to load if not already loaded
        if sound_name not in self.sounds:
            sound_path = f"{config.SOUND_PATHS.get(sound_prefix, 'assets/sfx/')}{sound_num}.wav"
            if os.path.exists(sound_path):
                self.load_sound(sound_name, sound_path)
            else:
                # Try .mp3 extension
                sound_path = f"{config.SOUND_PATHS.get(sound_prefix, 'assets/sfx/')}{sound_num}.mp3"
                if os.path.exists(sound_path):
                    self.load_sound(sound_name, sound_path)
                else:
                    print(f"Warning: Sound file not found: {sound_path}")
                    return False
        
        return self.play_sound(sound_name)
    
    def play_land_sound(self) -> bool:
        """Play random landing sound."""
        return self.play_random_sound("land", 5)
    
    def play_pop_sound(self) -> bool:
        """Play random pop sound."""
        return self.play_random_sound("pop", 6)
    
    def play_success_sound(self) -> bool:
        """Play success sound."""
        if "success" not in self.sounds:
            success_path = "assets/sfx/Success.mp3"
            if os.path.exists(success_path):
                self.load_sound("success", success_path)
            else:
                print("Warning: Success sound not found")
                return False
        return self.play_sound("success")
    
    def play_fail_sound(self) -> bool:
        """Play fail sound."""
        if "fail" not in self.sounds:
            fail_path = "assets/sfx/Fail.mp3"
            if os.path.exists(fail_path):
                self.load_sound("fail", fail_path)
            else:
                print("Warning: Fail sound not found")
                return False
        return self.play_sound("fail")
    
    def play_rail_sound(self) -> bool:
        """Play rail grinding sound."""
        if "rail" not in self.sounds:
            rail_path = "assets/sfx/Rail.wav"
            if os.path.exists(rail_path):
                self.load_sound("rail", rail_path)
            else:
                print("Warning: Rail sound not found")
                return False
        
        # Play rail sound in a loop
        try:
            # Stop existing rail sound if playing
            if self.rail_channel is not None:
                self.rail_channel.stop()
            
            self.rail_channel = self.sounds["rail"].play(-1)  # -1 means loop forever
            self.rail_channel.set_volume(self.master_volume)
            return True
        except Exception as e:
            print(f"Error playing rail sound: {e}")
            return False
    
    def stop_rail_sound(self):
        """Stop rail grinding sound."""
        try:
            if self.rail_channel is not None:
                self.rail_channel.stop()
                self.rail_channel = None
        except Exception as e:
            print(f"Error stopping rail sound: {e}")
    
    def preload_common_sounds(self):
        """Preload commonly used sounds to prevent frame drops."""
        common_sounds = [
            ("success", "assets/sfx/Success.mp3"),
            ("fail", "assets/sfx/Fail.mp3"),
        ]
        
        for name, path in common_sounds:
            if os.path.exists(path):
                self.load_sound(name, path)
    
    def cleanup(self):
        """Clean up sound resources."""
        self.sounds.clear()
