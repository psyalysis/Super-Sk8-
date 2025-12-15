"""Essential settings/configuration module."""

# --- Debug Settings ---
DEBUG_TEXT_VISIBLE = True
DEBUG_PRINT_VISIBLE = False

# --- Font settings ---
FONT_PATH = "fonts/ari-w9500.ttf"
FONT_BOLD_PATH = "fonts/ari-w9500-bold.ttf"
FONT_SIZE_SMALL = 16
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 32

# --- Display settings --- chatgpt
# Supported resolutions
SUPPORTED_RESOLUTIONS = [
    (800, 600),    # 4:3
    (1024, 768),   # 4:3
    (1280, 720),   # 16:9
    (1200, 675),   # 16:9 (default)
    (1366, 768),   # 16:9
    (1600, 900),   # 16:9
    (1920, 1080),  # 16:9
]

DISPLAY_WIDTH = 1100
DISPLAY_HEIGHT = 750
FPS = 60

# --- Texture settings ---
FLOOR_TEXTURES_PATH = "./objects/"

# --- Camera settings ---
CAMERA_ZOOM = 1.25
CAMERA_SPEED = 8

# --- Skateboard display settings ---
SKATEBOARD_OFFSET_X = 150
SKATEBOARD_OFFSET_Y = 165

# --- Colors ---
COLORS = {
    'primary': (52, 73, 94),
    'background': (0, 0, 0),
    'accent': (241, 196, 15),
    'success': (39, 174, 96),
    'danger': (192, 57, 43),
    'white': (236, 240, 241),
    'black': (22, 22, 22),
    'gray': (127, 140, 141),
    'warning': (241, 196, 15),
    'info': (39, 174, 96),
}

# --- Animation settings ---
ANIMATIONS = "animations/flip/"
ANIMATION_FRAME_RATE = 30

# --- Grind settings ---
GRIND_ANIMATIONS = "animations/grind/"
GRIND_SPEED = 1.0

# --- Sound settings ---
SOUND_PATHS = {
    "land": "SFX/land_",
    "pop": "SFX/pop_"
}
SOUND_VOLUME = 0.1
MASTER_VOLUME = 0.1

# --- Key mappings ---
import pygame

KEY_MAPPINGS = {
    pygame.K_w: 'left-up',
    pygame.K_s: 'left-down',
    pygame.K_a: 'left-left',
    pygame.K_d: 'left-right',
    pygame.K_RETURN: 'enter',
    pygame.K_ESCAPE: 'escape',
    pygame.K_i: 'right-up',
    pygame.K_k: 'right-down',
    pygame.K_j: 'right-left',
    pygame.K_l: 'right-right',
}

# --- Trick Controls ---
FLIP_CONTROLS = {
    "Kickflip": {
        "keys": [["left-left", False], ["right-down", False]]
    },
    "Heelflip": {
        "keys": [["left-left", False], ["right-up", False]]
    },
    "Varial Kickflip": {
        "keys": [["left-down", False], ["right-down", False]]
    },
    "Varial Heelflip": {
        "keys": [["left-up", False], ["right-up", False]]
    },
    "Hardflip": {
        "keys": [["left-up", False], ["right-down", False]]
    },
    "Inward Heelflip": {
        "keys": [["left-down", False], ["right-up", False]]
    },
    "BS-Shuv": {
        "keys": [["left-down", False], ["right-left", False]]
    },
    "FS-Shuv": {
        "keys": [["left-up", False], ["right-left", False]]
    },
    "360 Hardflip": {
        "keys": [["left-up", True], ["right-down", False]]
    },
    "360 Inward Heelflip": {
        "keys": [["left-down", True], ["right-up", False]]
    },
    "Tre Flip": {
        "keys": [["left-down", True], ["right-down", False]]
    },
    "Lazer Flip": {
        "keys": [["left-up", True], ["right-up", False]]
    }
}

FLIP_SPEEDS = {
    "Kickflip": 1.5,
    "Heelflip": 1.5,
    "Varial Kickflip": 1.75,
    "Varial Heelflip": 1.75,
    "Hardflip": 1.85,
    "Inward Heelflip": 1.85,
    "BS-Shuv": 1.7,
    "FS-Shuv": 1.7,
    "360 Hardflip": 1.8,
    "360 Inward Heelflip": 1.8,
    "Tre Flip": 1.4,
    "Lazer Flip": 1.4,
}

GRIND_CONTROLS = {
    "50-50 Grind": ["left-left", "right-right"],

    "5-0 Grind": ["left-left", "right-left"],
    "Nose Grind": ["left-right", "right-right"],

    "Overcrooked Grind": ["left-up", "right-right"],
    "Crooked Grind": ["left-down", "right-right"],

    "Losi Grind": ["left-up", "right-right"],
    "Lazy Grind": ["left-down", "right-left"],

    "Salad Grind": ["left-left", "right-up"],
    "Suski Grind": ["left-left", "right-down"],

    "Feeble Grind": ["left-right", "right-up"],
    "Smith Grind": ["left-right", "right-down"],

    "Noseslide": ["left-up", "right-up"],
    "Tailslide": ["left-down", "right-down"],

    "Boardslide": ["left-down", "right-up"],
    "Lipslide": ["left-up", "right-down"],

}
# ["left-down", "right-left"]

# ["left-right", "right-left"]


# ["left-up", "right-left"]
