import pygame
import cv2
import sys
import Game  # Assuming 'game.py' is in the same directory as this file
import random
import os  # For handling file paths

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize Pygame and the mixer for audio
pygame.init()
pygame.mixer.init()

# Set up the display in fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Mars Rover Adventure")

# Function to play video using OpenCV in fullscreen mode
def play_video(video_path, sound_path):
    # Load and play the background sound
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play(-1)  # -1 means the sound will loop indefinitely during video playback

    # Open the video using OpenCV
    cap = cv2.VideoCapture(video_path)

    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS) if cap.get(cv2.CAP_PROP_FPS) > 0 else 60  # Default to 60 if FPS is not available

    # Load font and render the "Press space to skip" text
    font = pygame.font.Font(None, 36)
    skip_text = font.render("Press space to skip", True, (255, 255, 255))  # White text initially
    skip_text_surface = skip_text.convert_alpha()

    # Position the text slightly to the left and upwards
    skip_text_width, skip_text_height = skip_text.get_size()
    skip_text_x = screen_width - skip_text_width - 50  # Moved more to the left
    skip_text_y = screen_height - skip_text_height - 50  # Moved more upwards

    # Start playing the video
    clock = pygame.time.Clock()  # Pygame clock to manage frame rate
    while cap.isOpened():
        ret, frame = cap.read()  # Read the next video frame
        if not ret:
            break  # Break the loop if the video ends

        # Convert the OpenCV image (BGR) to Pygame surface (RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame_rgb)

        # Rotate the frame 90 degrees counterclockwise to fix the sideways video
        frame_surface = pygame.transform.rotate(frame_surface, 270)

        # Flip the frame horizontally to fix the mirroring issue
        frame_surface = pygame.transform.flip(frame_surface, True, False)

        # Scale the rotated and flipped frame to fit fullscreen
        frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))

        # Draw the video frame on the screen
        screen.blit(frame_surface, (0, 0))

        # Draw the "Press space to skip" text at the updated position
        screen.blit(skip_text_surface, (skip_text_x, skip_text_y))

        # Update the Pygame display
        pygame.display.flip()

        # Manage frame rate according to the video's fps
        clock.tick(fps)  # Ensures the loop runs at the same speed as the video

        # Event handling (quit and spacebar for skipping)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.mixer.music.stop()  # Stop the sound when quitting
                pygame.quit()
                sys.exit()  # Ensure we quit the program gracefully
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Check if spacebar is pressed
                    cap.release()
                    pygame.mixer.music.stop()  # Stop the sound when skipping the video
                    return  # Exit the function to skip the video

    # Fade out transition after video ends
    fade_out()

    # Release the video capture object and stop the sound
    cap.release()
    pygame.mixer.music.stop()  # Stop the sound after the video ends

# Function for fading out the screen to black
def fade_out():
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))  # Black surface

    for alpha in range(0, 300):  # Gradually increase opacity
        fade_surface.set_alpha(alpha // 3)  # Gradually make the surface more opaque
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)  # Delay to control fade speed

# Function for fading in the lobby image
def fade_in(image_surface):
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))  # Black surface

    for alpha in range(255, -1, -5):  # Gradually reduce opacity
        screen.blit(image_surface, (0, 0))  # Draw the image first
        fade_surface.set_alpha(alpha)  # Overlay the black surface to fade in
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)  # Delay to control fade speed

# Function to display the lobby image with a fade-in transition and play music
def show_lobby(image_path, music_path):
    # Load and play the music
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    # Load the lobby image
    lobby_image = pygame.image.load(image_path)

    # Scale the image to fullscreen
    lobby_image = pygame.transform.scale(lobby_image, (screen_width, screen_height))

    # Load the font for displaying the "Press Enter to Play" and "Press Q to Quit" text
    font = pygame.font.Font(None, 50)
    enter_text = font.render("Press Enter to Play", True, (255, 255, 255))  # White text
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))  # White text

    # Get the size of the text
    enter_text_width, enter_text_height = enter_text.get_size()
    quit_text_width, quit_text_height = quit_text.get_size()

    # Adjust the position of "Press Enter to Play" (a bit lower and to the right)
    base_enter_text_x = (screen_width - enter_text_width) // 2 + 10
    base_enter_text_y = screen_height - 90  # Slightly lower than before

    quit_text_x = 30  # Adjusted to move a bit to the right
    quit_text_y = 30  # Adjusted to move slightly lower

    # Fade in the image
    fade_in(lobby_image)

    # Main lobby loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_with_fade_out()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # If Enter is pressed
                    running = False  # Exit the lobby
                elif event.key == pygame.K_q:  # If Q is pressed, quit the program
                    quit_with_fade_out()

        # Random shake effect for "Press Enter to Play"
        shake_x = random.randint(-2, 2)
        shake_y = random.randint(-2, 2)

        # Display the lobby image and text
        screen.blit(lobby_image, (0, 0))  # Display the lobby image
        screen.blit(enter_text, (base_enter_text_x + shake_x, base_enter_text_y + shake_y))  # Display shaking "Press Enter to Play" text
        screen.blit(quit_text, (quit_text_x, quit_text_y))  # Display "Press Q to Quit" text

        # Update the display
        pygame.display.flip()

    # Fade out the lobby before starting the game
    fade_out()

    # After fading out the lobby, run the integrated game logic from game.py
    run_game()

# Function to handle quitting with a fade out animation
def quit_with_fade_out():
    fade_out()  # Apply fade out animation
    pygame.quit()  # Quit the game after the fade out
    sys.exit()

# Function that calls game.py's game logic
def run_game():
    # Call the main game loop or function from game.py
    Game.main()  # Assuming game.py has a main() function that starts the game

# Main function
def main():
    # Use relative paths for all assets
    video_path = os.path.join(script_dir, "background6.mp4")
    sound_path = os.path.join(script_dir, "space song.mp3")
    lobby_image_path = os.path.join(script_dir, "maRS.png")
    music_path = os.path.join(script_dir, "space mountain.mp3")

    play_video(video_path, sound_path)

    # After the video ends or is skipped, show the lobby image with music
    show_lobby(lobby_image_path, music_path)

if __name__ == "__main__":
    main()
