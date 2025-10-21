"""Simple state management with basic flags."""


class StateManager:
    def __init__(self):
        # Simple boolean flags instead of complex state system
        self.in_menu = True
        self.player_rolling = True
        self.player_airborne = False
    
    def start_game(self):
        """Start the game."""
        self.in_menu = False
        self.player_rolling = True
        self.player_airborne = False
    
    def start_trick(self):
        """Start a trick."""
        self.player_rolling = False
        self.player_airborne = True
    
    def end_trick(self):
        """End a trick."""
        self.player_rolling = True
        self.player_airborne = False
    
    def is_in_menu(self):
        """Check if in menu state."""
        return self.in_menu
    
    def is_player_rolling(self):
        """Check if player is rolling."""
        return self.player_rolling
    
    def is_player_airborne(self):
        """Check if player is airborne."""
        return self.player_airborne