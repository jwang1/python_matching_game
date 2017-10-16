"""exit python program from function"""
"""https://stackoverflow.com/questions/73663/terminating-a-python-script"""
from sys import exit

# https://stackoverflow.com/questions/2823316/generate-a-random-letter-in-python
import string
import random
import re

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
  RED = '\033[91m'



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

  USER_CONFIRM = ('y', 'yes', 'Yes', 'YES', 'confirm', 'Confirm', 'CONFIRM')
  USER_CANCEL = ('n', 'no', 'No', 'NO', 'cancel', 'Cancel', 'CANCEL')

  DERANDOMIZER = 'a'

  MATCH_MARKER = '*'

  BOARD_ROW_START = 1

  BOARD_COLUMN_START = 'A'

  DIRECTION_UP = ('u', 'U', 'up', 'Up', 'UP')
  DIRECTION_DOWN = ('d', 'D', 'down', 'Donw', 'DOWN')
  DIRECTION_LEFT = ('l', 'L', 'left', 'Left', 'LEFT')
  DIRECTION_RIGHT = ('r', 'R', 'right', 'Right', 'RIGHT')


  """Initialize data members."""
  def __init__(self, autoGameSetting, randmoizeCells = True, cellVals = string.ascii_lowercase):

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
    # self.setupGame()  # called outside of the __init__, so that we can set the cell-values, isDebug stuff


  # overrides the cell values (useful for testing, small cellVals, can get more matches; otherwise, 26 lowercase
  # letters not easy to get consecutive matches)
  def setCellValues(self, cellVals):
    self.cellValues = cellVals


  """User prompts, set up the board size, and defined consecutive matching"""
  def setupGame(self):
    if not self.autoGameSetting:
      self.promptUser()

    self.initBoard()

    print("__________BEFORE checking consecutive matches_____________\n")
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
      # Mark the consecutive matches
      self.markMatches()
      # Replace the consecutive matches by 1) sinking above cells for each column with marked matches;
      # and 2) randomly generating values for places after being sunk
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
    self.printColumnHeader()

    for r in range(self.row):
      self.printRowDelimitor()

      self.printRowNumber(r)

      for c in range(self.col):
        # print without newline : https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space
        print('|' + self.board[r][c], end="", flush=True)

      print('|')

    self.printRowDelimitor()


  def printRowNumber(self, row):
    # print row number, starts from 1
    print('{} '.format(row + MatchingGame.BOARD_ROW_START), end='', flush=True)


  def printColumnHeader(self):
    # print column letters, starts from A
    print(' '*2, end='', flush=True)
    for c in range(self.col):
      print(' ' + chr(ord(MatchingGame.BOARD_COLUMN_START) + c), end='', flush=True)
    print(' ')


  def printRowDelimitor(self):
    print(' '*2 + '-'*(2 * self.col + 1))


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

        # get the elements that can be sunk
        # notice the order of the elements;  1st row element @ that column is the first element in elements List
        # after the following operation
        elements = []
        for r in range(0, startEndByCol[0]):
          elements.append(self.board[r][c])

        # for sure we need to generate some randomized values; to be exact,
        for i in range(0, startEndByCol[1] - startEndByCol[0] + 1):
          elements.insert(0, random.choice(self.cellValues))

        self.debugMatchingGame("elements {} to replace and fill the column".format(elements))

        # now fill all from elements, into the column starting from startEndByCol[1],
        for i in range(startEndByCol[1] + 1):
          self.board[i][c] = elements[i]

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
        pass

      finally:
        if self.quit:
          exit(MatchingGame.USER_QUITS)


  """Initialize data members."""
  def playMatchingGame(self):
    self.printGuide()

    while True:
      try:
        rip = input(">>>>> Please select a cell to swap with another by using the direction (u, d, l, r): ")

        if rip in self.USER_QUITS:
          self.quit = True


        # move will be '2B u'  (or '2b u')
        (cell, direction) = rip.split(' ')

        # validate
        (r, c, direction) = self.validateMove(cell, direction)

        # move
        # it will have following checkMatches() multiple times until no consecutive matches, and also add up scores
        self.move(int(r), c, direction)

        self.printScore()

      except (Exception, IndexError) as err:
        if self.quit:
          confirm = input("Are your sure to Quit the game?")
          if confirm in MatchingGame.USER_CONFIRM:
            print("{}Your final score is: {}{}".format(MatchingGame.BOLD, self.score, MatchingGame.END))
          elif confirm in MatchingGame.USER_CANCEL:
            # user's is not going to quit game, after being double-checked
            self.quit = False

        else:
          print('{}your input "{}" may be invalid; or some other errors "{}"{}'
                .format(MatchingGame.RED, rip, err, MatchingGame.END))

      finally:
        if self.quit:
          exit(MatchingGame.USER_QUITS)


  def printScore(self):
    print('Your current score is: {}{}{}'.format(MatchingGame.BOLD, self.score, MatchingGame.END))


  """move() method is called after validateMove()"""
  """user's input row starts from 1, and column starts from A"""
  def move(self, row, col, direction):
    row -= MatchingGame.BOARD_ROW_START
    col = ord(col) - ord(MatchingGame.BOARD_COLUMN_START)

    tmp = self.board[row][col]
    if direction in MatchingGame.DIRECTION_UP:
      self.board[row][col] = self.board[row-1][col]
      self.board[row-1][col] = tmp
    elif direction in MatchingGame.DIRECTION_DOWN:
      self.board[row][col] = self.board[row+1][col]
      self.board[row+1][col] = tmp
    elif direction in MatchingGame.DIRECTION_LEFT:
      self.board[row][col] = self.board[row][col-1]
      self.board[row][col-1] = tmp
    elif direction in MatchingGame.DIRECTION_RIGHT:
      self.board[row][col] = self.board[row][col+1]
      self.board[row][col+1] = tmp
    else:
      # will not come here because move() is called after validateMove()
      pass


    while True:
      self.checkMatches()

      if self.matchesInOneRound <= 0:
        break
      else:
        self.debugMatchingGame('{} matches found'.format(self.matchesInOneRound))
        self.score += self.matchesInOneRound

        # now that found conseuctive matches, let's mark them
        self.markMatches()
        # sweep those marked celss by 1) sinking above cells for each column with marked matches;
        # and 2) replace those sunk cells with randomly generated values.
        self.replaceMatchMarker()

        if self.isDebug:
          self.printBoard()


    # at least user made a move (swapped two cells); note that computer may mark/sweep/replace/generate values
    # let's reflect the move on Board
    self.printBoard()



  """return tuple (row, col, direction), or exception"""
  def validateMove(self, cell, direction):

    match = re.match(r"([0-9]+)([a-z]+)", cell, re.I)

    if match == None or len(match.groups()) != 2:
      raise Exception('{} is invalid, input something like 2B (2nd row, 2nd column).'.format(cell))

    (row, col) = match.groups()

    if direction not in MatchingGame.DIRECTION_UP and direction not in MatchingGame.DIRECTION_DOWN \
            and direction not in MatchingGame.DIRECTION_LEFT and direction not in MatchingGame.DIRECTION_RIGHT:
     raise Exception('direction {} is invalid, please input either u, d, l, or r'.format(direction))
    elif direction in MatchingGame.DIRECTION_UP and int(row) <= 1:
      raise IndexError('direction {} is out of bound. Row {} cannot move up.'.format(direction, row))
    elif direction in MatchingGame.DIRECTION_DOWN and int(row) >= self.row:
      raise IndexError('direction {} is out of bound. Row {} cannot move down.'.format(direction, row))
    elif direction in MatchingGame.DIRECTION_LEFT and ord(col.upper()) <= ord(MatchingGame.BOARD_COLUMN_START):
      raise IndexError('direction {} is out of bound. Column {} cannot move left.'.format(direction, row))
    elif direction in MatchingGame.DIRECTION_RIGHT and ord(col.upper()) - ord(MatchingGame.BOARD_COLUMN_START) >= self.col:
      raise IndexError('direction {} is out of bound. Column {} cannot move left.'.format(direction, row))

    return (row, col.upper(), direction)



  def printGuide(self):
    print("***************************************************************************************************")
    print("****** Let's start gaming: (enter q to Quit game)                                            ******")
    print("****** Pick a cell, and give moving direction                                                ******")
    print("****** use row-# and column-letter for Cell, for instance, 2B for cell at 2nd row 2nd column ******")
    print("****** moving directions (u / d / l / r),  u for Up, d for Down, l for Left, and r for Right ******")
    print("***************************************************************************************************")


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
    uip = input("? Randomize cells: ")
    if uip in ('no', 'n', 'nope', 'don\'t'):
      game = MatchingGame(MatchingGame.GAME_BOARD_SET_BY_COMPUTER, False)
    else:
      game = MatchingGame(MatchingGame.GAME_BOARD_SET_BY_COMPUTER, True, 'abc')

      # when computer generate Game Board, we will re-set the cell-values
      # game.setCellValues("abc")  (no effect, before init happened first)

  else:
    uip = input("? using smaller set of letters (say, abcefg): ")
    if uip in MatchingGame.USER_CONFIRM:
      game = MatchingGame(not MatchingGame.GAME_BOARD_SET_BY_COMPUTER, cellVals = 'abcefg')
    else:
      game = MatchingGame(not MatchingGame.GAME_BOARD_SET_BY_COMPUTER, cellVals = string.ascii_lowercase)

  # setting debug mode
  game.setDebug(True)

  game.setupGame()

  game.playMatchingGame()
