"""Game configuration constants."""

FPS = 60
ANIMATION_FRAME_RATE = 45
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
CAMERA_SPEED = 300

# Trick patterns: trick name -> {left/right hand -> direction from input.Direction}
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

TRICK_SCORE_MAP = {
    "Kickflip": 100,
    "Heelflip": 100,
    "BS-Shuv": 100,
    "FS-Shuv": 100,
    "Varial Kickflip": 150,
    "Varial Heelflip": 150,
    "Hardflip": 200,
    "Inward Heelflip": 200,
    "5-0": 150,
    "50-50": 100,
    "Nose": 150,
    "Crooked": 200,
    "Overcrooked": 200,
    "Smith": 200,
    "Feeble": 200,
    "Lazy": 200,
    "Losi": 200,
    "Suski": 200,
    "Salad": 200,
    "Boardslide": 100,
    "Lipslide": 100,
    "Noseslide": 150,
    "Tailslide": 150,
}