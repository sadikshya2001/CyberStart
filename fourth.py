import random 
import pygame 
import sys 
import os 
import pygame.time
from pygame.locals import * 
from config import Config  
pygame.init()

# Import the shared config object  
config = Config()  

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
WINDOWWIDTH, WINDOWHEIGHT = info.current_w, info.current_h
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

FPS = 30 # frames per second, the general speed of the program 
REVEALSPEED = 8 # speed boxes' sliding reveals and covers 
BOXSIZE = 80 # size of box height & width in pixels 
GAPSIZE = 10 # size of gap between boxes in pixels 
BOARDWIDTH = 6 # number of columns of icons 
BOARDHEIGHT = 3 # number of rows of icons 

assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.' 
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2) 
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2) 

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
ALICEBLUE = (240, 248, 255)   
CYAN_AZURE = (78, 130, 180) 
BLACK = (0, 0, 0) 

BGCOLOR = NAVYBLUE 
LIGHTBGCOLOR = GRAY 
BOXCOLOR = BGCOLOR 
HIGHLIGHTCOLOR = WHITE 

DONUT = 'donut' 
SQUARE = 'square' 
DIAMOND = 'diamond' 
LINES = 'lines' 
OVAL = 'oval' 

ICON1 = 0 
ICON2 = 1 
ICON3 = 2 
ICON4 = 3 
ICON5 = 4 
ICON6 = 5 
ICON7 = 6 
ICON8 = 7 
ICON9 = 8 
ICON10 = 9 
ICON11 = 10 
ICON12 = 11 
ICON13 = 12 
ICON14 = 13 
ICON15 = 14 
ICON16 = 15 
ICON17 = 16 

font_folder = "Fonts"   
font_path = os.path.join(font_folder, "SixWeekHolidayDEMO-Regular.otf")   
button_font_path = os.path.join(font_folder, "Bakemono-Stereo-Regular-trial.ttf")   
question_font_path = os.path.join(font_folder, "Invisible-ExtraBold.otf")   
option_font_path = os.path.join(font_folder, "Please write me a song.ttf")   
score_font_path = os.path.join(font_folder, "Cute Notes.ttf")    
  
# Set fonts   
username_font = pygame.font.Font(None, 20)   
message_font = pygame.font.Font(font_path, 36)   
button_font = pygame.font.Font(button_font_path, 24)   
question_font = pygame.font.Font(question_font_path, 28)   
option_font = pygame.font.Font(option_font_path, 24)   
score_font = pygame.font.Font(score_font_path, 36)   

# Load images for each icon 
ICON_IMAGES = [ 
    pygame.image.load("Images/Memory/binary-code.png"), 
    pygame.image.load("Images/Memory/data_4024778.png"), 
    pygame.image.load("Images/Memory/desktop_954736.png"), 
    pygame.image.load("Images/Memory/hacked.png"), 
    pygame.image.load("Images/Memory/hacker (1).png"), 
    pygame.image.load("Images/Memory/hacking.png"), 
    pygame.image.load("Images/Memory/insurance-protected-icon.png"), 
    pygame.image.load("Images/Memory/malware-virus-icon.png"), 
    pygame.image.load("Images/Memory/safety-icon.png"), 
    pygame.image.load("Images/Memory/self-employed.png"), 
    pygame.image.load("Images/Memory/shield-checkmark-black-icon.png"), 
    pygame.image.load("Images/Memory/shield-icon.png"), 
    pygame.image.load("Images/Memory/spy.png"), 
    pygame.image.load("Images/Memory/spyware.png"), 
    pygame.image.load("Images/Memory/virus (1).png"), 
    pygame.image.load("Images/Memory/virus_564643.png"), 
    pygame.image.load("Images/Memory/virus.png") 
    #pygame.image.load(""), 
] 

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN) 
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL) 
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined." 

# Load background image   
background_image = pygame.image.load("Images/background.png")   
background_image = pygame.transform.scale(background_image, (WINDOWWIDTH, WINDOWHEIGHT))   

# Load the back button image  
back_button_image = pygame.image.load("Images/back.png")  # Replace with the actual path of your back button image  
back_button_image = pygame.transform.scale(back_button_image, (70, 70))  # Adjust the size of the back button as needed  

# Define button dimensions and positions   
button_width = 200   
button_height = 50   
button_x = WINDOWWIDTH // 2 - button_width // 2   
button_y = WINDOWHEIGHT // 2 - 40  
start_time = pygame.time.get_ticks()

# Function to detect when the player clicks on the back button  
def check_back_button_click():
    mouse_pos = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_pos):
        return True
    return False  

def updateGameBoardPosition():
    global XMARGIN, YMARGIN
    # Calculate the new X and Y margins based on the current window dimensions
    XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
    YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

