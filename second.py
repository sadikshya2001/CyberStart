import pygame  
import random  
from words import cybersecurity_words  
import os  
import string  
import sys  
from config import Config  

pygame.init()  

# Import the shared config object  
config = Config()  

WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
GREEN = (124,252,0)  
BLACK = (0, 0, 0)    
GRAY = (200, 200, 200)    
GREEN = (0, 255, 0)    
ALICEBLUE = (240, 248, 255)    
CYAN_AZURE = (78, 130, 180)    
HIGHLIGHT_COLOR = (150, 150, 150)    
LIGHT_GREEN = (144, 238, 144)    
RED = (255, 0, 0)    
AMARANTH = (159, 43, 104)  
DARK_GREEN = (0,100,0)  

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Set up the screen   
screen = pygame.display.set_mode((WIDTH , HEIGHT )) 
pygame.display.set_caption("Hangman Game")  

# Set up fonts  
pygame.font.init()  
font = pygame.font.Font(None, 36)  
large_font = pygame.font.Font(None, 72)  

# Set font paths   
font_folder = "Fonts"   
font_path = os.path.join(font_folder, "SixWeekHolidayDEMO-Regular.otf")   
button_font_path = os.path.join(font_folder, "Bakemono-Stereo-Regular-trial.ttf")   
question_font_path = os.path.join(font_folder, "Invisible-ExtraBold.otf")   
option_font_path = os.path.join(font_folder, "Please write me a song.ttf")   
score_font_path = os.path.join(font_folder, "Cute Notes.ttf")   

username_font = pygame.font.Font(None, 20)   
message_font = pygame.font.Font(font_path, 30)   
button_font = pygame.font.Font(button_font_path, 24)   
question_font = pygame.font.Font(question_font_path, 28)   
option_font = pygame.font.Font(option_font_path, 24)   
score_font = pygame.font.Font(score_font_path, 36)  

def draw_text(text, font, color, x, y):  
    text_surface = font.render(text, True, color)  
    screen.blit(text_surface, (x, y))  

lives_visual_dict = {  
    0: """  
___________  
| /        |  
|/        ( )  
|          |  
|         / \\  
|  
""",  
    1: """  
___________  
| /        |  
|/        ( )  
|          |  
|         /  
|  
""",  
    2: """  
___________  
| /        |  
|/        ( )  
|          |  
|  
""",  
    3: """  
___________  
| /        |  
|/        ( )  
|  
""",  
    4: """  
___________  
| /        |  
|/  
|  
""",  
    5: """ 
___________  
| /  
|/  
|  
""",  
    6: """  
|  
|  
|  
""",  
    7: "",  
}  

# Load background image    
background_image = pygame.image.load("Images/background.png")    
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))    

# Load the back button image   
back_button_image = pygame.image.load("Images/back.png")  # Replace with the actual path of your back button image   
back_button_image = pygame.transform.scale(back_button_image, (70, 70))  # Adjust the size of the back button as needed   

# Define button dimensions and positions    
button_width = 200    
button_height = 50    
button_x = (WIDTH - button_width) // 2   
button_y = (HEIGHT - button_height) // 2 

def check_back_button_click():
    mouse_pos = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_pos):
        return True
    return False 

def get_valid_word(words):  
    word = random.choice(cybersecurity_words)  
    while '-' in word or ' ' in word:  
        word = random.choice(words)  
    return word.upper()  

def draw_text(text, font, color, x, y):  
    text_surface = font.render(text, True, color)  
    screen.blit(text_surface, (x, y))  
 
