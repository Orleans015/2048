"""
This script is the main script for the 2048 game. It contains the main game loop
and the functions that are used to play the game.
"""

import random
import sys
import os
import time
import numpy as np

# Constants
EMPTY = 0
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
SIZE = 4
WIN_VALUE = 'inf'
MAX_VALUE = 2048

# Functions
def print_board(board):
  """
  Print the board to the console.
  """
  print(board)
  
def get_empty_cells(board):
  """
  Get the empty cells on the board.
  """
  return list(zip(*np.where(board == EMPTY)))

def add_new_tile(board):
  """
  Add a new tile to the board. The new tile must be added to an empty cell 
  that is chosen form the empty cells on the board. however the new tile must
  be either 2 or 4 with a 90% and 10% probability respectively, moreover the
  new tile must be added to an empty cell that is the furthest from the
  empty border with respect to the direction of the move.
  """
  empty_cells = get_empty_cells(board)
  if empty_cells:
    i, j = random.choice(empty_cells)
    board[i, j] = 2 if random.random() < 0.9 else 4
  return board

def move(board, direction):
  """
  Move all the tiles in the given direction until they reach a border or
  another tile they cannot merge with.
  """
  if direction == UP:
    for i in range(SIZE):
      # remove the zeros and put them at the end of the column
      board[:, i] = np.concatenate((board[board[:, i] != EMPTY, i], np.zeros(board[board[:, i] == EMPTY, i].shape)))
      # now merge the tiles
      for j in range(SIZE - 1):
        if board[j, i] == board[j + 1, i]:
          board[j, i] *= 2
          board[j + 1, i] = EMPTY
      board[:, i] = np.concatenate((board[board[:, i] != EMPTY, i], np.zeros(board[board[:, i] == EMPTY, i].shape)))
  elif direction == DOWN:
    for i in range(SIZE):
      # remove the zeros and put them at the beginning of the column
      board[:, i] = np.concatenate((np.zeros(board[board[:, i] == EMPTY, i].shape), board[board[:, i] != EMPTY, i]))
      # now merge the tiles
      for j in range(SIZE - 1, 0, -1):
        if board[j, i] == board[j - 1, i]:
          board[j, i] *= 2
          board[j - 1, i] = EMPTY
      board[:, i] = np.concatenate((np.zeros(board[board[:, i] == EMPTY, i].shape), board[board[:, i] != EMPTY, i]))
  elif direction == LEFT:
    for i in range(SIZE):
      # remove the zeros and put them at the end of the row
      board[i, :] = np.concatenate((board[i, board[i, :] != EMPTY], np.zeros(board[i, board[i, :] == EMPTY].shape)))
      # now merge the tiles
      for j in range(SIZE - 1):
        if board[i, j] == board[i, j + 1]:
          board[i, j] *= 2
          board[i, j + 1] = EMPTY
      board[i, :] = np.concatenate((board[i, board[i, :] != EMPTY], np.zeros(board[i, board[i, :] == EMPTY].shape)))
  elif direction == RIGHT:
    for i in range(SIZE):
      # remove the zeros and put them at the beginning of the row
      board[i, :] = np.concatenate((np.zeros(board[i, board[i, :] == EMPTY].shape), board[i, board[i, :] != EMPTY]))
      # now merge the tiles
      for j in range(SIZE - 1, 0, -1):
        if board[i, j] == board[i, j - 1]:
          board[i, j] *= 2
          board[i, j - 1] = EMPTY
      board[i, :] = np.concatenate((np.zeros(board[i, board[i, :] == EMPTY].shape), board[i, board[i, :] != EMPTY]))
  return board

def is_game_over(board):
  """
  Check if the game is over.
  """
  for i in range(SIZE):
    for j in range(SIZE):
      if board[i, j] == EMPTY:
        return False
      if i < SIZE - 1 and board[i, j] == board[i + 1, j]:
        return False
      if j < SIZE - 1 and board[i, j] == board[i, j + 1]:
        return False
  return True

def is_win(board):
  """
  Check if the player has won the game.
  """
  return np.any(board == MAX_VALUE)

def main():
  """
  Main function for the 2048 game.
  """
  # Initialize the board
  board = np.zeros((SIZE, SIZE), dtype=int)
  board = add_new_tile(board)
  board = add_new_tile(board)

  # Main game loop
  while True:
    new_board = board.copy()
    os.system('clear')
    print_board(board)
    
    if is_game_over(board):
      print('Game Over!')
      break
    
    if is_win(board):
      print('You Win!')
      np.save(f'saved_games/board_{time.time()}.npy', board)
      break
    
    while np.array_equal(board, new_board):
      try:
        direction = int(input('Enter direction (1: up, 2: down, 3: left, 4: right, 0: save & exit): '))
        if direction == 0:
          print('Saving game status!')
          # if the saved_games directory does not exist, create it
          if not os.path.exists('saved_games'):
            os.makedirs('saved_games')
          np.save(f'saved_games/board_{time.time()}.npy', board)
          sys.exit()
      except ValueError:
          print('Invalid direction!')
          continue
      if direction in [UP, DOWN, LEFT, RIGHT]:
        board = move(board, direction)
      else:
        print('Invalid direction!')
  
    # if the move has been successful, add a new tile to the board
    board = add_new_tile(board)    
    time.sleep(1)

if __name__ == '__main__':
  main()