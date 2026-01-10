"""Simple debug logging system."""

# Hardcoded debug settings
DEBUG_TEXT_VISIBLE = True


class Debug:
    def __init__(self):
        pass
    
    def log_trick(self, trick_name):
        """Log trick execution."""
        if DEBUG_TEXT_VISIBLE:
            print(f"Trick: {trick_name}")
    
    def log_error(self, message):
        """Log error messages."""
        print(f"Error: {message}")  # Removed: log_info() method (unused)
