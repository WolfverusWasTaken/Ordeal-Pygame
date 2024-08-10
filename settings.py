# settings.py

# Room and display settings
WIDTH = 700
HEIGHT = 700
ROOM_SIZE = 600
WALL_THICKNESS = 10
CHAR_SIZE = 30
BLUE_SQUARE_SIZE = 20
CHAR_SPEED = 10
BLUE_SQUARE_SPEED = 2
BLINK_INTERVAL = 500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)


# Room boundaries
def get_room_boundaries(start_x, start_y):
    return {
        "LEFT": start_x,
        "RIGHT": start_x + ROOM_SIZE,
        "TOP": start_y,
        "BOTTOM": start_y + ROOM_SIZE,
    }


# Targeting Modes
TARGET_MODES = ["Red", "Blue"]
CURRENT_TARGET_INDEX = 0  # Index of the currently targeted blue square
TARGET_MODE = "Red"  # Initial target mode
