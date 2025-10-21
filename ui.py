"""UI module."""

import pygame
import config


class UI:
    def __init__(self, display):
        self.display = display
        self.button = pygame.image.load("icons/ButtonEmpty.png")
        self.play_icon = pygame.image.load("icons/play.png")
        self.settings_icon = pygame.image.load("icons/question.png")
        self.bob_frame = 0
        
        # Pre-scale UI elements for better performance
        self.button_scale = 4
        self.scaled_button = pygame.transform.scale(
            self.button, 
            (self.button.get_width() * self.button_scale, 
             self.button.get_height() * self.button_scale)
        )
        
        icon_scale = self.button.get_height() * self.button_scale * 0.9
        self.scaled_play_icon = pygame.transform.scale(self.play_icon, (icon_scale, icon_scale))
        self.scaled_settings_icon = pygame.transform.scale(self.settings_icon, (icon_scale, icon_scale))
        
        # Trick display
        self.current_trick_display = None
        self.trick_display_duration = 2000  # 2 seconds
        self.trick_display_start_time = 0
        
        # Load bold font for trick display
        self.trick_font = self.display.resource_manager.load_font(config.FONT_BOLD_PATH, config.FONT_SIZE_MEDIUM)
        
    def draw_menu(self):
        screen = self.display.screen
        width, height = screen.get_size()
        horizontal_center = width // 2
        horizontal_offset = 400

        # Use pre-scaled button dimensions
        scaled_button_width = self.scaled_button.get_width()
        scaled_button_height = self.scaled_button.get_height()
        
        vertical_spacing = 64

        self.bob_frame += 0.25
        if self.bob_frame > 20:
            self.bob_frame = 0

        bob_offset = 5 if self.bob_frame > 10 else -5

        button_x = horizontal_center - scaled_button_width // 2 + horizontal_offset

        total_height = (scaled_button_height * 2) + vertical_spacing
        center_y = height // 2

        play_button_y = center_y - total_height // 2 + bob_offset
        settings_button_y = play_button_y + scaled_button_height + vertical_spacing
        
        play_button_icon_x = button_x + scaled_button_height // 2
        settings_button_icon_x = button_x + scaled_button_height // 2
        
        play_button_icon_y = play_button_y + scaled_button_height // 2
        settings_button_icon_y = settings_button_y + scaled_button_height // 2
        
        # Use pre-scaled elements
        self.display.screen.blit(self.scaled_button, (button_x, play_button_y))
        self.display.screen.blit(self.scaled_button, (button_x, settings_button_y))

        self.display.screen.blit(
            self.scaled_play_icon,
            (play_button_icon_x, play_button_y + scaled_button_height // 2 - self.scaled_play_icon.get_height() // 2)
        )

        self.display.screen.blit(
            self.scaled_settings_icon,
            (settings_button_icon_x, settings_button_y + scaled_button_height // 2 - self.scaled_settings_icon.get_height() // 2)
        )
        
    def draw_progress_bar(self):
        pass
    
    def show_trick_start(self, trick_name):
        """Show trick name in grey when trick starts."""
        self.current_trick_display = {
            'text': trick_name,
            'color': config.COLORS['gray'],
            'type': 'start'
        }
        self.trick_display_start_time = pygame.time.get_ticks()
    
    def show_trick_success(self, trick_name, score):
        """Show trick name and score in green for successful landing."""
        self.current_trick_display = {
            'text': f"{trick_name} - {score}",
            'color': config.COLORS['success'],
            'type': 'success'
        }
        self.trick_display_start_time = pygame.time.get_ticks()
    
    def show_trick_fail(self, trick_name):
        """Show trick name in red for failed landing."""
        self.current_trick_display = {
            'text': trick_name,
            'color': config.COLORS['danger'],
            'type': 'fail'
        }
        self.trick_display_start_time = pygame.time.get_ticks()
    
    def update_trick_display(self):
        """Update trick display timer and clear if expired."""
        if self.current_trick_display:
            current_time = pygame.time.get_ticks()
            if current_time - self.trick_display_start_time > self.trick_display_duration:
                self.current_trick_display = None
    
    def draw_trick_display(self):
        """Draw current trick display in bottom middle of screen."""
        if not self.current_trick_display:
            return
        
        screen = self.display.screen
        width, height = screen.get_size()
        
        # Position in bottom middle
        x = width // 2
        y = height - 60
        
        # Render text with drop shadow
        text = self.current_trick_display['text']
        color = self.current_trick_display['color']
        
        # Render shadow (black, offset by 2 pixels)
        shadow_surface = self.trick_font.render(text, True, config.COLORS['black'])
        shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2))
        
        # Render main text
        text_surface = self.trick_font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        
        # Draw shadow first, then main text
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)