import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display (this is the size of the player's view)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Image Movement with WASD and Scrolling Camera")

# Load the large background image (this is the entire world)
large_image = pygame.image.load('MainBG2.png')
large_image_width, large_image_height = large_image.get_size()

# Load and resize the custom minimap image
minimap_image = pygame.image.load('MiniMap.png')  # Load your custom minimap image
minimap_image = pygame.transform.scale(minimap_image, (200, 150))  # Resize it as needed

# Reduce the size of the camera (viewing area)
camera_rect = pygame.Rect(0, 0, screen_width, screen_height)

# Load and resize the player images (rocket)
rocket_images = [
    pygame.transform.scale(pygame.image.load('frame_0.png'), (96, 96)),  # First rocket image
    pygame.transform.scale(pygame.image.load('frame_1.png'), (96, 96)),  # Second rocket image
    pygame.transform.scale(pygame.image.load('frame_end.png'), (96, 96)),  # Third rocket image
]

# Load and resize the arrow image for the minimap
arrow_image = pygame.transform.scale(rocket_images[0], (20, 20))  # Arrow for minimap (using the first rocket image)

# Load the image to display when pressing "E"
popup_image = pygame.image.load('RoverSelfie.png')  # Replace with your image
popup_image_rect = popup_image.get_rect(center=(screen_width // 2, screen_height // 2))

image_index = 0  # To track which image to show
image_rect = rocket_images[image_index].get_rect()  # Get the rect of the resized image

# Set the initial position of the player (inside the larger world)
image_rect.topleft = (large_image_width // 2, large_image_height // 2)

# Define movement speed
move_speed = 5

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Initialize rotation angle
rotation_angle = 0

# Time for image change
image_change_time = 100  # Time in milliseconds to change image
last_image_change = pygame.time.get_ticks()  # Track the last image change time

# Prompt variables
prompt_visible = False  # To control the visibility of the prompt message
prompt_text = 'Press E to interact!'  # The prompt message
font = pygame.font.Font(None, 36)  # Font for the prompt text

# Set transparency level (0-255, where 255 is fully opaque)
minimap_alpha = 150  # 150 will give a semi-transparent effect

# Variables for expanding the image
expanding_image = False  # Track if the image is currently expanded
expansion_scale = 0.0  # Start scale for the expansion animation
target_scale = 0.5  # Target scale (50% of screen size)
scaling_speed = 0.05  # Speed at which the image scales

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Check for quitting the game
    if keys[pygame.K_q]:  # Check if the 'Q' key is pressed
        running = False

    # Determine the direction of movement and adjust the rotation angle
    moving = False
    if keys[pygame.K_w] and image_rect.top > 0:  # Move up
        image_rect.y -= move_speed
        rotation_angle = 270  # Upwards
        moving = True
    if keys[pygame.K_a] and image_rect.left > 0:  # Move left
        image_rect.x -= move_speed
        rotation_angle = 0  # Left
        moving = True
    if keys[pygame.K_s] and image_rect.bottom < large_image_height:  # Move down
        image_rect.y += move_speed
        rotation_angle = 90  # Downwards
        moving = True
    if keys[pygame.K_d] and image_rect.right < large_image_width:  # Move right
        image_rect.x += move_speed
        rotation_angle = 180  # Right
        moving = True

    # Update the camera to follow the player
    camera_rect.center = image_rect.center

    # Make sure the camera doesn't go out of the world bounds
    if camera_rect.left < 0:
        camera_rect.left = 0
    if camera_rect.right > large_image_width:
        camera_rect.right = large_image_width
    if camera_rect.top < 0:
        camera_rect.top = 0
    if camera_rect.bottom > large_image_height:
        camera_rect.bottom = large_image_height

    # Clear the screen
    screen.fill((0, 0, 0))

    # Blit only the portion of the large image that's within the smaller camera view
    screen.blit(large_image, (0, 0), camera_rect)

    # Rotate the rocket based on the movement direction
    if moving:
        current_time = pygame.time.get_ticks()  # Get the current time
        if current_time - last_image_change > image_change_time:  # Check if enough time has passed
            image_index = (image_index + 1) % len(rocket_images)  # Cycle through images
            last_image_change = current_time  # Reset the last change time

        # Rotate the current rocket image
        rotated_image = pygame.transform.rotate(rocket_images[image_index], rotation_angle)
        rotated_rect = rotated_image.get_rect(center=image_rect.center)
        screen.blit(rotated_image, rotated_rect.move(-camera_rect.left, -camera_rect.top))
    else:
        # If not moving, draw the rocket as is
        screen.blit(rocket_images[image_index], image_rect.move(-camera_rect.left, -camera_rect.top))

    # Create a transparent surface for the minimap
    transparent_minimap = pygame.Surface((200, 150), pygame.SRCALPHA)
    transparent_minimap.set_alpha(minimap_alpha)  # Apply transparency

    # Blit the minimap image onto the transparent surface
    transparent_minimap.blit(minimap_image, (0, 0))

    # Blit the transparent minimap onto the screen
    minimap_rect = pygame.Rect(screen_width - 210, 10, 200, 150)  # Position for the minimap
    screen.blit(transparent_minimap, minimap_rect.topleft)

    # Calculate player's position on the minimap
    minimap_scale_x = minimap_rect.width / large_image_width
    minimap_scale_y = minimap_rect.height / large_image_height

    minimap_player_x = int((image_rect.x * minimap_scale_x) + minimap_rect.x)
    minimap_player_y = int((image_rect.y * minimap_scale_y) + minimap_rect.y)

    # Blit the arrow on the minimap
    arrow_rotated = pygame.transform.rotate(arrow_image, -rotation_angle)  # Rotate arrow to match player direction
    arrow_rect = arrow_rotated.get_rect(center=(minimap_player_x, minimap_player_y))
    screen.blit(arrow_rotated, arrow_rect.topleft)

    # Detect the color of the pixel the player is standing on
    minimap_player_pos = (minimap_player_x - minimap_rect.x, minimap_player_y - minimap_rect.y)  # Position on minimap image
    if 0 <= minimap_player_pos[0] < minimap_image.get_width() and 0 <= minimap_player_pos[1] < minimap_image.get_height():
        current_pixel_color = minimap_image.get_at((minimap_player_pos[0], minimap_player_pos[1]))  # Get pixel color
    else:
        current_pixel_color = (0, 0, 0)  # Default to black if out of bounds

    # Check if the green component of the pixel color is greater than 40
    if current_pixel_color[1] > 40:  # Green value is greater than 40
        prompt_visible = True
    else:
        prompt_visible = False

    # Display prompt message if visible
    if prompt_visible and not expanding_image:
        prompt_surface = font.render(prompt_text, True, (255, 255, 255))  # Create text surface
        screen.blit(prompt_surface, (10, screen_height - 40))  # Draw prompt text on screen

        # Check for interaction (pressing "E")
        if keys[pygame.K_e]:  
            expanding_image = True
            expansion_scale = 0.0  # Reset scale for the expansion animation

    # If the image is expanding, animate it
    if expanding_image:
        # Increase the scale over time
        expansion_scale += scaling_speed
        if expansion_scale >= target_scale:  # Stop when it reaches the target size
            expansion_scale = target_scale  # Clamp the value to the target scale
        
        # Scale the image
        scaled_image = pygame.transform.scale(popup_image, 
            (int(popup_image.get_width() * expansion_scale), int(popup_image.get_height() * expansion_scale)))
        
        # Center the scaled image
        scaled_rect = scaled_image.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(scaled_image, scaled_rect)

    # If the player moves while the image is expanded, hide the image
    if moving and expanding_image:
        expanding_image = False

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