def draw_wrapped_text(text, font, color, size, max_width, max_height): 
    max_width, max_height = WIDTH - 100, HEIGHT - 100  # Adjust as needed 
    text_surface = font.render(text, True, color) 
    text_rect = text_surface.get_rect() 
    if text_rect.width > max_width: 
        # Wrap text if it exceeds the maximum width 
        words = text.split() 
        lines = [] 
        current_line = "" 
        for word in words: 
            test_line = current_line + word + " " 
            test_width, _ = font.size(test_line) 
 
            if test_width <= max_width: 
                current_line = test_line 
            else: 
                lines.append(current_line) 
                current_line = word + " " 
        lines.append(current_line) 
        total_height = len(lines) * font.get_height() 
        y_position = (HEIGHT - total_height) // 2 

        for line in lines: 
            line_surface = font.render(line, True, color) 
            line_rect = line_surface.get_rect(center=(WIDTH // 2, y_position)) 
            screen.blit(line_surface, line_rect) 
            y_position += font.get_height() 
    else: 
        text_rect.center = (WIDTH // 2, HEIGHT // 2) 
        screen.blit(text_surface, text_rect) 

def game_over(word, lives, word_letters):    
    screen.blit(background_image, (0, 0))   
    global back_button_rect  
    back_button_rect = back_button_image.get_rect(topleft=(10, 10))  
    screen.blit(back_button_image, back_button_rect)  

    # Define button dimensions and positions    
    button_width = 200    
    button_height = 50    
    button_x = (WIDTH - button_width) // 2   
    button_y = (HEIGHT - 200) // 2 

    if lives == 0:  
        draw_wrapped_text("You died. The word was -- {} --".format(word), question_font, RED, 30, 250, WIDTH - 100)  
        play_again_text = button_font.render("Sorry!", True, BLACK)
    elif not word_letters:  
        draw_wrapped_text("YAY! You guessed the word -- {} --".format(word), question_font, DARK_GREEN, 30, 250, WIDTH - 100) 
        play_again_text = button_font.render("You did it!", True, BLACK) 
    play_again_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    #play_again_text = button_font.render("Play Again", True, BLACK)   
    play_again_text_rect = play_again_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    pygame.draw.rect(screen, GREEN, play_again_rect)   
    screen.blit(play_again_text, play_again_text_rect)  
    pygame.display.update()   

    running = True  
    while running: 
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                sys.exit()  
            

        if check_back_button_click():
            running = False  

        pygame.display.update()  

def main(config):   
    global back_button_rect  
    global background_image  
    global WIDTH, HEIGHT
    word, hint = random.choice(cybersecurity_words)  
    word = word.upper()  
    word_letters = set(word.upper())  
    alphabet = set(string.ascii_uppercase)  
    used_letters = set()  
    lives = 7  
    back_button_rect = back_button_image.get_rect(topleft=(10, 10))  

    # Retrieve the player's name from the Config object
    player_name = config.get_username()

    clock = pygame.time.Clock()  
    running = True  
    while running:  
        screen.blit(background_image, (0, 0))  

        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False  
            elif event.type == pygame.VIDEORESIZE:  
                # Update window dimensions  
                WIDTH, HEIGHT = event.size  
                # Resize the background image to fit the new window size  
                background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))         
            elif event.type == pygame.KEYDOWN:  
                if event.unicode.upper() in alphabet - used_letters:  
                    user_letter = event.unicode.upper()  
                    used_letters.add(user_letter)  
                    if user_letter in word_letters:  
                        word_letters.remove(user_letter)  
                    else:  
                        lives -= 1 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_back_button_click():
                    running = False
                        
        # Display the current hangman state using ASCII art  
        current_hangman_state = lives_visual_dict[lives]  
        hangman_lines = current_hangman_state.strip().split('\n')  
        word_list = [letter if letter in used_letters else '_' for letter in word]  

        if config.avatar_image_path is not None:
            avatar_image = pygame.image.load(config.avatar_image_path)
            avatar_image = pygame.transform.scale(avatar_image, (90, 90))
            avatar_rect = avatar_image.get_rect(topright=(WIDTH - 20, 20))
            screen.blit(avatar_image, avatar_rect)

            # Display the player's name just below the avatar image
            player_name_text = username_font.render("Player: {}".format(player_name), True, BLACK)
            player_name_rect = player_name_text.get_rect(topright=(WIDTH - 20, avatar_rect.bottom - 10 ))
            screen.blit(player_name_text, player_name_rect)

        screen.blit(back_button_image, back_button_rect) 

        # Calculate positions for each text element based on the screen center 
        lives_text_x = (WIDTH - 540) // 2
        lives_text_y = 150 
        used_letters_x = (WIDTH - 500) // 2
        used_letters_y = 200 
        hangman_x = (WIDTH - 500) // 2 
        hangman_y = 300 
        current_word_x = (WIDTH - 500) // 2  
        current_word_y = 620 
        hint_x = (WIDTH - 400) // 2 
        hint_y = 650 

        # Draw text elements individually with their respective positions 
        draw_text("You have {} lives left".format(lives), score_font, AMARANTH, lives_text_x, lives_text_y)
        draw_text("You have used these letters:\n{}".format(' '.join(used_letters)), message_font, BLACK, used_letters_x, used_letters_y)
        y_position = hangman_y 
        for line in hangman_lines: 
            draw_text(line, large_font, BLACK, hangman_x, y_position) 
            y_position += large_font.get_height() 
        draw_text("Current word: {}".format(' '.join(word_list)), font, BLACK, current_word_x, current_word_y)
        draw_text("HINT: {} ".format(hint), option_font, BLACK, hint_x, hint_y)

        if lives == 0 or not word_letters:  
            game_over(word, lives, word_letters)  

        pygame.display.flip()  
        clock.tick(60)  

    pygame.display.update()  
    
if __name__ == '__main__':  
    main(config)  