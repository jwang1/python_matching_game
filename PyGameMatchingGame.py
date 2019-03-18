import pygame, random, sys
from pygame.locals import *

class MatchingPyGame:

  FPS = 30
  WINDOW_WIDTH = 640
  WINDOW_HEIGHT = 480

  REVEAL_SPEED = 8
  BOX_SIZE = 40
  GAP_SIZE = 10

  #BOARD_WIDTH = 10  # nbr of columns of icons
  #BOARD_HEIGHT = 7  # nbr of rows of icons
  BOARD_WIDTH = 4  # nbr of columns of icons
  BOARD_HEIGHT = 3  # nbr of rows of icons

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
  def __init__(self, pygame):

    self.pygame = pygame

    self.pygame.init()
    self.fpsClock = self.pygame.time.Clock()
    self.displaySurf = self.pygame.display.set_mode((MatchingPyGame.WINDOW_WIDTH, MatchingPyGame.WINDOW_HEIGHT))

    self.mouseX = 0
    self.mouseY = 0
    
    self.getRandomizedBoard()

    self.generateRevealedBoxesData(False)

    # stores (x, y) of the first box clicked
    self.firstSelection = None

    self.displaySurf.fill(MatchingPyGame.BG_COLOR)

    self.makeAnimation()

    self.play()

    # as no-op (nice to use for empty function definition
    pass


  """Start the game"""
  def play(self):
    while True:  # main game loop
      mouseClicked = False
      mousex = mousey = 0  # otherwise getBoxAtPixel will complain referred before assignment

      self.displaySurf.fill(MatchingPyGame.BG_COLOR)  # drawing the window
      self.pygame.time.wait(300)
      self.drawBoard()

      for event in pygame.event.get():  # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
          pygame.quit()
          sys.exit()
        elif event.type == MOUSEMOTION:
          mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
          mousex, mousey = event.pos
          mouseClicked = True

      boxx, boxy = self.getBoxAtPixel(mousex, mousey)
      if boxx != None and boxy != None:
        # The mouse is currently over a box.
        if not self.revealedBoxes[boxx][boxy]:
          self.drawHighlightBox(boxx, boxy)

        if not self.revealedBoxes[boxx][boxy] and mouseClicked:
          self.revealedBoxes[boxx][boxy] = True  # set the box as "revealed"
          self.revealBoxesAnimation([(boxx, boxy)])

          if self.firstSelection == None:  # the current box was the first box clicked
            self.firstSelection = (boxx, boxy)

          else:  # the current box was the second box clicked
            # Check if there is a match between the two icons.
            icon1shape, icon1color = self.getShapeAndColor(self.firstSelection[0], self.firstSelection[1])
            icon2shape, icon2color = self.getShapeAndColor(boxx, boxy)

            if icon1shape != icon2shape or icon1color != icon2color:
              # Icons don't match. Re-cover up both selections.
              #pygame.time.wait(1000)  # 1000 milliseconds = 1 sec
              #self.coverBoxesAnimation([(self.firstSelection[0], self.firstSelection[1]), (boxx, boxy)])

              # need to flip the two-not-matched cards
              self.revealedBoxes[self.firstSelection[0]][self.firstSelection[1]] = False
              self.revealedBoxes[boxx][boxy] = False

            elif self.hasWon():  # check if all pairs found
              self.gameWonAnimation()
              pygame.time.wait(2000)

              # Reset the board
              self.getRandomizedBoard()
              self.generateRevealedBoxesData(False)

              # Show the fully unrevealed board for a second.
              self.drawBoard()
              pygame.display.update()
              pygame.time.wait(1000)

              # Replay the start game animation.
              #self.startGameAnimation()

            self.firstSelection = None  # reset firstSelection variable

      # Redraw the screen and wait a clock tick.
      self.pygame.display.update()
      self.fpsClock.tick(MatchingPyGame.FPS)



  """revealed boxes on game board"""
  def generateRevealedBoxesData(self, revealed):
    self.revealedBoxes = []
    for i in range(MatchingPyGame.BOARD_WIDTH):
      self.revealedBoxes.append([revealed] * MatchingPyGame.BOARD_HEIGHT)


  """Define the game board"""
  def getRandomizedBoard(self):
    self.icons = []

    for color in MatchingPyGame.ALL_COLORS:
      for shape in MatchingPyGame.ALL_SHAPES:
        self.icons.append((shape, color))

    random.shuffle(self.icons)

    numIconsUsed = int(MatchingPyGame.BOARD_WIDTH * MatchingPyGame.BOARD_HEIGHT / 2)
    # make two of each icon
    self.icons = self.icons[:numIconsUsed] * 2

    random.shuffle(self.icons)

    self.mainBoard = []
    for x in range(MatchingPyGame.BOARD_WIDTH):
      column = []
      for y in range(MatchingPyGame.BOARD_HEIGHT):
        # using the icon one at a time, and remove it from the self.icons
        column.append(self.icons[0])
        del self.icons[0]

      self.mainBoard.append(column)


  """Gmae animation"""
  def makeAnimation(self):
    self.generateRevealedBoxesData(False)
    boxes = []
    for x in range(MatchingPyGame.BOARD_WIDTH):
        for y in range(MatchingPyGame.BOARD_HEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    #boxGroups = splitIntoGroupsOf(8, boxes)
    boxGroups = self.splitIntoGroupsOf(MatchingPyGame.BOARD_WIDTH, boxes)

    self.drawBoard()
    for boxGroup in boxGroups:
        self.revealBoxesAnimation(boxGroup)
        self.coverBoxesAnimation(boxGroup)


  def drawBoard(self):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(MatchingPyGame.BOARD_WIDTH):
        for boxy in range(MatchingPyGame.BOARD_HEIGHT):
            left, top = self.leftTopCoordsOfBox(boxx, boxy)
            if not self.revealedBoxes[boxx][boxy]:
                # Draw a covered box.
                self.pygame.draw.rect(self.displaySurf, MatchingPyGame.BOX_COLOR,
                                      (left, top, MatchingPyGame.BOX_SIZE, MatchingPyGame.BOX_SIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = self.getShapeAndColor(boxx, boxy)
                self.drawIcon(shape, color, boxx, boxy)


  def leftTopCoordsOfBox(self, boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (MatchingPyGame.BOX_SIZE + MatchingPyGame.GAP_SIZE) + MatchingPyGame.X_MARGIN
    top = boxy * (MatchingPyGame.BOX_SIZE + MatchingPyGame.GAP_SIZE) + MatchingPyGame.Y_MARGIN
    return (left, top)


  def getShapeAndColor(self, boxx, boxy):
    return self.mainBoard[boxx][boxy][0], self.mainBoard[boxx][boxy][1]

  def drawIcon(self, shape, color, boxx, boxy):
    quarter = int(MatchingPyGame.BOX_SIZE * 0.25) # syntactic sugar
    half =    int(MatchingPyGame.BOX_SIZE * 0.5)  # syntactic sugar

    left, top = self.leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == MatchingPyGame.DONUT:
        pygame.draw.circle(self.displaySurf, color, (left + half, top + half), half - 5)
        pygame.draw.circle(self.displaySurf, MatchingPyGame.BG_COLOR, (left + half, top + half), quarter - 5)
    elif shape == MatchingPyGame.SQUARE:
        pygame.draw.rect(self.displaySurf, color,
                         (left + quarter, top + quarter, MatchingPyGame.BOX_SIZE - half, MatchingPyGame.BOX_SIZE - half))
    elif shape == MatchingPyGame.DIAMOND:
        pygame.draw.polygon(self.displaySurf, color,
                            ((left + half, top),
                             (left + MatchingPyGame.BOX_SIZE - 1, top + half),
                             (left + half, top + MatchingPyGame.BOX_SIZE - 1), (left, top + half)))

    elif shape == MatchingPyGame.LINES:
        for i in range(0, MatchingPyGame.BOX_SIZE, 4):
            pygame.draw.line(self.displaySurf, color, (left, top + i), (left + i, top))
            pygame.draw.line(self.displaySurf, color, (left + i, top + MatchingPyGame.BOX_SIZE - 1),
                             (left + MatchingPyGame.BOX_SIZE - 1, top + i))
    elif shape == MatchingPyGame.OVAL:
        pygame.draw.ellipse(self.displaySurf, color, (left, top + quarter, MatchingPyGame.BOX_SIZE, half))


  def getBoxAtPixel(self, x, y):
    for boxx in range(MatchingPyGame.BOARD_WIDTH):
        for boxy in range(MatchingPyGame.BOARD_HEIGHT):
            left, top = self.leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, MatchingPyGame.BOX_SIZE, MatchingPyGame.BOX_SIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

  def drawHighlightBox(self, boxx, boxy):
    left, top = self.leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(self.displaySurf, MatchingPyGame.HIGHLIGHT_COLOR,
                     (left - 5, top - 5, MatchingPyGame.BOX_SIZE + 10, MatchingPyGame.BOX_SIZE + 10), 4)

  def revealBoxesAnimation(self, boxes):
    self.drawBoxCovers(boxes, -1)

    #for coverage in range(MatchingPyGame.BOX_SIZE, (-MatchingPyGame.REVEAL_SPEED) - 1, -MatchingPyGame.REVEAL_SPEED):
    #    self.drawBoxCovers(boxes, coverage)

  def gameWonAnimation(self):
    # flash the background color when the player has won
    self.generateRevealedBoxesData(True)
    color1 = MatchingPyGame.LIGHT_BG_COLOR
    color2 = MatchingPyGame.BG_COLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        self.displaySurf.fill(color1)
        self.drawBoard()
        pygame.display.update()
        pygame.time.wait(300)

  def drawBoxCovers(self, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = self.leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(self.displaySurf, MatchingPyGame.BG_COLOR,
                         (left, top, MatchingPyGame.BOX_SIZE, MatchingPyGame.BOX_SIZE))
        shape, color = self.getShapeAndColor(box[0], box[1])
        self.drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(self.displaySurf, MatchingPyGame.BOX_COLOR,
                             (left, top, coverage, MatchingPyGame.BOX_SIZE))
    pygame.display.update()
    self.fpsClock.tick(MatchingPyGame.FPS)

  def coverBoxesAnimation(self, boxes):
    self.drawBoxCovers(boxes, MatchingPyGame.BOX_SIZE)

    # Do the "box cover" animation.
    #for coverage in range(0, MatchingPyGame.BOX_SIZE + MatchingPyGame.REVEAL_SPEED, MatchingPyGame.REVEAL_SPEED):
    #    self.drawBoxCovers(boxes, coverage)

  def hasWon(self):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in self.revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True

  def startGameAnimation(self):
    # Randomly reveal the boxes 8 at a time.
    self.generateRevealedBoxesData(False)
    boxes = []
    for x in range(MatchingPyGame.BOARD_WIDTH):
        for y in range(MatchingPyGame.BOARD_HEIGHT):
            boxes.append( (x, y))
    random.shuffle(boxes)
    boxGroups = self.splitIntoGroupsOf(8, boxes)

    self.drawBoard()
    for boxGroup in boxGroups:
        self.revealBoxesAnimation(boxGroup)
        self.coverBoxesAnimation(boxGroup)

  def splitIntoGroupsOf(self, groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


# main function
if __name__ == '__main__':

  global pygame

  game = MatchingPyGame(pygame)

  game.play()
