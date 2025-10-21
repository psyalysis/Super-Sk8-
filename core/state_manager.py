"""Clean state management system with enums and transitions."""

from enum import Enum
from typing import Optional, Callable, Dict, Any


class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class PlayerState(Enum):
    ROLLING = "rolling"
    AIRBORNE = "airborne"
    GRINDING = "grinding"


class StateManager:
    def __init__(self):
        self.game_state = GameState.MENU
        self.player_state = PlayerState.ROLLING
        self.state_history = []
        self.state_callbacks: Dict[str, Callable] = {}
        
        self._setup_default_callbacks()
    
    def _setup_default_callbacks(self):
        self.state_callbacks = {
            'on_menu_enter': lambda: None,
            'on_playing_enter': lambda: None,
            'on_paused_enter': lambda: None,
            'on_game_over_enter': lambda: None,
            'on_rolling_enter': lambda: None,
            'on_airborne_enter': lambda: None,
            'on_grinding_enter': lambda: None,
        }
    
    def set_callback(self, event_name: str, callback: Callable):
        self.state_callbacks[event_name] = callback
    
    def transition_game_state(self, new_state: GameState) -> bool:
        if new_state == self.game_state:
            return False
        
        old_state = self.game_state
        self.state_history.append(old_state)
        
        if len(self.state_history) > 10:
            self.state_history.pop(0)
        
        self.game_state = new_state
        
        callback_name = f'on_{new_state.value}_enter'
        if callback_name in self.state_callbacks:
            self.state_callbacks[callback_name]()
        
        return True
    
    def transition_player_state(self, new_state: PlayerState) -> bool:
        if new_state == self.player_state:
            return False
        
        old_state = self.player_state
        self.player_state = new_state
        
        callback_name = f'on_{new_state.value}_enter'
        if callback_name in self.state_callbacks:
            self.state_callbacks[callback_name]()
        
        return True
    
    def is_in_game_state(self, state: GameState) -> bool:
        return self.game_state == state
    
    def is_in_player_state(self, state: PlayerState) -> bool:
        return self.player_state == state
    
    def get_state_info(self) -> Dict[str, Any]:
        return {
            'game_state': self.game_state.value,
            'player_state': self.player_state.value,
            'state_history': [state.value for state in self.state_history[-5:]]
        }
    
    def reset_to_menu(self):
        self.transition_game_state(GameState.MENU)
        self.transition_player_state(PlayerState.ROLLING)
        self.state_history.clear()