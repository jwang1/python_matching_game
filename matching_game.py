"""exit python program from function"""
"""https://stackoverflow.com/questions/73663/terminating-a-python-script"""
from sys import exit


"""Matching Game Class."""
class MatchingGame:

  # https://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
  # does python have such constant ?
  BOLD = '\033[1m'
  END = '\033[0m'

  QUIT = 'q'

  """Constants."""
  PROMPT_BOARD_ROW = "Please input the number of " + BOLD + "Rows" + END + " for the game board (must be number > 0): "
  PROMPT_BOARD_COL = "Please input the number of " + BOLD + "Columns" + END + " for the game board (must be number > 0): "
  PROMPT_CONSECUTIVE_MATCHES = "Please input " + BOLD + " Number of consecutive matches" + END + " for the game " \
                               "(note it has to be less or equal to the mininum of "
  USER_QUITS = "User quits game."

  """Initialize data members."""
  def __init__(self):
    self.row = -1
    self.col = -1
    self.consecutiveMatch = -1
    self.quit = False
    self.setupGame()

  """User prompts, set up the board size, and defined consecutive matching"""
  def setupGame(self):
    while self.row < 1 or self.col < 1 or self.consecutiveMatch > min(self.row, self.col):
      self.promptUser()


  def promptUser(self):
    self.promptRow()
    self.promptColumn()
    self.promptConsecutiveMatches()

  def promptConsecutiveMatches(self):
    while (self.consecutiveMatch < 2 or self.consecutiveMatch > min(self.row, self.col)):
      try:
        ipt = int(input(MatchingGame.PROMPT_CONSECUTIVE_MATCHES + " row (" + str(self.row)
                                        + ") and column (" + str(self.col) + "): "))
        if (ipt == MatchingGame.QUIT):
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
        if ipt == MatchingGame.QUIT:
          self.quit = True

        self.row = int(ipt)

      except:
        if self.quit:
          exit(MatchingGame.USER_QUITS)


  def promptColumn(self):
    while self.col < 1:
      try:
        ipt = int(input(MatchingGame.PROMPT_BOARD_COL))

        if ipt == MatchingGame.QUIT:
          self.quit = True

        self.col = int(ipt)

      except:
        # pass
        if self.quit:
          exit(MatchingGame.USER_QUITS)

  """Initialize data members."""
  def playMatchingGame(self):
    print(self.row)

    # input:  grid size (nxm) ;  number of consecutive matching (cm) (which has to be less than min(n, m)

    # init grid  (need to make sure no consecutive matches)

    # print grid

    # game looping until quit



# main function
if __name__ == '__main__':
  game = MatchingGame()
  game.playMatchingGame()
