#This is a folder for all the constants for the checkers game

import pygame

# -- Game constants --

# Size
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
GREEN = (0, 255, 0)

# Images

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

# -- Input constants --

# Default Hough Circle Detection parameters
param1 = 28
param2 = 50
minRadius = 20
maxRadius = 135

# Define which webcam input you use
webcam = 0
webcam_width = 1280
webcam_height = 720

# Definitions for Logitech HD720
board_size = 720
offset = 1280/4-30

