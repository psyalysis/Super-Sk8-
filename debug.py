import config
import pygame


class Debug:
    def __init__(self, main):
        self.main = main
        self.current_message = None
        self.message_type = None
        self.message_time = 0
        self.display_duration = 3000
    
    def _set_message(self, message, msg_type):
        self.current_message = str(message)
        self.message_type = msg_type
        self.message_time = pygame.time.get_ticks()
    
    def get_current_message(self):
        if self.current_message is None:
            return None
        
        if pygame.time.get_ticks() - self.message_time > self.display_duration:
            self.current_message = None
            self.message_type = None
            return None
        
        return [self.current_message, self.message_type]
    
    def success(self, message):
        if config.DEBUG_PRINT_VISIBLE:
            print("[Success]: " + str(message))
        if config.DEBUG_TEXT_VISIBLE:
            self._set_message(message, "success")
    
    def error(self, message):
        print("[Error]: " + str(message))
        if config.DEBUG_TEXT_VISIBLE:
            self._set_message(message, "danger")
    
    def warning(self, message):
        if config.DEBUG_PRINT_VISIBLE:
            print("[Warning]: " + str(message))
        if config.DEBUG_TEXT_VISIBLE:
            self._set_message(message, "warning")
    
    def info(self, message):
        if config.DEBUG_PRINT_VISIBLE:
            print("[Info]: " + str(message))
        if config.DEBUG_TEXT_VISIBLE:
            self._set_message(message, "info")
    
    def log_trick(self, trick_name):
        """Log trick execution for debugging."""
        if config.DEBUG_PRINT_VISIBLE:
            print(f"[Trick]: {trick_name}")
        if config.DEBUG_TEXT_VISIBLE:
            self._set_message(f"Trick: {trick_name}", "success")
    
    def log_input(self, action, is_double_tap=False):
        """Log input events for debugging."""
        if config.DEBUG_PRINT_VISIBLE:
            double_tap_str = " (double-tap)" if is_double_tap else ""
            print(f"[Input]: {action}{double_tap_str}")
    
    def log_state_change(self, old_state, new_state):
        """Log state transitions for debugging."""
        if config.DEBUG_PRINT_VISIBLE:
            print(f"[State]: {old_state} -> {new_state}")