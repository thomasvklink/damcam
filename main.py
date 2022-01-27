# AI Practise Final project by Thomas van Klink & Tristan van Marle
# Made 17-01-2022
# Inspiration taken from Tech by Tim:https://www.youtube.com/playlist?list=PLzMcBGfZo4-lkJr3sqpikNyVzbNZLRiT3

# Importing variables
import pygame
from constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from game import Game
from algorithm import minimax
import input


# Setting variables for pygame
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
print(FPS)
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

    while run:
        print("run")
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, WHITE, game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            # run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()



if __name__=="__main__":
    print("HALLO!")
    main()