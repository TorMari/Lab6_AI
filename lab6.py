import pygame
import sys
import time
from pygame.locals import *

WIDTH = 400
HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100), 0, 32)


x_img = pygame.image.load('C:\\Users\\user\\Desktop\\AI\\x_img.png')
o_img = pygame.image.load('C:\\Users\\user\\Desktop\\AI\\o_img.png')

new_width = 80
new_height = 80

x_img = pygame.transform.scale(x_img, (new_width, new_height))
o_img = pygame.transform.scale(o_img, (new_width, new_height))

board = [['_']*3 for _ in range(3)]

step = 0
evaluation = 0
winner = None
draw = None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def game_init():
   screen.fill(WHITE)
   pygame.draw.line(screen, BLACK, (WIDTH/3, 0), (WIDTH/3, HEIGHT), 7)
   pygame.draw.line(screen, BLACK, (WIDTH/3*2, 0), (WIDTH/3*2, HEIGHT), 7)
   pygame.draw.line(screen, BLACK, (0, HEIGHT/3), (WIDTH, HEIGHT/3), 7)
   pygame.draw.line(screen, BLACK, (0, HEIGHT*2/3), (WIDTH, HEIGHT*2/3), 7)
   game_status()


RED = (255, 0, 0)
RED_DARKER = (230, 0, 0)
GREEN_DARKER = (0, 153, 51)
BLUE_DARKER = (0, 115, 230)

def game_status():
   global draw, step, winner
   if winner is None:
      turn_status = 'AI`s turn' if step % 2 == 1 else 'Your`s turn'
   else:
      turn_status = 'AI is winner!' if winner == 'X' else 'You`re winner!'
   if draw:
      turn_status = 'Game draw'

   font = pygame.font.Font(None, 33)
   text = font.render(turn_status, True, WHITE)

   if turn_status == 'You`re winner!':
      text_color = GREEN_DARKER
   elif turn_status == 'AI is winner!':
      text_color = RED_DARKER
   elif turn_status == 'Game draw':
      text_color = BLUE_DARKER
   else:
      text_color = BLACK

   screen.fill(text_color, (0, 400, 500, 100))
   text_area = text.get_rect(center=(WIDTH/2, 500 - 50))
   screen.blit(text, text_area)
   pygame.display.update()


def check_win(depth, status):
   global board, winner, draw
   for row in range(3):
      if board[row][0] == board[row][1] == board[row][2] and (board[row][0] != '_'):
         if status == 'Evaluate':
            return 10 - depth if board[row][0] == 'X' else depth-10
         else:
            winner = board[row][0]
            pygame.draw.line(screen, RED, (0, (row + 1)*HEIGHT/3 - HEIGHT/6), 
                             (WIDTH, (row+1)*HEIGHT/3 - HEIGHT/6), 4)
         break

   for col in range(3):
      if board[0][col] == board[1][col] == board[2][col] and (board[0][col] != '_'):
         if status == 'Evaluate':
            return 10-depth if board[0][col] == 'X' else depth-10
         else:
            winner = board[0][col]
            pygame.draw.line(screen, RED, ((col+1)*WIDTH/3 - WIDTH/6, 0),
                             ((col+1)*WIDTH/3-WIDTH/6, HEIGHT), 4)
         break

   if board[0][0] == board[1][1] == board[2][2] and (board[0][0] != '_'):
      if status == 'Evaluate':
         return 10-depth if board[0][0] == 'X' else depth-10
      else:
         winner = board[0][0]
      pygame.draw.line(screen, RED, (50, 50), (350, 350), 4)

   if board[0][2] == board[1][1] == board[2][0] and (board[0][2] != '_'):
      if status == 'Evaluate':
         return 10-depth if board[0][2] == 'X' else depth-10
      else:
         winner = board[0][2]
      pygame.draw.line(screen, RED, (350, 50), (50, 350), 4)

   if winner is None and step == 9:
      draw = True

   if status == 'Evaluate':
      return 0
   
   game_status()



def insert_img(row, col):
    global board, step
    if row == 1:
        pos_y = 30
    elif row == 2:
        pos_y = HEIGHT / 3 + 30
    elif row == 3:
        pos_y = HEIGHT / 3 * 2 + 30

    if col == 1:
        pos_x = 25
    elif col == 2:
        pos_x = WIDTH / 3 + 25
    elif col == 3:
        pos_x = WIDTH / 3 * 2 + 25

    board[row - 1][col - 1] = 'X' if step % 2 == 1 else '0'

    if step % 2 == 1:
        screen.blit(x_img, (pos_x, pos_y))
    else:
        screen.blit(o_img, (pos_x, pos_y))

    step += 1
    pygame.display.update()



def check_mouse_click():
    global board, step
    x, y = pygame.mouse.get_pos()

    if x < WIDTH / 3:
        col = 1
    elif x < WIDTH / 3 * 2:
        col = 2
    elif x < WIDTH:
        col = 3
    else:
        col = None

    if y < HEIGHT / 3:
        row = 1
    elif y < HEIGHT / 3 * 2:
        row = 2
    elif y < HEIGHT:
        row = 3
    else:
        row = None

    if (row is not None) and (col is not None) and board[row - 1][col - 1] == '_':
        insert_img(row, col)
        check_win(0, 'Check')



def check_endgame():
   global board
   for i in range(3):
      for j in range(3):
         if board[i][j] == '_':
            return True
   return False


def minimax(depth, is_max, score):
   global board
   new_score = check_win(depth, 'Evaluate')
   if is_max and new_score > score:
      return new_score
   if not is_max and new_score < score:
      return new_score
   if not check_endgame():
      return 0
   
   if is_max:
      best = -1000
      for i in range(3):
         for j in range(3):
            if board[i][j] == '_':
               board[i][j] = 'X'
               best = max(best, minimax(depth+1, not is_max, new_score))
               board[i][j] = '_'
      return best
   else:
      best = 1000
      for i in range(3):
         for j in range(3):
            if board[i][j] == '_':
               board[i][j] = '0'
               best = min(best, minimax(depth+1, not is_max, new_score))
               board[i][j] = '_'
      return best


def find_best_move():
   global board
   best_value = -1000
   best_move = (-1, -1)
   for i in range(3):
      for j in range(3):
         if board[i][j] == '_':
            board[i][j] = 'X'
            score = check_win(0, 'Evaluate')
            move_value = minimax(0, False, score)
            board[i][j] = '_'
            if move_value > best_value:
               best_move = (i, j)
               best_value = move_value
   time.sleep(0.5)
   return best_move


def reset_game():
   global board, winner, step, evaluation, draw
   time.sleep(3)
   step = 0
   evaluation = 0
   draw = False
   winner = None
   board = [['_']*3 for _ in range(3)]
   game_init()


FPS = 60
CLOCK = pygame.time.Clock()

game_init()
while True:
   if step % 2 == 0:
      for event in pygame.event.get():
         if event.type == QUIT:
            pygame.quit()
            sys.exit()
         elif event.type == MOUSEBUTTONDOWN:
            check_mouse_click()
            if winner or draw:
               reset_game()

   else: 
      best_ai_move = find_best_move()
      insert_img(best_ai_move[0] +1, best_ai_move[1]+1)
      check_win(0, 'Check')
      if winner or draw:
         reset_game()

   pygame.display.update()
   CLOCK.tick(FPS)
