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
    # Play background sound
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play(-1)

    # Open the video using OpenCV
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video at {video_path}")
        return

    # Get video FPS, defaulting to 60 if unavailable
    fps = cap.get(cv2.CAP_PROP_FPS) or 60

    # Render "Press space to skip" text
    font = pygame.font.Font(None, 36)
    skip_text = font.render("Press space to skip", True, (255, 255, 255))
    skip_text_x = screen_width - skip_text.get_width() - 50
    skip_text_y = screen_height - skip_text.get_height() - 50

    # Play the video
    clock = pygame.time.Clock()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert OpenCV frame to Pygame format and display it
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        frame_surface = pygame.transform.rotate(frame_surface, 270)
        frame_surface = pygame.transform.flip(frame_surface, True, False)
        frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))
        screen.blit(frame_surface, (0, 0))
        screen.blit(skip_text, (skip_text_x, skip_text_y))
        pygame.display.flip()

        # Control the frame rate and handle events
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                cap.release()
                pygame.mixer.music.stop()
                return

    fade_out()
    cap.release()
    pygame.mixer.music.stop()

# Fade-out transition function
def fade_out():
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade_surface.set_alpha(alpha // 3)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

# Fade-in transition for lobby image
def fade_in(image_surface):
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))
    for alpha in range(255, -1, -5):
        screen.blit(image_surface, (0, 0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

# Show the lobby screen with music
def show_lobby(image_path, music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

    lobby_image = pygame.image.load(image_path)
    lobby_image = pygame.transform.scale(lobby_image, (screen_width, screen_height))

    font = pygame.font.Font(None, 50)
    enter_text = font.render("Press Enter to Play", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))

    enter_text_x = (screen_width - enter_text.get_width()) // 2 + 10
    enter_text_y = screen_height - 90
    quit_text_x = 30
    quit_text_y = 30

    fade_in(lobby_image)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_with_fade_out()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_q:
                    quit_with_fade_out()

        # Add a slight shake effect to the "Press Enter to Play" text
        shake_x = random.randint(-2, 2)
        shake_y = random.randint(-2, 2)
        screen.blit(lobby_image, (0, 0))
        screen.blit(enter_text, (enter_text_x + shake_x, enter_text_y + shake_y))
        screen.blit(quit_text, (quit_text_x, quit_text_y))
        pygame.display.flip()

    fade_out()
    run_game()

# Handle quitting with fade out
def quit_with_fade_out():
    fade_out()
    pygame.quit()
    sys.exit()

# Launch the main game
def run_game():
    Game.main()

# Main function to run the program
def main():
    video_path = os.path.join(script_dir, "material/background6.mp4")
    sound_path = os.path.join(script_dir, "material/space song.mp3")
    lobby_image_path = os.path.join(script_dir, "material/lobby screen.png")
    music_path = os.path.join(script_dir, "material/space music.mp3")

    play_video(video_path, sound_path)
    show_lobby(lobby_image_path, music_path)

if __name__ == "__main__":
    main()
