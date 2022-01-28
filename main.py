# AI Practise Final project by Thomas van Klink & Tristan van Marle
# Made 17-01-2022
# Inspiration taken from Tech by Tim:https://www.youtube.com/playlist?list=PLzMcBGfZo4-lkJr3sqpikNyVzbNZLRiT3

# Importing variables
import keyboard
import pygame
from constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, RED
from game import Game
from algorithm import minmax
from input import Input
from board import Board
import copy

# Setting variables for pygame
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Damcam - Hybrid Checkers')

# method for returning on which row and column the mouse is
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Main method for running the code as well as running methods from other classes.
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    input = Input()
    board = Board()
    current_board = copy.deepcopy(input.board)

    while run:
        clock.tick(FPS)
        # print([piece.row for piece in board.get_all_pieces(RED)])

        if game.turn == WHITE:
            value, new_board = minmax(game.get_board(), 4, WHITE, game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

            # Launch continious circle detection, for setting up the system
            if keyboard.is_pressed("p"):
                input.continuous_detection()

            # After the user plays a move you hit your spacebar to switch turn and without reading the board and updating it
            if keyboard.is_pressed("space"):
                input.single_detection()
                new_board = copy.deepcopy(input.board)
                changed_tiles = []
                # Compare both board to see what move has been made
                for key,old in current_board.items():
                    if old != new_board[key]:
                        changed_tiles.append(key)
                print("Tiles that have changed: " + changed_tiles)
                # Save current board
                current_board = new_board

                if len(changed_tiles) == 2:
                    if new_board[changed_tiles[0]] == 0:
                        # row,col = board.get_row_col_from_pos(changed_tiles[0])
                        # piece: Piece = board.get_piece(row, col)
                        # game.select(int(row), int(col))
                        # row, col = board.get_row_col_from_pos(changed_tiles[1])
                        # game.select(int(row), int(col))
                        # piece.move(0, 0)
                        game.selected = False
                        row, col = get_row_col_from_mouse(changed_tiles[0])
                        game.select(row, col)
                        row, col = get_row_col_from_mouse(changed_tiles[1])
                        game.select(row, col)
                        # print(piece)
                    else:
                        # row, col = board.get_row_col_from_pos(changed_tiles[1])
                        # piece: Piece = board.get_piece(row, col)
                        # game.select(int(row), int(col))
                        # row, col = board.get_row_col_from_pos(changed_tiles[0])
                        # game.select(int(row), int(col))
                        # piece.move(0, 0)
                        game.selected = False
                        row, col = get_row_col_from_mouse(changed_tiles[1])
                        game.select(row, col)
                        row, col = get_row_col_from_mouse(changed_tiles[0])
                        game.select(row, col)
                        # print(piece)
        game.update()

    pygame.quit()

if __name__=="__main__":
    main()