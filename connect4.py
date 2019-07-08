import numpy as np
import pygame
import sys
import math

ROW_COUNT=6
COLUMN_COUNT=7
SQUARE_SIZE=100
RADIUS= int(SQUARE_SIZE/2)-5
BLUE=(50,50,200)
BLACK=(20,20,20)
PLAYER1_COLOR=(200,20,20)      # RED PLAYER 1
PLAYER2_COLOR=(200,200,0)      # YELLOW PLAYER 2

def create_board():
    board =np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board,row,col,piece):
    board[row][col]=piece

def is_valid_location(board,col):
    if col<0 or col>=COLUMN_COUNT:
        return False
    return board[ROW_COUNT-1][col]==0

def get_next_open_row(board,col):
    for row in range(ROW_COUNT):
        if board[row][col]==0:
            return row
    return -1

def print_board(board):
    print(np.flip(board,axis=0))

def game_won(board,piece):
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT-3):
            if board[row][col]==piece and board[row][col+1]==piece and board[row][col+2]==piece and board[row][col+3]==piece :
                return True

    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT):
            if board[row][col]== piece and board[row+1][col]==piece and board[row + 2][col] == piece and board[row + 3][col] == piece:
                return True

    for row in range(ROW_COUNT-3):
        for col in range(COLUMN_COUNT-3 ):
            if board[row][col]==piece and board[row+1][col+1]==piece and board[row+2][col+2]==piece and board[row+3][col+3]==piece :
                return True

    for row in range(3,ROW_COUNT):
        for col in range(COLUMN_COUNT-3 ):
            if board[row][col]==piece and board[row-1][col+1]==piece and board[row-2][col+2]==piece and board[row-3][col+3]==piece :
                return True
    return False

def draw_board(board):
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE+SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == 1:
                pygame.draw.circle(screen, PLAYER1_COLOR, ( int(col * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, PLAYER2_COLOR, ( int(col * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()

if __name__ == '__main__':

    pygame.init()
    MY_FONT = pygame.font.SysFont("casual", 100)
    width= COLUMN_COUNT*SQUARE_SIZE
    height=(ROW_COUNT+1)*SQUARE_SIZE
    screen_size=(width,height)
    screen =pygame.display.set_mode(screen_size)

    board=create_board()
    draw_board(board)

    GAME_OVER=False
    turn=1
    piece=1
    while not GAME_OVER:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()

            if event.type==pygame.MOUSEMOTION:
                pos_x=event.pos[0]
                pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
                if turn==1:
                    pygame.draw.circle(screen,PLAYER1_COLOR,(pos_x,int(SQUARE_SIZE/2)),RADIUS)
                else:
                    pygame.draw.circle(screen,PLAYER2_COLOR,(pos_x,int(SQUARE_SIZE/2)),RADIUS)
                pygame.display.update()
            if event.type==pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                pygame.display.update()
                # ask for player 1 input
                if turn == 1:
                    piece = 1
                    pos_x=event.pos[0]
                    col = int(math.floor(pos_x/SQUARE_SIZE))
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, piece)
                        if game_won(board, piece):
                            label = MY_FONT.render("Player 1 wins!!", 1, PLAYER1_COLOR)
                            screen.blit(label,(100, 20))
                            GAME_OVER= True
                        turn = (turn + 1) % 2
                # ask for player2 input
                elif turn == 0:
                    piece = 2
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / SQUARE_SIZE))
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, piece)
                        if game_won(board, piece):
                            label = MY_FONT.render("Player 2 wins!!", 1, PLAYER2_COLOR)
                            screen.blit(label, (100, 20))
                            GAME_OVER = True

                        turn = (turn + 1) % 2


                draw_board(board)
    pygame.time.wait(3000)
