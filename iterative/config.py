""" Game configuration constants. """

FPS = 60
ANIMATION_FRAME_RATE = 45
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
CAMERA_SPEED = 300

# Trick patterns: map trick name to required directions per hand.
# Directions are string names matching the `Direction` enum in control.py (e.g. "LEFT", "UP").
# Left or right can be omitted if the trick doesn't require that hand.
TRICK_MAP = {
    "Kickflip": {"left": "LEFT", "right": "DOWN"},
    "Heelflip": {"left": "LEFT", "right": "UP"},
    "BS-Shuv": {"left": "DOWN", "right": "LEFT"},
    "FS-Shuv": {"left": "UP", "right": "LEFT"},
    "Varial Kickflip": {"left": "DOWN", "right": "DOWN"},
    "Varial Heelflip": {"left": "UP", "right": "UP"},
    "Hardflip": {"left": "UP", "right": "DOWN"},
    "Inward Heelflip": {"left": "DOWN", "right": "UP"},
}

GRIND_MAP = {
    "5-0": {"left": "LEFT", "right": "LEFT"},
    "50-50": {"left": "LEFT", "right": "RIGHT"},
    "Nose": {"left": "RIGHT", "right": "RIGHT"},
    "Crooked": {"left": "DOWN", "right": "RIGHT"},
    "Overcrooked": {"left": "UP", "right": "RIGHT"},
    "Smith": {"left": "RIGHT", "right": "DOWN"},
    "Feeble": {"left": "RIGHT", "right": "UP"},
    "Lazy": {"left": "DOWN", "right": "LEFT"},
    "Losi": {"left": "UP", "right": "LEFT"},
    "Suski": {"left": "LEFT", "right": "DOWN"},
    "Salad": {"left": "LEFT", "right": "UP"},
    "Boardslide": {"left": "DOWN", "right": "UP"},
    "Lipslide": {"left": "UP", "right": "DOWN"},
    "Noseslide": {"left": "UP", "right": "UP"},
    "Tailslide": {"left": "DOWN", "right": "DOWN"},
}

""" TEMPORARY PRINT SYSTEM """
import time
PRINT_COOLDOWN = 0.075
last_print_time = 0

def print_debug(message):
    global last_print_time
    current_time = time.time()
    if current_time - last_print_time > PRINT_COOLDOWN:
        print(message)
        last_print_time = current_time