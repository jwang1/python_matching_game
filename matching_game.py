"""exit python program from function"""
"""https://stackoverflow.com/questions/73663/terminating-a-python-script"""
from sys import exit

# https://stackoverflow.com/questions/2823316/generate-a-random-letter-in-python
import string
import random

"""
    # input:  grid size (nxm) ;  number of consecutive matching (cm) (which has to be less than min(n, m)

    # init grid  (need to make sure no consecutive matches)

    # print grid

    # game looping until quit

"""


"""Matching Game Class."""
class MatchingGame:

  # https://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
  # does python have such constant ?
  BOLD = '\033[1m'
  END = '\033[0m'

  QUIT = ('q', 'quit', 'Q', 'Quit')

  LITTLE_A_ORD = ord('a')
  LITTLE_Z_ORD = ord('z')

  GAME_BOARD_SET_BY_COMPUTER = True

  """Constants."""
  PROMPT_BOARD_ROW = "Please input the number of " + BOLD + "Rows" + END + " for the game board (must be number > 0): "
  PROMPT_BOARD_COL = "Please input the number of " + BOLD + "Columns" + END + " for the game board (must be number > 0): "
  PROMPT_CONSECUTIVE_MATCHES = "Please input " + BOLD + " Number of consecutive matches" + END + " for the game " \
                               "(note it has to be less or equal to the mininum of "
  USER_QUITS = "User quits game."

  """Initialize data members."""
  def __init__(self, autoGameSetting, randmoizeCells):
    self.score = 0
    self.hasMatches = False
    self.row = -1
    self.col = -1
    self.consecutiveMatch = -1
    self.quit = False
    self.autoGameSetting = autoGameSetting
    self.randomizeCells = randmoizeCells

    if self.autoGameSetting:
      self.row = 4
      self.col = 5
      self.consecutiveMatch = 3

    """Data structure for the matches"""
    # matches records the tuples of matching start-and-end index for a row, a column
    # for example:   {"rows": { {"1": (2, 6)}, {"3": (0, 3)} },
    #                 "cols": { {"3": (0, 3)}, {"6": (3, 7)} }
    #                }
    self.matches = {"rows": {}, "cols": {}}

    # set up game board
    self.setupGame()



  """User prompts, set up the board size, and defined consecutive matching"""
  def setupGame(self):
    if not self.autoGameSetting:
      self.promptUser()

    self.initBoard()
    self.checkMatches()
    self.printBoard()


  def initBoard(self):
    # list comprehension:
    # https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
    # https://stackoverflow.com/questions/12791501/python-initializing-a-list-of-lists
    self.board = [['0' for r in range(self.col)] for i in range(self.row)]

    if not self.randomizeCells:
      return

    for r in range(self.row):
      for c in range(self.col):
        self.board[r][c] = random.choice(string.ascii_lowercase)


  def printBoard(self):
    for r in range(self.row):
      print('-'*2*self.col)

      for c in range(self.col):
        # print without newline : https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space
        print('|' + self.board[r][c], end="", flush=True)

      print('|')

    print('-'*2*self.col)


  def checkMatches(self):
    colMatchStart = -1
    colMatchEnd = -1

    # handle rows matches
    for r in range(self.row):
      # for each row, starts the matching character at the beginning of the row
      rowMatchStart = 0
      rowMatchEnd = rowMatchStart
      matchingChar = self.board[r][0]

      for c in range(self.col):
        if self.board[r][c] == matchingChar:
          rowMatchEnd = c
        else:
          # check if previous matches (right before this point) reaches consecutiveMatch ?
          if rowMatchEnd - rowMatchStart >= self.consecutiveMatch:
            self.matches.get("rows")[str(r)] = (rowMatchStart, rowMatchEnd)

          # reset rowMatchStart index
          rowMatchStart = c
          matchingChar = self.board[r][c]

      # special case; all characters in that row are matched
      if rowMatchEnd - rowMatchStart >= self.consecutiveMatch:
        self.matches.get("rows")[str(r)] = (rowMatchStart, rowMatchEnd)


    # handle columns matches
    for c in range(self.col):
      colMatchStart = 0
      colMatchEnd = colMatchStart
      matchingChar = self.board[0][c]

      for r in range(self.row):
        if self.board[r][c] == matchingChar:
          colMatchEnd = r
        else:
          # check if previous matches (prior to this breaking point) reaches self.consecutiveMatch ?
          if colMatchEnd - colMatchStart >= self.consecutiveMatch:
            self.matches.get("cols")[str(c)] = (colMatchStart, colMatchEnd)

          # reset colMatchStart index
          colMatchStart = r
          matchingChar = self.board[r][c]

      # special case: all characters in that column are matched
      if colMatchEnd - colMatchStart >= self.consecutiveMatch:
        self.matches.get("cols")[str(c)] = (colMatchStart, colMatchEnd)




  def promptUser(self):
    self.promptRow()
    self.promptColumn()
    self.promptConsecutiveMatches()


  def promptConsecutiveMatches(self):
    while (self.consecutiveMatch < 2 or self.consecutiveMatch > min(self.row, self.col)):
      try:
        ipt = input(MatchingGame.PROMPT_CONSECUTIVE_MATCHES + " row (" + str(self.row)
                                        + ") and column (" + str(self.col) + "): ")
        if (ipt in MatchingGame.QUIT):
          self.quit = True

        self.consecutiveMatch = int(ipt)

      except:
        # pass  (python non-op)
        if self.quit:
          exit(MatchingGame.USER_QUITS)


  def promptRow(self):
    while self.row < 1:
      try:
        ipt = input(MatchingGame.PROMPT_BOARD_ROW)
        if ipt in MatchingGame.QUIT:
          self.quit = True

        self.row = int(ipt)

      except:
        if self.quit:
          exit(MatchingGame.USER_QUITS)


  def promptColumn(self):
    while self.col < 1:
      try:
        ipt = int(input(MatchingGame.PROMPT_BOARD_COL))

        if ipt in MatchingGame.QUIT:
          self.quit = True

        self.col = int(ipt)

      except:
        # pass
        if self.quit:
          exit(MatchingGame.USER_QUITS)


  """Initialize data members."""
  def playMatchingGame(self):
    print("\n" + "Let's start gaming: ")
    print(self.matches)



# main function
if __name__ == '__main__':
  uip = input("? Computer set up game board: ")
  if uip in ('yes', 'y', 'true', 'sure', 'ok', 'k'):
    uip = input ("? Randomize cells: ")
    if uip in ('no', 'n', 'nope', 'don\'t'):
      game = MatchingGame(MatchingGame.GAME_BOARD_SET_BY_COMPUTER, False)
    else:
      game = MatchingGame(MatchingGame.GAME_BOARD_SET_BY_COMPUTER, True)

  else:
    game = MatchingGame(not MatchingGame.GAME_BOARD_SET_BY_COMPUTER)

  game.playMatchingGame()