def game_over(elapsed_time, start_time):   
    DISPLAYSURF.blit(background_image, (0, 0))  
    global back_button_rect 
    back_button_rect = back_button_image.get_rect(topleft=(10, 10)) 
    DISPLAYSURF.blit(back_button_image, back_button_rect) 
    current_time = pygame.time.get_ticks()  # Get current time
    elapsed_time = current_time - start_time  # Calculate elapsed time

    time_text = f"You did it! You took {elapsed_time // 60000} minutes and {(elapsed_time % 60000) // 1000} seconds."
    time_surface = question_font.render(time_text, True, BLACK)
    time_rect = time_surface.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 60))  # Adjust the position as needed
    DISPLAYSURF.blit(time_surface, time_rect)

    play_again_rect = pygame.Rect(button_x, button_y, button_width, button_height)  
    play_again_text = button_font.render("Play Again", True, BLACK)  
    play_again_text_rect = play_again_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))  
    pygame.draw.rect(DISPLAYSURF, GREEN, play_again_rect)  
    DISPLAYSURF.blit(play_again_text, play_again_text_rect)  

    running = True 
    while running: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                sys.exit() 
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_pos = pygame.mouse.get_pos() 
                if play_again_rect.collidepoint(mouse_pos): 
                    main(config)   
        if check_back_button_click():   
            running = False  

        if config.avatar_image_path is not None:  
            avatar_image = pygame.image.load(config.avatar_image_path)  
            avatar_image = pygame.transform.scale(avatar_image, (90, 90))  
            avatar_rect = avatar_image.get_rect(topright=(WINDOWWIDTH - 20, 20))  
            DISPLAYSURF.blit(avatar_image, avatar_rect) 

            # Display the player's name just below the avatar image
            player_name = config.get_username()
            player_name_text = username_font.render("Player: {}".format(player_name), True, BLACK)
            player_name_rect = player_name_text.get_rect(topright=(WINDOWWIDTH - 20, avatar_rect.bottom - 10 ))
            DISPLAYSURF.blit(player_name_text, player_name_rect)  
        pygame.display.update() 

def main(config): 
    global FPSCLOCK, DISPLAYSURF, background_image 
    global WINDOWWIDTH, WINDOWHEIGHT 
    pygame.init() 
    FPSCLOCK = pygame.time.Clock() 
    start_time = pygame.time.get_ticks()
 
    #DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) 
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) 
    background_image = pygame.image.load("Images/background.png") 
    background_image = pygame.transform.scale(background_image, (WINDOWWIDTH, WINDOWHEIGHT)) 

    mousex = 0 # used to store x coordinate of mouse event 
    mousey = 0 # used to store y coordinate of mouse event 
    pygame.display.set_caption('Memory Game') 
    mainBoard = getRandomizedBoard() 
    revealedBoxes = generateRevealedBoxesData(False) 

    firstSelection = None # stores the (x, y) of the first box clicked. 
    DISPLAYSURF.blit(background_image, (0, 0)) 

    # Retrieve the player's name from the Config object
    player_name = config.get_username()

    startGameAnimation(mainBoard) 

    running = True 
    while running: # main game loop 
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        elapsed_seconds = elapsed_time // 1000  # Convert to seconds
        elapsed_minutes = elapsed_seconds // 60   # Convert to minutes
        elapsed_seconds %= 60  # Get the remaining seconds

        mouseClicked = False 
        DISPLAYSURF.blit(background_image, (0, 0)) 

        drawBoard(mainBoard, revealedBoxes) 
        time_text = f"Time: {elapsed_minutes} minutes {elapsed_seconds} seconds"
        time_surface = question_font.render(time_text, True, BLACK)
        time_rect = time_surface.get_rect()
        time_rect.midtop = (WINDOWWIDTH // 2, YMARGIN + BOARDHEIGHT * (BOXSIZE + GAPSIZE) + 10)
        DISPLAYSURF.blit(time_surface, time_rect)

        global back_button_rect  # Add back_button_rect to the global scope  
        back_button_rect = back_button_image.get_rect(topleft=(10, 10)) 
        DISPLAYSURF.blit(back_button_image, (10, 10)) 

        if config.avatar_image_path is not None:  
            avatar_image = pygame.image.load(config.avatar_image_path)  
            avatar_image = pygame.transform.scale(avatar_image, (90, 90))  
            avatar_rect = avatar_image.get_rect(topright=(WINDOWWIDTH - 20, 20))  
            DISPLAYSURF.blit(avatar_image, avatar_rect) 

            # Display the player's name just below the avatar image
            player_name = config.get_username()
            player_name_text = username_font.render("Player: {}".format(player_name), True, BLACK)
            player_name_rect = player_name_text.get_rect(topright=(WINDOWWIDTH - 20, avatar_rect.bottom - 10 ))
            DISPLAYSURF.blit(player_name_text, player_name_rect)    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                # Update window dimensions
                WINDOWWIDTH, WINDOWHEIGHT = event.size
                # Resize the background image to fit the new window size
                background_image = pygame.transform.scale(background_image, (WINDOWWIDTH, WINDOWHEIGHT))
                # Update the game board position
                updateGameBoardPosition()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_back_button_click():
                    running = False
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
                    icon1 = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1]) 
                    icon2 = getShapeAndColor(mainBoard, boxx, boxy) 
                    if icon1 != icon2: 
                        # Icons don't match. Re-cover up both selections. 
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec 
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)]) 
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False 
                        revealedBoxes[boxx][boxy] = False 

                    elif hasWon(revealedBoxes): # check if all pairs found 
                        # In the main() function, before the game_over() function call
                        current_time = pygame.time.get_ticks()
                        elapsed_time = current_time - start_time
                        game_over(elapsed_time, start_time) 
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
    # Get a list of every possible icon index. 
    icons = [ICON1, ICON2, ICON3, ICON4, ICON5, ICON6, ICON7, ICON8, ICON9, ICON10, ICON11, ICON12, ICON13, ICON14, ICON15, ICON16, ICON17]# Add more icon indices as needed 
    # Add more icon indices to fill the board if needed 
    random.shuffle(icons)  # Randomize the order of the icons list 
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)  # Calculate how many icons are needed 
    icons = icons[:numIconsUsed] * 2  # Make two of each 
    random.shuffle(icons) 

    # Create the board data structure, with randomly placed icons. 
    board = [] 
    for x in range(BOARDWIDTH): 
        column = [] 
        for y in range(BOARDHEIGHT): 
            column.append(icons[0]) 
            del icons[0]  # Remove the icons as we assign them 
        board.append(column) 
    return board 

