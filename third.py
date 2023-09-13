import pygame  
import string  
import os  
from config import Config  

# Pygame initialization  
pygame.init()  

# Constants   
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
GREEN = (0, 255, 0)  
PURPLE = (128, 0, 128)  
RED = (255, 0, 0)  
FONT_SIZE = 30 
CURSOR_BLINK_TIME_MS = 500  # Cursor blink time in milliseconds  

# Import the shared config object  
config = Config()  

# Password requirements  
MIN_LENGTH = 8  
MIN_UPPERCASE = 1  
MIN_LOWERCASE = 1  
MIN_DIGITS = 1  
MIN_SPECIAL_CHARS = 1  
SPECIAL_CHARS = string.punctuation  

# Set font paths  
font_folder = "Fonts"  
font_path = os.path.join(font_folder, "SixWeekHolidayDEMO-Regular.otf")  
button_font_path = os.path.join(font_folder, "Bakemono-Stereo-Regular-trial.ttf")  
question_font_path = os.path.join(font_folder, "Invisible-ExtraBold.otf")  
option_font_path = os.path.join(font_folder, "Please write me a song.ttf")  
score_font_path = os.path.join(font_folder, "Cute Notes.ttf")  

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h  
screen = pygame.display.set_mode((WIDTH , HEIGHT )) 

pygame.display.set_caption("Password Power-Up")  

# Set up fonts  
pygame.font.init()  
username_font = pygame.font.Font(None, 20)   
font = pygame.font.Font(font_path, FONT_SIZE)  
button_font = pygame.font.Font(button_font_path, FONT_SIZE)  
question_font = pygame.font.Font(question_font_path, FONT_SIZE)  
option_font = pygame.font.Font(option_font_path, FONT_SIZE,)  
score_font = pygame.font.Font(score_font_path, FONT_SIZE) 

# Calculate the center position for the main content
center_x = WIDTH // 2
center_y = HEIGHT // 2

# Function to display text on the screen  
def display_text(text, font, color, y_offset=0):  
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (center_x, center_y + y_offset)
    screen.blit(text_surface, text_rect) 

# Function to check the password strength  
def check_password_strength(password):  
    score = 0  
    # Length check  
    if len(password) >= MIN_LENGTH:  
        score += 1  
    # Uppercase check  
    if any(char.isupper() for char in password):  
        score += 1  
    # Lowercase check  
    if any(char.islower() for char in password):  
        score += 1  

    # Digit check  
    if any(char.isdigit() for char in password):  
        score += 1  
   # Special character check  
    if any(char in SPECIAL_CHARS for char in password):  
        score += 1  
    return score  
  
#cursor visibility   
cursor_visible = True   
clock = pygame.time.Clock()   

# Load background image   
background_image = pygame.image.load("Images/background.png")   
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))   

# Load the back button image  

back_button_image = pygame.image.load("Images/back.png")  # Replace with the actual path of your back button image  
back_button_image = pygame.transform.scale(back_button_image, (70, 70))  # Adjust the size of the back button as needed  

# Function to detect when the player clicks on the back button  

def check_back_button_click():
    mouse_pos = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_pos):
        return True
    return False

INPUT_BOX_WIDTH = 300
INPUT_BOX_HEIGHT = 40
input_box_x = (WIDTH - INPUT_BOX_WIDTH) // 2
input_box_y = (HEIGHT - INPUT_BOX_HEIGHT) // 2

