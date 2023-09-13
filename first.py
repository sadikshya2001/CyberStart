import pygame
import sys
import random
import textwrap
import os
from pygame.locals import *
from config import Config

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
ALICEBLUE = (240, 248, 255)
CYAN_AZURE = (78, 130, 180)
HIGHLIGHT_COLOR = (150, 150, 150)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)

# Set the path to your sound files
sound_folder = "Sounds"

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
window_width, window_height = info.current_w, info.current_h
window = pygame.display.set_mode((window_width, window_height)) 

pygame.display.set_caption("Quiz Game")

# Import the shared config object
config = Config()

# Load the back button image
back_button_image = pygame.image.load("Images/back.png")
back_button_image = pygame.transform.scale(back_button_image, (70, 70))

# Set font paths
font_folder = "Fonts"
font_path = os.path.join(font_folder, "SixWeekHolidayDEMO-Regular.otf")
button_font_path = os.path.join(font_folder, "Bakemono-Stereo-Regular-trial.ttf")
question_font_path = os.path.join(font_folder, "Invisible-ExtraBold.otf")
option_font_path = os.path.join(font_folder, "Please write me a song.ttf")
score_font_path = os.path.join(font_folder, "Cute Notes.ttf")
username_font = pygame.font.Font(None, 20)

# Set fonts
message_font = pygame.font.Font(font_path, 36)
button_font = pygame.font.Font(button_font_path, 24)
question_font = pygame.font.Font(question_font_path, 28)
option_font = pygame.font.Font(option_font_path, 24)
score_font = pygame.font.Font(score_font_path, 36)

# Load background image
background_image = pygame.image.load("Images/background.png")
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Function to detect when the player clicks on the back button
def check_back_button_click():
    mouse_pos = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_pos):
        return True
    return False

# Define button dimensions and positions
button_width = 200
button_height = 50
button_x = window_width // 2 - button_width // 2
button_y = window_height // 2 + 50

# Define box dimensions and positions for the options of the quiz
option_box_width = 400
option_box_height = 200
option_box_x = (window_width - option_box_width) // 2
option_box_y = window_height // 2 + 50

# Define the border radius for the option boxes
option_box_border_radius = 50

