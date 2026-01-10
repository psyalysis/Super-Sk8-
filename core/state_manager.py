"""Simple state management with basic flags."""


class StateManager:
    def __init__(self):
        self.in_menu = True
        self.player_rolling = True
        self.player_airborne = False
        self.player_grinding = False
    
    def start_game(self):
        self.in_menu = False
        self.player_rolling = True
        self.player_airborne = False
    
    def start_trick(self):
        self.player_rolling = False
        self.player_airborne = True
    
    def end_trick(self):
        self.player_rolling = True
        self.player_airborne = False
    
    def is_in_menu(self):
        return self.in_menu
    
    def is_player_rolling(self):
        return self.player_rolling
    
    def is_player_airborne(self):
        return self.player_airborne
    
    def start_grind(self):
        self.player_grinding = True
        self.player_airborne = False
    
    def end_grind(self):
        self.player_grinding = False
        self.player_rolling = True
    
    def is_player_grinding(self):
        return self.player_grinding
