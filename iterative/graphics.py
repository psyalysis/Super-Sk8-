import pygame
import os
import config

class Graphics:
    def __init__(self, screen):
        self.screen = screen
        self.animation_frame_rate = config.ANIMATION_FRAME_RATE

    def draw(self, player):
        self.screen.fill((0, 0, 0))
        
        pygame.display.flip()

    def update(self):
        pygame.display.update()

    def clear(self):
        self.screen.fill((0, 0, 0))