import pygame, random, sys
from pygame.locals import *

class MatchingPyGame:

  FPS = 30
  WINDOW_WIDTH = 640
  WINDOW_HEIGHT = 480

  REVEAL_SPEED = 8
  BOX_SIZE = 40
  GAP_SIZE = 10

  BOARD_WIDTH = 10  # nbr of columns of icons
  BOARD_HEIGHT = 8  # nbr of rows of icons

  # for future improvement
  EMOJIS = ['🍌', '🍒', '🍐', '🍈', '🍇', '🍊', '🍉']

  X_MARGIN = int((WINDOW_WIDTH - BOARD_WIDTH * (BOX_SIZE + GAP_SIZE)) / 2)
  Y_MARGIN = int((WINDOW_HEIGHT - BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE)) / 2)

  #            R    G    B
  GRAY     = (100, 100, 100)
  NAVYBLUE = ( 60,  60, 100)
  WHITE    = (255, 255, 255)
  RED      = (255,   0,   0)
  GREEN    = (  0, 255,   0)
  BLUE     = (  0,   0, 255)
  YELLOW   = (255, 255,   0)
  ORANGE   = (255, 128,   0)
  PURPLE   = (255,   0, 255)
  CYAN     = (  0, 255, 255)

  BG_COLOR = NAVYBLUE
  LIGHT_BG_COLOR = GRAY
  BOX_COLOR = WHITE
  HIGHLIGHT_COLOR = BLUE

  DONUT = 'donut'
  SQUARE = 'square'
  DIAMOND = 'diamond'
  LINES = 'lines'
  OVAL = 'oval'

  ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
  ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)


  """initialize data members."""
  def __init__(self):
    print("TODO: add some data memeber")




# main function
if __name__ == '__main__':
  game = MatchingPyGame()

  game.play()
