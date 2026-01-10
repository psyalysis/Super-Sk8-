"""UI module."""

import pygame

# Hardcoded UI settings
FONT_PATH = "assets/ui/ari-w9500.ttf"
FONT_BOLD_PATH = "assets/ui/ari-w9500-bold.ttf"
FONT_SIZE_SMALL = 16
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 32

COLORS = {
    'background': (0, 0, 0),
    'white': (236, 240, 241),
    'black': (22, 22, 22),
    'gray': (127, 140, 141),
    'success': (39, 174, 96),
    'danger': (192, 57, 43),
    'warning': (241, 196, 15),
}


class UI:
    def __init__(self, display):
        self.display = display
        self.button = pygame.image.load("assets/ui/ButtonEmpty.png")
        self.play_icon = pygame.image.load("assets/ui/play.png")
        
        self.button_scale = 4
        self.scaled_button = pygame.transform.scale(
            self.button, 
            (self.button.get_width() * self.button_scale, 
             self.button.get_height() * self.button_scale)
        )
        
        icon_scale = self.button.get_height() * self.button_scale * 0.7
        self.scaled_play_icon = pygame.transform.scale(self.play_icon, (icon_scale, icon_scale))
        
        self.current_trick_display = None
        self.trick_display_duration = 2000
        self.trick_display_start_time = 0
        
        self.total_score = 0
        
        self.score_font = self.display.resource_manager.load_font(FONT_BOLD_PATH, FONT_SIZE_LARGE)
        self.trick_font = self.display.resource_manager.load_font(FONT_BOLD_PATH, FONT_SIZE_MEDIUM)
        
        self.feedback_effects = []
        self.feedback_duration = 1000
        
    def draw_menu(self):
        screen = self.display.screen
        width, height = screen.get_size()
        horizontal_center = width // 2

        scaled_button_width = self.scaled_button.get_width()
        scaled_button_height = self.scaled_button.get_height()

        button_x = horizontal_center - scaled_button_width // 2
        center_y = height // 2
        play_button_y = center_y - scaled_button_height // 2
        
        self.display.screen.blit(self.scaled_button, (button_x, play_button_y))

        self.display.screen.blit(
            self.scaled_play_icon,
            (button_x + scaled_button_height // 2, play_button_y + scaled_button_height // 2 - self.scaled_play_icon.get_height() // 2)
        )
        
    def show_trick_start(self, trick_name):
        self.current_trick_display = {
            'text': trick_name,
            'color': COLORS['gray'],
            'type': 'start'
        }
        self.trick_display_start_time = pygame.time.get_ticks()
    
    def show_trick_success(self, trick_name, score):
        self.current_trick_display = {
            'text': f"{trick_name} - {score}",
            'color': COLORS['success'],
            'type': 'success'
        }
        self.trick_display_start_time = pygame.time.get_ticks()
        
        self.add_score(score)
        
        if score >= 400:
            feedback_text = "PERFECT!"
            feedback_color = COLORS['warning']
        elif score >= 200:
            feedback_text = "GREAT!"
            feedback_color = COLORS['success']
        elif score >= 100:
            feedback_text = "GOOD!"
            feedback_color = COLORS['white']
        else:
            feedback_text = "OK"
            feedback_color = COLORS['white']

        self.add_feedback_effect(feedback_text, feedback_color)
    
    def show_trick_fail(self, trick_name):
        self.current_trick_display = {
            'text': trick_name,
            'color': COLORS['danger'],
            'type': 'fail'
        }
        self.trick_display_start_time = pygame.time.get_ticks()
        
        self.add_feedback_effect("FAIL!", COLORS['danger'])
    
    def update_trick_display(self):
        if self.current_trick_display:
            current_time = pygame.time.get_ticks()
            if current_time - self.trick_display_start_time > self.trick_display_duration:
                self.current_trick_display = None
    
    def add_score(self, points):
        self.total_score += points
    
    def draw_trick_display(self):
        if not self.current_trick_display:
            return
        
        screen = self.display.screen
        width, height = screen.get_size()
        
        x = width // 2
        y = height - 60
        
        text = self.current_trick_display['text']
        color = self.current_trick_display['color']
        
        shadow_surface = self.trick_font.render(text, True, COLORS['black'])
        shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2))
        
        text_surface = self.trick_font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)
    
    def draw_score_display(self):
        screen = self.display.screen
        
        score_text = f"Score: {self.total_score:,}"
        score_surface = self.score_font.render(score_text, True, COLORS['white'])
        score_x = 20
        score_y = 20
        
        shadow_surface = self.score_font.render(score_text, True, COLORS['black'])
        screen.blit(shadow_surface, (score_x + 2, score_y + 2))
        screen.blit(score_surface, (score_x, score_y))
    
    def draw_hud(self):
        self.draw_score_display()
        self.draw_feedback_effects()
    
    def add_feedback_effect(self, text, color, position=None):  # Simplified: Removed size and tag parameters (over-engineered)
        effect = {
            'text': text,
            'color': color,
            'position': position,
            'start_time': pygame.time.get_ticks(),
            'alpha': 255
        }
        self.feedback_effects.append(effect)
    
    def draw_feedback_effects(self):
        current_time = pygame.time.get_ticks()
        effects_to_remove = []
        
        for i, effect in enumerate(self.feedback_effects):
            elapsed = current_time - effect['start_time']
            
            if elapsed > self.feedback_duration:
                effects_to_remove.append(i)
                continue
            
            fade_progress = elapsed / self.feedback_duration
            alpha = int(255 * (1.0 - fade_progress))
            
            width, height = self.display.screen.get_size()
            x = width // 2  # Simplified: Removed complex tag-based positioning logic
            y = height - 130
            
            if effect['position']:
                x, y = effect['position']
            
            y -= int(fade_progress * 50)
            
            text_surface = self.trick_font.render(effect['text'], True, effect['color'])  # Simplified: Always use trick_font (removed size-based font selection)
            text_surface.set_alpha(alpha)
            self.display.screen.blit(text_surface, (x, y))
        
        for i in reversed(effects_to_remove):
            self.feedback_effects.pop(i)
