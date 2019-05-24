

import random, pygame, sys
from pygame.locals import *
FPS = 30 # khung hình mỗi giây, tốc độ chung của chương trình
WINDOWWIDTH = 640 # Kích thước chiều rộng của cửa sổ tính bằng pixel
WINDOWHEIGHT = 480 # Kích thước chiều cao của của sổ tính bằng pixel
REVEALSPEED = 8 # tốc độ hiển thị của từng ô và nắp trượt của khung
BOXSIZE = 40 # Kích thước của hộp( chiều cao và rộng tính bằng pixel)
GAPSIZE = 10 # Kích thước khoảng cách giữa các hộp tính theo pixel
BOARDWIDTH = 10 # Số lượng cột các biểu tượng icon
BOARDHEIGHT = 7 # Số hàng của các biểu tượng icon
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Yêu cầu số lượng hộp là chẵn cho các cặp icons'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100) # màu xám
NAVYBLUE = ( 60,  60, 100) # màu xanh hải quân
WHITE    = (255, 255, 255) # màu trắng
RED      = (255,   0,   0) # màu đỏ
GREEN    = (  0, 255,   0) # màu xanh lá cây
BLUE     = (  0,   0, 255) # màu xanh trời
YELLOW   = (255, 255,   0) # màu vàng
ORANGE   = (255, 128,   0) # màu cam
PURPLE   = (255,   0, 255) # màu tím
CYAN     = (  0, 255, 255) # màu lục lam

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
# hàm assert được sử dụng để đánh giá biểu thức và phát hiện lỗi logic bằng bieuer thức đầu vào
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()# tạo 1 đối tượng theo dõi thời gian pygame.Clock.
    # chúng tôi sẽ sử dụng phương thức tick() của đối tượng để đảm bảo rằng chowng trình chạy với tốc độ
    # không quá 30 khung hình mỗi giây( trong hằng số FPS)
    #pygame.display.set_mode: khởi tạo 1 cửa sổ màn hình để hiển thị
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) 
#"pygame.init(): cần được gọi trước bất kì hàm Pygame nào khác"
    #"mousex và mousey: sẽ lưu trữ tọa độ mới nhất của con trỏ chuột"
    mousex = 0 # used to store x coordinate of mouse event( được sử dụng để lưu trữ tọa độ x của sự kiện chuột)
    mousey = 0 # used to store y coordinate of mouse event( được sử dụng để lưu trữ tọa độ y của sự kiện chuột)
    #pygame.display.set_caption(Đặt chú thích cửa sổ hiện  tại)
    pygame.display.set_caption('Memory Game')
#mainBoard: chứa cấu trúc dữ liệu bảng biểu tượng trong mỗi hộp.
    mainBoard = getRandomizedBoard()# sẽ trả về 1 bảng với số ngẫu nhiên chọn Icons, đó là cách trò chơi bắt đầu 
    #revealedBoxes: nơi lưu trữ các cặp khớp mà người chơi đã tìm thấy
    #generateRevealedBoxesData: Trả về 1 ds các ds, với một gá trị( sai trong trường hợp trên)
#Hai biến này theo dõi bước đó là gì. Khi người dùng nhấp vào hộp lần đầu tiên, chúng tôi sẽ thay đổi
    # thì revealedBoxes đổi trạng thái từ True thành false và lưu hộp nào được nhấp vào FirstSelection. Lần tiếp theo người chơi nhấp vào hộp,
    #revealedBoxed sẽ là Sai (đó là cách chúng tôi biết đây là bước thứ hai của người chơi)
    #và chúng tôi có thể xem liệu hộp mà người chơi vừa nhấp vào có khớp với cái trong FirstSelection không.

#    Sau đó, chúng tôi đặt lại đầu tiên, quay lại True để lần sau khi người chơi nhấp vào hộp, nó được xem là bước đầu tiên của quy trình hai bước. "" "
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.
#Khi bắt đầu trò chơi, chức năng lướt qua nội dung của bảng chỉ để cho người chơi xem lén mọi thứ
    # startGameAnimation() sẽ làm việc này
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)
# vòng lặp trò chơi chính( đây là vòng lặp chơi chính,
# liên tục lặp trong khi chương trình đang phát. Trong vòng lặp này
# hiển thị bảng trên màn hình và cũng xử lý bất kỳ sự kiện đầu vào từ người chơi.
# mỗi lần click vào sẽ lưu trữ xem người chơi có chọn hay ko( lưu trong mousex, mousey)
# Và nó sẽ được đặt giá trị là False mỗi lần vòng chơi được lặp lại

    while True:# trong khi đúng
        mouseClicked = False # nhấp vào sai

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): # event handling loop, pygame.event.get() trả về 1 danh sách các đối tượng
            
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes): # check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation.
                        startGameAnimation(mainBoard)
                    firstSelection = None # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True


if __name__ == '__main__':
    main()
