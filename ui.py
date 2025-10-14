"""UI module."""

import pygame

class UI:
    def __init__(self, display):
        self.display = display
        self.button = pygame.image.load("icons/ButtonEmpty.png")
        self.play_icon = pygame.image.load("icons/play.png")
        self.settings_icon = pygame.image.load("icons/question.png")
        self.bob_frame = 0
        
    def draw_menu(self):
        """
        Draws a pixel art style play button (light grey) and a settings button underneath.
        Both are centered horizontally, with the settings button below the play button.
        """       
        
        
        screen = self.display.screen  # Assume display has the pygame surface as .screen
        width, height = screen.get_size()
        horizontal_center = width // 2
        horizontal_offset = 400

        button_width = self.button.get_width()
        button_height = self.button.get_height()

        play_button = self.button.copy()
        settings_button = self.button.copy()
        play_button_icon = self.play_icon.copy()
        settings_button_icon = self.settings_icon.copy()
        # Size and space
        button_scale = 4
        vertical_spacing = 64  # Space between buttons in pixels (after scaling)

        # Rescale buttons
        play_button = pygame.transform.scale(play_button, (button_width * button_scale, button_height * button_scale))
        settings_button = pygame.transform.scale(settings_button, (button_width * button_scale, button_height * button_scale))
        scaled_button_width = play_button.get_width()
        scaled_button_height = play_button.get_height()

        # Animation: make both buttons bob together
        self.bob_frame += 0.25
        if self.bob_frame > 20:
            self.bob_frame = 0

        #Bob offset is 5 pixels up and 5 pixels down every 10 frames
        bob_offset = 5 if self.bob_frame > 10 else -5

        # Centered horizontally
        button_x = horizontal_center - scaled_button_width // 2 + horizontal_offset

        # Center both buttons vertically and space them apart
        total_height = (scaled_button_height * 2) + vertical_spacing
        center_y = height // 2

        #Position the buttons vertically with the bobbing effect
        play_button_y = center_y - total_height // 2 + bob_offset
        settings_button_y = play_button_y + scaled_button_height + vertical_spacing
        
        #Scale the icons according to the button height (because the icons are 1:1 ratio)
        #Icons are also slightly scaled down to fit inside button better
        play_button_icon = pygame.transform.scale(play_button_icon, (button_height * button_scale * 0.9, button_height * button_scale * 0.9))
        settings_button_icon = pygame.transform.scale(settings_button_icon, (button_height * button_scale * 0.9, button_height * button_scale * 0.9))
        
        #Position the icons in the center of the buttons horizontally (after scaling)
        play_button_icon_x = button_x + scaled_button_height // 2
        settings_button_icon_x = button_x + scaled_button_height // 2
        
        #Position the icons vertically in the center of the buttons
        play_button_icon_y = play_button_y + scaled_button_height // 2
        settings_button_icon_y = settings_button_y + scaled_button_height // 2
        
        #Draw the buttons
        self.display.screen.blit(play_button, (button_x, play_button_y))
        self.display.screen.blit(settings_button, (button_x, settings_button_y))

        # Draw the play icon
        self.display.screen.blit(
            play_button_icon,
            (play_button_icon_x, play_button_y + scaled_button_height // 2 - play_button_icon.get_height() // 2)
        )

        # Draw the settings icon
        self.display.screen.blit(
            settings_button_icon,
            (settings_button_icon_x, settings_button_y + scaled_button_height // 2 - settings_button_icon.get_height() // 2)
        )
        
        
    def draw_progress_bar(self):
        """
        Draw the progress bar.
        """
        pass