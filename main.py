import pygame   
import sys   
import os   
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

# Set the path to your sound files    
sound_folder = "Sounds"   

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
window_width, window_height = info.current_w, info.current_h
window = pygame.display.set_mode((window_width - 10, window_height - 50), pygame.RESIZABLE)

pygame.display.set_caption("CyberStart")   
swoosh_sound = pygame.mixer.Sound(os.path.join(sound_folder, "optimistic.mp3"))   
option_sound = pygame.mixer.Sound(os.path.join(sound_folder, "Button.mp3"))  
 
sound_enabled = True   
mute_icon = pygame.transform.scale(pygame.image.load("Images/mute.png"), (30, 30))   
unmute_icon = pygame.transform.scale(pygame.image.load("Images/unmute.png"), (30, 30))   
icon_size = mute_icon.get_size()   
icon_rect = mute_icon.get_rect(topright=(window_width - 20, 20))   

def update_icon_position():
    icon_rect.topright = (window_width - 20, 20)

font_folder = "Fonts"   
font_path = os.path.join(font_folder, "SixWeekHolidayDEMO-Regular.otf")   
button_font_path = os.path.join(font_folder, "Bakemono-Stereo-Regular-trial.ttf")   
question_font_path = os.path.join(font_folder, "Invisible-ExtraBold.otf")   
option_font_path = os.path.join(font_folder, "Please write me a song.ttf")   
score_font_path = os.path.join(font_folder, "Cute Notes.ttf")   
username_font = pygame.font.Font(None, 20)    

# Play sound effect when navigating through menus   
def on_menu_navigation():   
    swoosh_sound.play()   

message_font = pygame.font.Font(font_path, 36)   
button_font = pygame.font.Font(button_font_path, 24)   
question_font = pygame.font.Font(question_font_path, 28)   
option_font = pygame.font.Font(option_font_path, 24)   
score_font = pygame.font.Font(score_font_path, 36)   

# Load background image   
background_image = pygame.image.load("Images/background.png")   
background_image = pygame.transform.scale(background_image, (window_width, window_height))   

# Define button dimensions and positions   
button_width = 200   
button_height = 50   
button_x = window_width // 2 - button_width // 2   
button_y = window_height // 2 + 50   
character_images = [   
    pygame.transform.scale(pygame.image.load("Images/man icon.png"), (200, 200)),   
    pygame.transform.scale(pygame.image.load("Images/women icon.png"), (200, 200))   
]    

character_image_paths = {  
    "man": "Images/man icon.png",  
    "woman": "Images/women icon.png"  
}  

avatar_image = None   
character_rects = [   
    pygame.Rect(150, 300, 200, 200),   
    pygame.Rect(450, 300, 200, 200)   
]   

game_state = "START"   
user_name = ""   
current_question_index = 0   
score = 0   
chosen_character = None   
chosen_avatar = None  # Add this variable to store the chosen avatar image path   
user_name = ""  # Initialize the user_name variable as an empty string   
cursor_visible = True   
clock = pygame.time.Clock()   

def resize_image(image, target_size):  
    original_size = image.get_size()  
    scale_factor = min(target_size[0] / original_size[0], target_size[1] / original_size[1])  
    new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))  
    return pygame.transform.scale(image, new_size)  

game_options = {  
    "OPTION_ONE":  "QUIZ: Answer 10 phising question and increase your cyber knowledge!!",  
    "OPTION_TWO": "HANG-MAN: Fun way to learn cybersecurity words.",  
    "OPTION_THIRD": "POWER-UP: Learn to a powerful pasword for your safety.",  
    "OPTION_FOURTH": "MEMORY GAME: Boost your memory and challange yourself."   
}  

config = Config()  
config.avatar_image_path = None  


