import config
import pygame


class Debug:
    def __init__(self, main):
        self.main = main
        self.current_message = None
        self.message_type = None
        self.message_time = 0
        self.display_duration = 3000  # milliseconds (3 seconds)
    
    def _set_message(self, message, msg_type):
        """Store the message with timestamp for auto-clearing"""
        self.current_message = str(message)
        self.message_type = msg_type
        self.message_time = pygame.time.get_ticks()
    
    def get_current_message(self):
        """Returns current message if still valid, otherwise None"""
        if self.current_message is None:
            return None
        
        # Check if message has expired
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
        # Always print the error messages whether enabled or not
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