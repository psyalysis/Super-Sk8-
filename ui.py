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
        
        # Score and combo tracking
        self.total_score = 0
        self.current_combo = 0
        self.max_combo = 0
        self.combo_start_time = 0
        self.combo_duration = 3000  # 3 seconds to maintain combo
        
        # Load fonts for UI elements with scaling
        scaled_large_size = int(config.FONT_SIZE_LARGE * config.SCALE_FACTOR)
        scaled_medium_size = int(config.FONT_SIZE_MEDIUM * config.SCALE_FACTOR)
        scaled_small_size = int(config.FONT_SIZE_SMALL * config.SCALE_FACTOR)
        
        self.score_font = self.display.resource_manager.load_font(config.FONT_BOLD_PATH, scaled_large_size)
        self.combo_font = self.display.resource_manager.load_font(config.FONT_PATH, scaled_small_size)
        self.trick_font = self.display.resource_manager.load_font(config.FONT_BOLD_PATH, scaled_medium_size)
        
        # Visual feedback system
        self.feedback_effects = []
        self.feedback_duration = 1000  # 1 second
        
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
        
        # Update score and combo
        self.add_score(score)
        self.increment_combo()
        
        # Add visual feedback effect
        screen = self.display.screen
        width, height = screen.get_size()
        feedback_position = (width // 2, height // 2 - 100)
        
        # Choose feedback text and color based on score
        if score >= 400:  # Perfect landing
            feedback_text = "PERFECT!"
            feedback_color = config.COLORS['warning']  # Gold
        elif score >= 200:  # Great landing
            feedback_text = "GREAT!"
            feedback_color = config.COLORS['success']  # Green
        elif score >= 100:  # Good landing
            feedback_text = "GOOD!"
            feedback_color = config.COLORS['info']  # Blue
        else:  # Basic landing
            feedback_text = "OK"
            feedback_color = config.COLORS['white']
        
        self.add_feedback_effect(feedback_text, feedback_color, feedback_position, "large")
    
    def show_trick_fail(self, trick_name):
        """Show trick name in red for failed landing."""
        self.current_trick_display = {
            'text': trick_name,
            'color': config.COLORS['danger'],
            'type': 'fail'
        }
        self.trick_display_start_time = pygame.time.get_ticks()
        
        # Reset combo on failure
        self.reset_combo()
        
        # Add visual feedback effect for failure
        screen = self.display.screen
        width, height = screen.get_size()
        feedback_position = (width // 2, height // 2 - 100)
        self.add_feedback_effect("FAIL!", config.COLORS['danger'], feedback_position, "large")
    
    def update_trick_display(self):
        """Update trick display timer and clear if expired."""
        if self.current_trick_display:
            current_time = pygame.time.get_ticks()
            if current_time - self.trick_display_start_time > self.trick_display_duration:
                self.current_trick_display = None
        
        # Update combo timer
        self.update_combo_timer()
    
    def add_score(self, points):
        """Add points to total score."""
        self.total_score += points
    
    def increment_combo(self):
        """Increment combo counter."""
        current_time = pygame.time.get_ticks()
        
        # If combo was already active, increment it
        if self.current_combo > 0 and current_time - self.combo_start_time <= self.combo_duration:
            self.current_combo += 1
        else:
            # Start new combo
            self.current_combo = 1
        
        self.combo_start_time = current_time
        self.max_combo = max(self.max_combo, self.current_combo)
        
        # Add visual feedback for combo milestones
        if self.current_combo in [5, 10, 15, 20, 25, 30]:
            screen = self.display.screen
            width, height = screen.get_size()
            feedback_position = (width - 200, 80)
            combo_text = f"{self.current_combo} COMBO!"
            self.add_feedback_effect(combo_text, config.COLORS['warning'], feedback_position, "medium")
    
    def reset_combo(self):
        """Reset combo counter."""
        self.current_combo = 0
    
    def update_combo_timer(self):
        """Update combo timer and reset if expired."""
        if self.current_combo > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.combo_start_time > self.combo_duration:
                self.reset_combo()
    
    def draw_trick_display(self):
        """Draw current trick display in bottom middle of screen."""
        if not self.current_trick_display:
            return
        
        screen = self.display.screen
        width, height = screen.get_size()
        
        # Position in bottom middle with scaling
        x = width // 2
        y = height - int(60 * config.SCALE_FACTOR)
        
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
    
    def draw_score_display(self):
        """Draw score display in top left corner."""
        screen = self.display.screen
        
        # Score text with scaled positioning
        score_text = f"Score: {self.total_score:,}"
        score_surface = self.score_font.render(score_text, True, config.COLORS['white'])
        score_x = int(20 * config.SCALE_FACTOR)
        score_y = int(20 * config.SCALE_FACTOR)
        score_rect = score_surface.get_rect(topleft=(score_x, score_y))
        
        # Draw shadow with scaled positioning
        shadow_surface = self.score_font.render(score_text, True, config.COLORS['black'])
        shadow_x = int(22 * config.SCALE_FACTOR)
        shadow_y = int(22 * config.SCALE_FACTOR)
        shadow_rect = shadow_surface.get_rect(topleft=(shadow_x, shadow_y))
        
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(score_surface, score_rect)
    
    def draw_combo_display(self):
        """Draw combo display in top right corner."""
        if self.current_combo <= 0:
            return
            
        screen = self.display.screen
        width, height = screen.get_size()
        
        # Combo text
        combo_text = f"Combo: x{self.current_combo}"
        
        # Choose color based on combo level
        if self.current_combo >= 10:
            combo_color = config.COLORS['warning']  # Gold for high combos
        elif self.current_combo >= 5:
            combo_color = config.COLORS['success']  # Green for medium combos
        else:
            combo_color = config.COLORS['white']    # White for low combos
        
        combo_surface = self.combo_font.render(combo_text, True, combo_color)
        combo_x = width - int(20 * config.SCALE_FACTOR)
        combo_y = int(20 * config.SCALE_FACTOR)
        combo_rect = combo_surface.get_rect(topright=(combo_x, combo_y))
        
        # Draw shadow with scaled positioning
        shadow_surface = self.combo_font.render(combo_text, True, config.COLORS['black'])
        shadow_x = width - int(18 * config.SCALE_FACTOR)
        shadow_y = int(22 * config.SCALE_FACTOR)
        shadow_rect = shadow_surface.get_rect(topright=(shadow_x, shadow_y))
        
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(combo_surface, combo_rect)
    
    def draw_hud(self):
        """Draw all HUD elements."""
        self.draw_score_display()
        self.draw_combo_display()
        self.draw_feedback_effects()
    
    def add_feedback_effect(self, text, color, position, size="medium"):
        """Add a visual feedback effect."""
        effect = {
            'text': text,
            'color': color,
            'position': position,
            'size': size,
            'start_time': pygame.time.get_ticks(),
            'alpha': 255
        }
        self.feedback_effects.append(effect)
    
    def draw_feedback_effects(self):
        """Draw all active feedback effects."""
        current_time = pygame.time.get_ticks()
        effects_to_remove = []
        
        for i, effect in enumerate(self.feedback_effects):
            elapsed = current_time - effect['start_time']
            
            if elapsed > self.feedback_duration:
                effects_to_remove.append(i)
                continue
            
            # Fade out effect
            fade_progress = elapsed / self.feedback_duration
            alpha = int(255 * (1.0 - fade_progress))
            
            # Choose font based on size
            if effect['size'] == "large":
                font = self.score_font
            elif effect['size'] == "small":
                font = self.combo_font
            else:
                font = self.trick_font
            
            # Create surface with alpha
            text_surface = font.render(effect['text'], True, effect['color'])
            text_surface.set_alpha(alpha)
            
            # Position effect (move up as it fades)
            x, y = effect['position']
            y -= int(fade_progress * 50)  # Move up 50 pixels over time
            
            self.display.screen.blit(text_surface, (x, y))
        
        # Remove expired effects
        for i in reversed(effects_to_remove):
            self.feedback_effects.pop(i)