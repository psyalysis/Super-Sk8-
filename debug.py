"""Simple debug logging system."""

import config


class Debug:
    def __init__(self):
        pass
    
    def log_trick(self, trick_name):
        """Log trick execution."""
        if config.DEBUG_TEXT_VISIBLE:
            print(f"Trick: {trick_name}")
    
    def log_error(self, message):
        """Log error messages."""
        print(f"Error: {message}")
    
    def log_info(self, message):
        """Log info messages."""
        if config.DEBUG_PRINT_VISIBLE:
            print(f"Info: {message}")