quiz_questions = [    
    {    
        "question": "Your bank sends you an email asking you to click on a link to verify your account details. What should you do?",    
        "options": {    
            "A": "Click on the link and enter your account details",    
            "B": "Forward the email to your bank's customer support for verification",    
            "C": "Ignore the email and delete it",    
            "D": "Reply to the email with your account details"    
        },    
        "answer": "B"    
    },    
    {    
        "question": "You receive a phone call from someone claiming to be a technical support representative from a well-known company. They ask for your personal information to fix a supposed issue with your computer. What should you do?",    
        "options": {    
            "A": "Provide them with the requested information",    
            "B": "Hang up the phone and report the call to the company's official support line",    
            "C": "Follow their instructions to fix the issue",    
            "D": "Stay on the call and engage with them to gather more information"    
       },    
        "answer": "B"    
    },    
   {    
       "question": "You receive an email stating that you've won a free vacation and need to provide your credit card details to claim the prize. What should you do?",    
        "options": {    
            "A": "Reply to the email with your credit card details",    
            "B": "Delete the email immediately",    
            "C": "Click on the provided link and enter your credit card details",    
            "D": "Forward the email to the authorities for investigation"    
        },    
        "answer": "B"    
    },    
    {    
        "question": "You receive a text message with a link claiming to be from your mobile service provider. It asks you to update your billing information by clicking the link. What should you do?",    
        "options": {    
            "A": "Click on the link and update your billing information",    
            "B": "Ignore the message and delete it",    
            "C": "Reply to the message with your billing information",    
            "D": "Contact your mobile service provider through their official channels to verify the message"    
        },    
        "answer": "D"    
    },    
    {    
       "question": "You receive an email from a social media platform stating that your account will be suspended unless you verify your login credentials by clicking on a link. What should you do?",    
        "options": {    
            "A": "Click on the link and enter your login credentials",    
            "B": "Forward the email to the social media platform's support team for verification",    
            "C": "Ignore the email and delete it",    
            "D": "Reply to the email with your login credentials"    
        },    
        "answer": "C"    
    },    
    {    
        "question": "You receive a pop-up message on your computer screen claiming that your device is infected with a virus and you need to call a provided phone number for immediate assistance. What should you do?",    
        "options": {    
            "A": "Call the provided phone number for assistance",    
            "B": "Disconnect from the internet and run a reputable antivirus scan on your device",    
            "C": "Ignore the message and continue using your device",    
            "D": "Reply to the pop-up message with your personal information"    
        },    
        "answer": "B"    
    },    
    {    
        "question": "You receive a message on a social media platform from someone you don't know, offering you a lucrative business opportunity. They ask for your bank account details to proceed. What should you do?",    
        "options": {    
            "A": "Provide them with your bank account details",    
            "B": "Report the message as spam and block the sender",    
            "C": "Engage in conversation to gather more information about the opportunity",    
            "D": "Forward the message to your bank for verification"    
        },    
        "answer": "B"    
    },    
    {    
        "question": "You receive an email claiming to be from a charity organization, requesting a donation. They ask for your credit card details to process the donation. What should you do?",    
        "options": {    
            "A": "Donate and provide your credit card details",    
            "B": "Forward the email to the charity organization for verification",    
            "C": "Delete the email immediately",    
            "D": "Reply to the email with your credit card details"    
        },    
        "answer": "B"    
    },    
    {    
        "question": "You receive a phone call from someone asking for your personal information to update their records. They claim to be from a legitimate organization. What should you do?",    
        "options": {    
            "A": "Provide them with the requested information",    
            "B": "Hang up the phone and report the call to the appropriate authorities",    
            "C": "Follow their instructions and provide the requested information",    
            "D": "Engage in conversation to gather more information about the purpose of the call"    
        },    
        "answer": "B"    
    },    
    {    
        "question": "You receive an email stating that your email account will be deleted unless you click on a provided link to confirm your account details. What should you do?",    
        "options": {    
            "A": "Click on the link and enter your account details",    
            "B": "Delete the email immediately",    
            "C": "Forward the email to your email service provider for verification",    
            "D": "Reply to the email with your account details"    
        },    
        "answer": "B"    
    }    
]  

# Initialize game variables
config.game_state = "PLAY_GAME"
current_question_index = 0
score = 0

# Function to shuffle the options
def shuffle_options(options):
    keys = list(options.keys())
    random.shuffle(keys)
    shuffled_options = {key: options[key] for key in keys}
    return shuffled_options

# cursor visibility
cursor_visible = True
clock = pygame.time.Clock()

# Function to check if the selected answer is correct
def check_answer(selected_answer, correct_answer):
    return selected_answer == correct_answer

# Define the offset value for moving the question higher
question_offset = 100