while True:   
    window.blit(background_image, (0, 0))   
    on_menu_navigation()  # Play sound effect when transitioning to game over state                        
    if game_state == "START":   
        start_text = message_font.render("Press SPACE to Start", True, BLACK)   
        start_text_rect = start_text.get_rect(center=(window_width // 2, window_height // 2))   
        window.blit(start_text, start_text_rect)   
        pygame.display.update()   

        for event in pygame.event.get():   
            if event.type == pygame.QUIT:   
                pygame.quit()   
                sys.exit()   

            elif event.type == pygame.VIDEORESIZE: 
                # Update window dimensions 
                window_width, window_height = event.size 
                # Resize the background image to fit the new window size 
                background_image = pygame.transform.scale(background_image, (window_width, window_height))   

            elif event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_SPACE:   
                    game_state = "CHOOSE_CHARACTER"   

    elif game_state == "CHOOSE_CHARACTER":   
        window.blit(background_image, (0, 0))   
        character_text = message_font.render("Choose Your Avatar", True, BLACK)   
        character_text_rect = character_text.get_rect(center=(window_width // 2, 150))   
        window.blit(character_text, character_text_rect)   

        for i, character_rect in enumerate(character_rects):
            # Calculate the center of the character_rect based on window size
            character_rect.center = ((i + 1) * window_width // (len(character_rects) + 1), window_height // 2)
            character_image = character_images[i]
            character_image_rect = character_image.get_rect(center=character_rect.center)
            window.blit(character_image, character_image_rect)   

        icon_rect.topright = (window_width - 20, 20)

        # Check for mute/unmute icon click and character selection   
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:   
                pygame.quit()   
                sys.exit()   

            elif event.type == pygame.VIDEORESIZE: 
                window_width, window_height = event.size 
                background_image = pygame.transform.scale(background_image, (window_width, window_height)) 
                update_icon_position()

            elif event.type == pygame.MOUSEBUTTONDOWN:   
                if event.button == 1:  # Left mouse button   
                    if icon_rect.collidepoint(event.pos):   
                        sound_enabled = not sound_enabled  # Toggle sound state   
                        if sound_enabled:   
                            swoosh_sound.set_volume(1.0)  # Unmute the sound   
                        else:   
                            swoosh_sound.set_volume(0.0)  # Mute the sound   

                    for i, character_rect in enumerate(character_rects):  
                        if character_rect.collidepoint(event.pos):   
                            if i == 0:  
                                chosen_character = "man"  
                            elif i == 1:  
                                chosen_character = "woman"  
                            avatar_image = pygame.transform.scale(character_images[i], (90, 90))  

                       # Store the chosen character's image path in the config  
                            config.avatar_image_path = character_image_paths[chosen_character]  
                            game_state = "ENTER_NAME" 

        if sound_enabled:   
            window.blit(unmute_icon, icon_rect)   
        else:   
            window.blit(mute_icon, icon_rect)   
        pygame.display.update()   

    elif game_state == "ENTER_NAME":   
        cursor_visible = not cursor_visible   
        window.blit(background_image, (0, 0))   

        if avatar_image is not None:   
            avatar_rect = avatar_image.get_rect(topright=(window_width - 20, 20))   
            window.blit(avatar_image, avatar_rect)   

        name_text = message_font.render("Enter your name:", True, BLACK)   
        name_text_rect = name_text.get_rect(center=(window_width // 2, window_height // 2 - 50))   

        # Increase the width and height of the name input box   
        name_input_box_width = 300   
        name_input_box_height = 50    
        name_input_text_rect = pygame.Rect((window_width - name_input_box_width) // 2, (window_height - name_input_box_height) // 2, name_input_box_width, name_input_box_height)   
        pygame.draw.rect(window, ALICEBLUE, name_input_text_rect)   
        pygame.draw.rect(window, BLACK, name_input_text_rect, 2)   

        # Blit the user_name if it exists   
        name_input_text = button_font.render(user_name, True, BLACK)   
        name_input_text_rect = name_input_text.get_rect(center=(window_width // 2, window_height // 2))    

        # Add a cursor when it is visible   
        if cursor_visible and game_state == "ENTER_NAME":   
            cursor_rect = pygame.Rect(name_input_text_rect.x + name_input_text_rect.width, name_input_text_rect.y, 2, name_input_text_rect.height)   
            pygame.draw.rect(window, BLACK, cursor_rect)   
        window.blit(name_text, name_text_rect)   
        window.blit(name_input_text, name_input_text_rect)   

        pygame.display.update()   
        #clock.tick(5)  # Adjust the blinking speed as needed   

        if user_name:  
            user_name_text = username_font.render(f"Player: {user_name}", True, BLACK)  
            user_name_text_rect = user_name_text.get_rect(topright=(window_width - 20, 100))  
            window.blit(user_name_text, user_name_text_rect)  

        for event in pygame.event.get():   
            if event.type == pygame.QUIT:   
                pygame.quit()   
                sys.exit()   

            elif event.type == pygame.VIDEORESIZE: 
                # Update window dimensions 
                window_width, window_height = event.size 
                # Resize the background image to fit the new window size 
                background_image = pygame.transform.scale(background_image, (window_width, window_height)) 

            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RETURN:   
                    config.set_username(user_name) 
                    game_state = "GAME_OPTIONS"   

                elif event.key == pygame.K_BACKSPACE:   
                    user_name = user_name[:-1]   
                else:   
                    user_name += event.unicode   

    elif game_state == "GAME_OPTIONS":  

        options_text = message_font.render("Choose a Game Option", True, BLACK)  
        options_text_rect = options_text.get_rect(center=(window_width // 2, 150))  
        window.blit(options_text, options_text_rect)  

        if user_name:  
            user_name_text = username_font.render(f"Player: {user_name}", True, BLACK)  
            user_name_text_rect = user_name_text.get_rect(topright=(window_width - 20, 100))  
            window.blit(user_name_text, user_name_text_rect)  

        if avatar_image is not None:   
            avatar_rect = avatar_image.get_rect(topright=(window_width - 20, 20))   
            window.blit(avatar_image, avatar_rect)   

        def wrap_text(text, font, width):  
            words = text.split(' ')  
            lines = []  
            current_line = ''  
            for word in words:  
                test_line = current_line + word + ' '  
                if font.size(test_line)[0] <= width:  
                    current_line = test_line  
                else:  
                    lines.append(current_line)  
                    current_line = word + ' '  
            if current_line:  
                lines.append(current_line)  
            return lines  

        def render_paragraph(text, font, color, x, y, line_spacing, column_width):  
            lines = wrap_text(text, font, column_width)  
            for i, line in enumerate(lines):  
                text_surface = font.render(line, True, color)  
                text_rect = text_surface.get_rect(topleft=(x, y + i * line_spacing))  
                window.blit(text_surface, text_rect)  

        # Calculate the x-coordinate for center alignment
        center_x = window_width // 2

        # Calculate the y-coordinate for the vertical positioning
        y_position = 300 

        # Display images for Option 1  
        option_one_image = pygame.image.load("Images/quiz.png")  
        option_one_image = pygame.transform.scale(option_one_image, (150, 150))  # Adjust size as needed  
        option_one_rect = option_one_image.get_rect(center=(center_x - 300, y_position))
        window.blit(option_one_image, option_one_rect)  

        # Display images for Option 2  
        option_two_image = pygame.image.load("Images/hangman.png")  
        option_two_image = pygame.transform.scale(option_two_image, (150, 150))  # Adjust size as needed  
        option_two_rect = option_two_image.get_rect(center=(center_x - 100, y_position))
        window.blit(option_two_image, option_two_rect)  

        # Display images for Option 3  
        option_third_image = pygame.image.load("Images/password.png")  
        option_third_image = pygame.transform.scale(option_third_image, (150, 150))  # Adjust size as needed  
        option_third_rect = option_third_image.get_rect(center=(center_x + 100, y_position))
        window.blit(option_third_image, option_third_rect)  

        # Display images for Option 3  
        option_fourth_image = pygame.image.load("Images/memory_game.png")  
        option_fourth_image = pygame.transform.scale(option_fourth_image, (150, 150))  # Adjust size as needed  
        option_fourth_rect = option_fourth_image.get_rect(center=(center_x + 300, y_position))
        window.blit(option_fourth_image, option_fourth_rect)  

        # Create a dictionary to store option images and rects
        option_data = {
            "OPTION_ONE": [option_one_image, option_one_rect],
            "OPTION_TWO": [option_two_image, option_two_rect],
            "OPTION_THIRD": [option_third_image, option_third_rect],
            "OPTION_FOURTH": [option_fourth_image, option_fourth_rect]
        }

        for option_key, (option_image, option_rect) in option_data.items():
            window.blit(option_image, option_rect)

            render_paragraph(game_options[option_key], option_font, BLACK,
                     option_rect.left, option_rect.bottom + 10, 30, 170)
      
        pygame.display.update()  
 
        user_choice = None  
        while not user_choice:  
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    pygame.quit()  
                    sys.exit()  
                elif event.type == pygame.VIDEORESIZE: 
                    # Update window dimensions 
                    window_width, window_height = event.size 
                    # Resize the background image to fit the new window size 
                    background_image = pygame.transform.scale(background_image, (window_width, window_height)) 
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    if option_one_rect.collidepoint(event.pos):  
                        user_choice = "OPTION_ONE"  
                    elif option_two_rect.collidepoint(event.pos):  
                        user_choice = "OPTION_TWO"  
                    elif option_third_rect.collidepoint(event.pos):  
                        user_choice = "OPTION_THIRD"  
                    elif option_fourth_rect.collidepoint(event.pos):  
                        user_choice = "OPTION_FOURTH"  

        # Transition to the corresponding game module based on user's choice  
        if user_choice == "OPTION_ONE":  
            import first  
            first.main(config)  
        elif user_choice == "OPTION_TWO":  
            import second
            second.main(config)
        elif user_choice == "OPTION_THIRD":  
            import third    
            third.main(config)
        elif user_choice == "OPTION_FOURTH":  
            import fourth    
            fourth.main(config) 

    pygame.display.update()  

#C:\Users\h27592\Videos