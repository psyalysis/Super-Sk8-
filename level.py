"""Level generation / management module."""

import config
import os
import pygame

class Level:
    def __init__(self, display, main):
        self.display = display
        self.main = main
        
    def load_textures(self):
        """
        Load the textures for the level.
        
        How it works:
        
        - Get all of the files in the floor texture location specified in config.py
        - Verify that the file is a VALID floor texture (is an image file and contains the word "sprite")
        - Load each of the textures found in the folder
        """
        self.floor_texture_location = config.FLOOR_TEXTURES_PATH
        for texture in os.listdir(self.floor_texture_location):
            print("Texture name: " + texture)
            if texture.endswith(".png"):
                if "sprite" in texture:
                    self.floor_textures.append(pygame.image.load(self.floor_texture_location + texture))
                    
        
    def draw_environment(self):
        """
        Draw the environment.
        """