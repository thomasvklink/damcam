# This is a class responsible for handling game events
import pygame
from .constants import RED, WHITE
from checkers.board import Board

class Game:
    def __init__(self, win):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.win = win

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()