# Function to draw the main game screen
def draw_game_screen():

    global background_image
    global window_height, window_width
    global current_question_index, score

    window.blit(background_image, (0, 0))

    wrapped_question = textwrap.wrap(
        f"{current_question_index + 1}/{len(quiz_questions)}: " + quiz_questions[current_question_index]["question"],
        width=50
    )

    for i, line in enumerate(wrapped_question):
        question_line_text = question_font.render(line, True, BLACK)
        question_text_rect = question_line_text.get_rect(center=(window_width // 2, window_height // 2 - 100 - question_offset + i * 30))
        window.blit(question_line_text, question_text_rect)

    options = shuffle_options(quiz_questions[current_question_index]["options"])
    option_rects = []

    for i, (option_key, option_value) in enumerate(options.items()):
        option_text = option_font.render(f"{option_key}. {option_value}", True, BLACK)
        option_text_rect = option_text.get_rect(center=(window_width // 2, window_height // 2 + i * 70))
        option_rects.append(option_text_rect)

        option_box_rect = pygame.Rect(
            option_text_rect.left - 10,
            option_text_rect.top - 5,
            option_text_rect.width + 20,
            option_text_rect.height + 10
        )
        pygame.draw.rect(window, ALICEBLUE, option_box_rect, border_radius=option_box_border_radius)
        pygame.draw.rect(window, CYAN_AZURE, option_box_rect, 3, border_radius=option_box_border_radius)
        window.blit(option_text, option_text_rect)

    pygame.display.update()

    # Wait for user input
    option_selected = False

    while not option_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE: 
                window_width, window_height = event.size 
                background_image = pygame.transform.scale(background_image, (window_width, window_height)) 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, option_rect in enumerate(option_rects):
                    if option_rect.collidepoint(event.pos):
                        selected_option = list(options.keys())[i]
                        selected_option_text = quiz_questions[current_question_index]['options'][selected_option]

                        if check_answer(selected_option, quiz_questions[current_question_index]["answer"]):
                            score += 1
                            # Highlight the selected option green (correct)
                            pygame.draw.rect(window, LIGHT_GREEN, option_rect)
                        else:
                            # Highlight the selected option red (incorrect)
                            pygame.draw.rect(window, RED, option_rect)
                        pygame.display.update()  # Update the display to apply the color change

                        option_selected = True

                        # Update the selected option text to white and blit it
                        selected_option_index = list(options.keys()).index(selected_option)
                        selected_option_rect = option_rects[selected_option_index]
                        option_text = option_font.render(f"{selected_option}. {selected_option_text}", True, WHITE)
                        window.blit(option_text, selected_option_rect)
                        pygame.display.update()  # Update the display to apply the text change
                        pygame.time.delay(1000)
                        break  # Exit the loop as the option is selected
    current_question_index += 1
    if current_question_index == len(quiz_questions):
        game_over()

# Function to draw the game over screen
def game_over():
    global current_question_index, score

    window.blit(background_image, (0, 0))
    global back_button_rect  # Add back_button_rect to the global scope
    back_button_rect = back_button_image.get_rect(topleft=(10, 10))
    window.blit(back_button_image, (10, 10))

    if config.avatar_image_path is not None:
        avatar_image = pygame.image.load(config.avatar_image_path)
        avatar_image = pygame.transform.scale(avatar_image, (60, 60))
        avatar_rect = avatar_image.get_rect(topright=(window_width - 20, 20))
        window.blit(avatar_image, avatar_rect)
        
        # Retrieve the player's name from the Config object
        player_name = config.get_username()
        player_name_text = username_font.render("Player: {}".format(player_name), True, BLACK)
        
        # Position the player's name text below the avatar image
        player_name_rect = player_name_text.get_rect(topright=(window_width - 20, avatar_rect.bottom + 10))
        window.blit(player_name_text, player_name_rect)

    game_over_text = message_font.render("Game Over!", True, BLACK)
    game_over_text_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2 - 100))
    window.blit(game_over_text, game_over_text_rect)

    score_text = score_font.render(f"Your Score: {score}/{len(quiz_questions)}", True, BLACK)
    score_text_rect = score_text.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(score_text, score_text_rect)

    play_again_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    play_again_text = button_font.render("You Did it!", True, BLACK)
    play_again_text_rect = play_again_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    pygame.draw.rect(window, GREEN, play_again_rect)
    window.blit(play_again_text, play_again_text_rect)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Create a function to update the background image
def update_background_image():
    print("update background is running")
    global background_image
    background_image = pygame.image.load("Images/background.png")
    background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Main game loop
def main(config):
    global window, back_button_rect, window_width, window_height, current_question_index, score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.size
                window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
                update_background_image()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_back_button_click():
                    running = False
                
        if current_question_index < len(quiz_questions):
            draw_game_screen()

        pygame.display.update()

if __name__ == "__main__":
    main(config)