
class Colors():
    """Class that contains all the most common colors"""

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    GRAY = (128, 128, 128)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    BROWN = (165, 42, 42)
    PINK = (255, 192, 203)
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    BEIGE = (245, 245, 220)


class Game_properties():
    """Class that stores all the game properties"""
    WIDTH = 1024
    HEIGHT = 768
    TICK_RATE = 30
    TITLE = 'Pong by LSTEP'
    VELOCITY = 10
    MIN_BALL_VELOCITY = 10
    MAX_BALL_VELOCITY = 20
    BACKGROUND_COLOR = Colors.BEIGE