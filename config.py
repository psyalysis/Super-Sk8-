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

# --- Display settings ---
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 675
FPS = 60

# --- Texture settings ---
FLOOR_TEXTURES_PATH = "./objects/"

# --- Camera settings ---
CAMERA_ZOOM = 2
CAMERA_SPEED = 8

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
ANIMATIONS = "animations/"
ANIMATION_FRAME_RATE = 24

# --- Sound settings ---
SOUND_PATHS = {
    "land": "SFX/land_",
    "pop": "SFX/pop_"
}
SOUND_VOLUME = 0.6

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