# Main game loop  
def main(config):
    global background_image
    global WIDTH, HEIGHT
    global back_button_rect

    password_input = ""
    cursor_blink_timer = 0
    cursor_show = True
    back_button_rect = back_button_image.get_rect(topleft=(10, 10))

    # Retrieve the player's name from the Config object
    player_name = config.get_username()

    running = True
    while running:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:  # Handle key presses
                if event.key == pygame.K_BACKSPACE:
                    # Handle backspace key press
                    password_input = password_input[:-1]
                elif event.key == pygame.K_RETURN:
                    # Handle Enter key press (you can add your own logic here)
                    print("Entered password:", password_input)
                else:
                    # Handle other key presses (append to the password)
                    password_input += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_back_button_click():
                    running = False

        if config.avatar_image_path is not None:
            avatar_image = pygame.image.load(config.avatar_image_path)
            avatar_image = pygame.transform.scale(avatar_image, (90, 90))
            avatar_rect = avatar_image.get_rect(topright=(WIDTH - 10, 20))
            screen.blit(avatar_image, avatar_rect)

            # Display the player's name just below the avatar image
            player_name_text = username_font.render("Player: {}".format(player_name), True, BLACK)
            player_name_rect = player_name_text.get_rect(topright=(WIDTH - 10, avatar_rect.bottom - 10 ))
            screen.blit(player_name_text, player_name_rect)


        # Draw the back button
        screen.blit(back_button_image, (10, 10))

        password_text_y = center_y - 50

        # Update the positions of the input box and other elements
        input_box_x = center_x - (INPUT_BOX_WIDTH // 2)
        input_box_y = password_text_y - 70

        # Draw a rectangle around the input box
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT), 2)

        # Check the password strength
        score = check_password_strength(password_input)

        display_text("Your Password:", question_font, BLACK, - 150 )

        # Display the password inside the input box
        password_text = option_font.render(password_input, True, BLACK)
        password_text_rect = password_text.get_rect(topleft=(input_box_x + 5, input_box_y + 5))
        screen.blit(password_text, password_text_rect)

        strength_text = "Password Strength: "

        if score == 0:
            strength_text += "Very Weak"
        elif score == 1:
            strength_text += "Weak"
        elif score == 2:
            strength_text += "Moderate"
        elif score == 3:
            strength_text += "Strong"
        elif score == 4 or score > 4:
            strength_text += "Very Strong"

        color = PURPLE if score >= 3 else RED

        display_text(strength_text, score_font, color, -200 )

        # Display password requirements
        display_text("Password Requirements", question_font, BLACK, -50)

        # Minimum character count check
        if len(password_input) >= MIN_LENGTH:
            display_text(f"- Minimum {MIN_LENGTH} characters", option_font, PURPLE, 0 )
        else:
            display_text(f"- Minimum {MIN_LENGTH} characters", option_font, RED, 0)

        # Minimum uppercase letter check
        if sum(1 for char in password_input if char.isupper()) >= MIN_UPPERCASE:
            display_text(f"- Minimum {MIN_UPPERCASE} uppercase letter", option_font, PURPLE, 50)
        else:
            display_text(f"- Minimum {MIN_UPPERCASE} uppercase letter", option_font, RED, 50)

        # Minimum lowercase letter check
        if sum(1 for char in password_input if char.islower()) >= MIN_LOWERCASE:
            display_text(f"- Minimum {MIN_LOWERCASE} lowercase letter", option_font, PURPLE, 100)
        else:
            display_text(f"- Minimum {MIN_LOWERCASE} lowercase letter", option_font, RED, 100)

        # Minimum digit check
        if sum(1 for char in password_input if char.isdigit()) >= MIN_DIGITS:
            display_text(f"- Minimum {MIN_DIGITS} lowercase letter", option_font, PURPLE, 150)
        else:
            display_text(f"- Minimum {MIN_DIGITS} digit", option_font, RED, 150)

        # Minimum special character check
        if sum(1 for char in password_input if char in SPECIAL_CHARS) >= MIN_SPECIAL_CHARS:
            display_text(f"- Minimum {MIN_SPECIAL_CHARS} special character", option_font, PURPLE, 200)
        else:
            display_text(f"- Minimum {MIN_SPECIAL_CHARS} special character", option_font, RED, 200)

        # Blinking cursor
        cursor_blink_timer += pygame.time.get_ticks()

        if cursor_blink_timer >= CURSOR_BLINK_TIME_MS:
            cursor_blink_timer = 0
            cursor_show = not cursor_show

        pygame.display.flip()
        clock.tick(5)  # Adjust the blinking speed as needed
    pygame.display.update()

if __name__ == "__main__":
    main(config)


 
 
 

 