def splitIntoGroupsOf(groupSize, theList): 
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

def drawIcon(icon_index, boxx, boxy): 
    left, top = leftTopCoordsOfBox(boxx, boxy) 
    # Load and draw the corresponding image based on the icon index 
    if icon_index == ICON1: 
        image = pygame.image.load("Images/Memory/binary-code.png") 
    elif icon_index == ICON2: 
        image = pygame.image.load("Images/Memory/data_4024778.png") 
    elif icon_index == ICON3: 
        image = pygame.image.load("Images/Memory/desktop_954736.png") 
    elif icon_index == ICON4: 
        image = pygame.image.load("Images/Memory/hacked.png") 
    elif icon_index == ICON5: 
        image = pygame.image.load("Images/Memory/hacker (1).png") 
    elif icon_index == ICON6: 
        image = pygame.image.load("Images/Memory/hacking.png") 
    elif icon_index == ICON7: 
        image = pygame.image.load("Images/Memory/insurance-protected-icon.png") 
    elif icon_index == ICON8: 
        image = pygame.image.load("Images/Memory/malware-virus-icon.png") 
    elif icon_index == ICON9: 
        image = pygame.image.load("Images/Memory/safety-icon.png") 
    elif icon_index == ICON10: 
        image = pygame.image.load("Images/Memory/self-employed.png") 
    elif icon_index == ICON11: 
        image = pygame.image.load("Images/Memory/shield-checkmark-black-icon.png") 
    elif icon_index == ICON12: 
        image = pygame.image.load("Images/Memory/shield-icon.png") 
    elif icon_index == ICON13: 
        image = pygame.image.load("Images/Memory/spy.png") 
    elif icon_index == ICON14: 
        image = pygame.image.load("Images/Memory/spyware.png") 
    elif icon_index == ICON15: 
        image = pygame.image.load("Images/Memory/virus (1).png") 
    elif icon_index == ICON16: 
        image = pygame.image.load("Images/Memory/virus_564643.png") 
    elif icon_index == ICON17: 
        image = pygame.image.load("Images/Memory/virus.png") 

    # Resize the image to fit the box size 
    image = pygame.transform.scale(image, (BOXSIZE, BOXSIZE)) 
    DISPLAYSURF.blit(image, (left, top)) 

def getShapeAndColor(board, boxx, boxy): 
    return board[boxx][boxy] 

def drawBoxCovers(board, boxes, coverage): 
    for box in boxes: 
        left, top = leftTopCoordsOfBox(box[0], box[1]) 
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE)) 
        icon_index = getShapeAndColor(board, box[0], box[1])  # Get the icon index 
        drawIcon(icon_index, box[0], box[1])  # Draw the corresponding image 
        if coverage > 0: 
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
    for boxx in range(BOARDWIDTH): 
        for boxy in range(BOARDHEIGHT): 
            left, top = leftTopCoordsOfBox(boxx, boxy) 
            if not revealed[boxx][boxy]: 
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE)) 
            else: 
                icon_index = getShapeAndColor(board, boxx, boxy)  # Get the icon index 
                drawIcon(icon_index, boxx, boxy)  # Draw the corresponding image 

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

def hasWon(revealedBoxes): 
    # Returns True if all the boxes have been revealed, otherwise False 
    for i in revealedBoxes: 
        if False in i: 
            return False # return False if any boxes are covered. 
    return True 

if __name__ == '__main__': 

    main(config) 

 