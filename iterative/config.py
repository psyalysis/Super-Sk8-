""" Game configuration constants. """

FPS = 60
ANIMATION_FRAME_RATE = 15
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
CAMERA_SPEED = 300

# Trick patterns: map trick name to required directions per hand.
# Directions are string names matching the `Direction` enum in control.py (e.g. "LEFT", "UP").
# Left or right can be omitted if the trick doesn't require that hand.
TRICK_MAP = {
    "Kickflip": {"left": "LEFT", "right": "DOWN"},
    "Heelflip": {"left": "LEFT", "right": "UP"},
}