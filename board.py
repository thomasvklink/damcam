# This is a class for the checkers board
import pygame
from constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from piece import Piece

import math


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        self.skip_check = 0

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            # while piece == 0 or row <= ROWS or row >= -1 or self.skip_check <= 1:
            #     left += piece.col - 1
            #     right += piece.col + 1
            # if piece != 0:
            #     self.skip_check + 1
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        # if piece.king:
        #     while piece == 0 or ROWS or -1 or self.skip_check <= 1:
        #         left+1
        #         right+1
        #     if piece != 0:
        #         self.skip_check + 1
        #     moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
        #     moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        #     moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
        #     moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        jump = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                for skipped in moves:
                    moves = skipped
                if skipped and not jump:
                    break
                elif skipped:
                    moves.clear()
                    moves[(r, left)] = jump + skipped
                else:
                    moves[(r, left)] = jump

                if jump:
                    # moves.clear()
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, jump))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, jump))
                break
            elif current.color == color:
                break
            else:
                jump = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        jump = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not jump:
                    break
                elif skipped:
                    moves[(r, right)] = jump + skipped
                else:
                    moves[(r, right)] = jump

                if jump:
                    # moves.clear()
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, jump))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1,jump))
                break
            elif current.color == color:
                break
            else:
                jump = [current]

            right += 1

        return moves

    def combine_input(self):
        # if there is a white piece do not override the board \ else do override and check if there is a piece in that square
        math.map()
        pass