import os
from pygame import mixer

SOUND_PATH = "./assets/sfx"

class Sound:
    def __init__(self):
        mixer.init()
        self._playing = {}  # name -> Sound instance (so we can stop the same one)

    def play_sound(self, sound_name, volume=1.0, loops=0, pitch=1.0):
        sound_path = f"{SOUND_PATH}/{sound_name}"
        if os.path.exists(sound_path):
            sound = mixer.Sound(sound_path)
            sound.set_volume(volume)
            sound.play(loops=loops)
            self._playing[sound_name] = sound

    def stop_sound(self, sound_name):
        if sound_name in self._playing:
            self._playing[sound_name].stop()
            del self._playing[sound_name]