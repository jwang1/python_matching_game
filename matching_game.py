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

  DERANDOMIZER = 'a'

  MATCH_MARKER = '*'


  """Initialize data members."""
  def __init__(self, autoGameSetting, randmoizeCells, cellVals = string.ascii_lowercase):

    self.cellValues = cellVals

    self.isDebug = True

    self.score = 0

    # might use self.matchesInOneRound, instead of self.foundMatches
    self.foundMatches = False
    self.matchesInOneRound = 0

    # Game board
    self.row = -1
    self.col = -1

    # how many consecutives are regarded as matches
    self.consecutiveMatch = -1

    # User quits playing?
    self.quit = False

    # Let computer set up game board?
    self.autoGameSetting = autoGameSetting

    # to randomize cells, useful for testing - deterministic consecutive matches
    self.randomizeCells = randmoizeCells

    # Computer always set Game Board 4x5, and requires 3 consecutives to be treated as matches.
    if self.autoGameSetting:
      self.row = 4
      self.col = 5
      self.consecutiveMatch = 3

    """Data structure for the matches"""
    # matches records the tuples of matching start-and-end index for a row, a column
    # for example:   {"rows": { {1: (2, 6)}, {3: (0, 3)} },
    #                 "cols": { {3: (0, 3)}, {6: (3, 7)} }
    #                }
    # Note, the above start-end index; the end-index is INCLUSIVE!
    #
    self.matches = {"rows": {}, "cols": {}}

    # set up game board
    self.setupGame()


  # overrides the cell values (useful for testing, small cellVals, can get more matches; otherwise, 26 lowercase
  # letters not easy to get consecutive matches)
  def setCellValues(self, cellVals):
    self.cellValues = cellVals


  """User prompts, set up the board size, and defined consecutive matching"""
  def setupGame(self):
    if not self.autoGameSetting:
      self.promptUser()

    self.initBoard()

    self.debugMatchingGame("__________BEFORE checking consecutive matches_____________\n")
    self.printBoard()


    self.checkMatches()

    # For testing game, if not randomzing cells, no need to checkMatches again.  Game Board is initialized up to here.
    if not self.randomizeCells:
      self.markMatches()
      self.replaceMatchMarker()
      self.printBoard()
      return

    # keep checkMatches until there are no matches, that is, Game Board is completed
    # initialization - no matches on the init-board; users can make move now on; Scores will be taken for user's move
    while self.matchesInOneRound > 0:
      # TODO: randomize the matched cells, to randomize the Board;  Or, instead randomize, let's sinkCells
      self.markMatches()
      self.replaceMatchMarker()

      # check matches again
      self.checkMatches()

      self.debugMatchingGame("# of matches : " + str(self.matchesInOneRound))

    print("__________AFTER checking consecutive matches (ready to play)_____________\n")
    self.printBoard()


  def initBoard(self):
    # list comprehension:
    # https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
    # https://stackoverflow.com/questions/12791501/python-initializing-a-list-of-lists
    self.board = [['0' for r in range(self.col)] for i in range(self.row)]

    if not self.randomizeCells:
      # for testing purpose, let's make 2nd row with matches, and 3rd column with matches
      self.deRandomizeRow(1)
      self.deRandomizeCol(2)
      return

    for r in range(self.row):
      for c in range(self.col):
        self.board[r][c] = random.choice(self.cellValues)


  def printBoard(self):
    for r in range(self.row):
      print('-'*2*self.col)

      for c in range(self.col):
        # print without newline : https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space
        print('|' + self.board[r][c], end="", flush=True)

      print('|')

    print('-'*2*self.col)


  def checkMatches(self):
    # matches for this round of checking
    # initialize to 0; so that we can use this value to check whether there are still matches.
    self.matchesInOneRound = 0
    self.matches =  {"rows": {}, "cols": {}}

    colMatchStart = -1
    colMatchEnd = -1

    # handle rows matches
    for r in range(self.row):
      # for each row, starts the matching character at the beginning of the row
      rowMatchStart = 0
      rowMatchEnd = rowMatchStart
      matchingChar = self.board[r][0]

      for c in range(self.col):
        if matchingChar.isalpha() and self.board[r][c] == matchingChar:
          rowMatchEnd = c
        else:
          # check if previous matches (right before this point) reaches consecutiveMatch ?
          if rowMatchEnd - rowMatchStart + 1 >= self.consecutiveMatch:
            self.matches.get("rows")[r] = (rowMatchStart, rowMatchEnd)
            self.matchesInOneRound += rowMatchEnd - rowMatchStart + 1
            self.foundMatches = True

          # reset rowMatchStart index
          rowMatchStart = c
          matchingChar = self.board[r][c]

      # special case; all characters in that row are matched
      if rowMatchEnd - rowMatchStart + 1 >= self.consecutiveMatch:
        self.matches.get("rows")[r] = (rowMatchStart, rowMatchEnd)
        self.matchesInOneRound += rowMatchEnd - rowMatchStart + 1
        self.foundMatches = True


    # handle columns matches
    for c in range(self.col):
      colMatchStart = 0
      colMatchEnd = colMatchStart
      matchingChar = self.board[0][c]

      for r in range(self.row):
        if matchingChar.isalpha() and self.board[r][c] == matchingChar:
          colMatchEnd = r
        else:
          # check if previous matches (prior to this breaking point) reaches self.consecutiveMatch ?
          if colMatchEnd - colMatchStart + 1 >= self.consecutiveMatch:
            self.matches.get("cols")[c] = (colMatchStart, colMatchEnd)
            self.matchesInOneRound += colMatchEnd - colMatchStart + 1
            self.foundMatches = True

          # reset colMatchStart index
          colMatchStart = r
          matchingChar = self.board[r][c]

      # special case: all characters in that column are matched
      if colMatchEnd - colMatchStart + 1 >= self.consecutiveMatch:
        self.matches.get("cols")[c] = (colMatchStart, colMatchEnd)
        self.matchesInOneRound += colMatchEnd - colMatchStart + 1
        self.foundMatches = True

    self.debugMatchingGame('{} self.matchesInOneRound is {}, matching-indexes: {}'
          .format("checkMatches()", self.matchesInOneRound, self.matches))


  """Mark matches with MATCH_MARKER"""
  def markMatches(self):
    for row, startEnd in self.matches.get("rows").items():
      # Python format String : https://pyformat.info/
      self.debugMatchingGame('{} {} {}'.format("row=", row, startEnd))
      for c in range(startEnd[0], startEnd[1] + 1):
        self.board[row][c] = MatchingGame.MATCH_MARKER

    for col, startEnd in self.matches.get("cols").items():
      self.debugMatchingGame('{} {} {}'.format("col=", col, startEnd))
      for r in range(startEnd[0], startEnd[1] + 1):
        self.board[r][col] = MatchingGame.MATCH_MARKER


  """Replace Match Markers"""
  def replaceMatchMarker(self):
    # the algorithm:
    # 1. check each column,
    # 2. from bottom of the column to the top of the column
    # 3. record the start and end of the MATCH_MARKERs
    # 4. Replace MATCH_MARKEs of (markerStart, markerEnd), with values from values from (0, markerEnd + 1);
    #    need to handle special case, when values above MATCH_MARKER for that column are NOT enough to cover MATCH_MARKERS,
    #    we need to randomily generate characters

    for c in range(self.col):
      startEndByCol = self.getStartEndIndexForMatchMarksByCol(c)

      if len(startEndByCol) > 0:
        # the value to be sunk; "sinkPos < 0" means no values on board for this column to sink, need to generate random value
        sinkPos = startEndByCol[0] -1

        # reverse traverse list (columnMatchMark-Start-Index, columnMatchMark-End-Index);
        # if exists, using existing value on that column to FILL IN marked cells
        # otherwise, using random generated value
        for r in range(startEndByCol[1], startEndByCol[0] -1, -1):
          if sinkPos < 0:
            self.board[r][c] = random.choice(self.cellValues)
          else:
            self.board[r][c] = self.board[sinkPos][c]
            sinkPos -= 1

        # after the sinking (replacing the markers), we still need to filling the cells sunk for the MATCH_MARKERs
        for r in range(startEndByCol[0]):
          self.board[r][c] = random.choice(self.cellValues)

    return


  """get start and end indexes for MACH_MARKERs in a column"""
  def getStartEndIndexForMatchMarksByCol(self, col):
    startEnd = ()
    start = -1
    end = -1

    for r in range(self.row):
      if self.board[r][col] == MatchingGame.MATCH_MARKER:
        if start < 0:
          start = r
        end = r

    if start >= 0:
      startEnd = (start, end)

    # print formatted tupple elements/values
    if len(startEnd) > 0:
      try:
        self.debugMatchingGame('{} {} got startEnd Indexes: ({}, {}) '.format("getStartEndIndexForMatchMarksByCol(...) checking column: ",
                                                  col, *startEnd))
      except IndexError:
        self.debugMatchingGame(startEnd)

    # the start-end-index can be None, ie, the tuple can be empty.
    return startEnd



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
    self.debugMatchingGame("\n" + "Let's start gaming: ")


  # Util api to derandomize cell by row
  def deRandomizeRow(self, row):
    for c in range(self.col):
      self.board[row][c] = MatchingGame.DERANDOMIZER


  # Util api to derandomize cell by column
  def deRandomizeCol(self, col):
    for r in range(self.row):
      self.board[r][col] = MatchingGame.DERANDOMIZER


  def setDebug(self, debug):
    self.isDebug = debug

  def debugMatchingGame(self, msg):
    if self.isDebug:
      print(msg)



# main function
if __name__ == '__main__':
  uip = input("? Computer set up game board: ")
  if uip in ('yes', 'y', 'true', 'sure', 'ok', 'k'):
    uip = input ("? Randomize cells: ")
    if uip in ('no', 'n', 'nope', 'don\'t'):
      game = MatchingGame(MatchingGame.GAME_BOARD_SET_BY_COMPUTER, False)
    else:
      game = MatchingGame(MatchingGame.GAME_BOARD_SET_BY_COMPUTER, True, 'ab')

      # when computer generate Game Board, we will re-set the cell-values
      # game.setCellValues("abc")  (no effect, before init happened first)

  else:
    game = MatchingGame(not MatchingGame.GAME_BOARD_SET_BY_COMPUTER)

  game.playMatchingGame()
