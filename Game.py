import pygame
import sys

def main():  # Main function wrapping the game logic
    # Initialize Pygame
    pygame.init()
    info = pygame.display.Info()

    # Set up the display in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("Image Movement with WASD and Scrolling Camera")

    # Load the background and minimap images
    large_image = pygame.image.load('newest_map.png')  # Background map
    large_image_width, large_image_height = large_image.get_size()
    minimap_image = pygame.image.load('MiniMap.png')  # Minimap
    minimap_image = pygame.transform.scale(minimap_image, (400, 300))  # Resized minimap

    # Set up the camera and load the rocket images
    camera_rect = pygame.Rect(0, 0, screen_width, screen_height)
    rocket_images = [
        pygame.transform.scale(pygame.image.load('Rover2.png'), (180, 180)),
        pygame.transform.scale(pygame.image.load('Rover2_frame2.png'), (180, 180)),
        pygame.transform.scale(pygame.image.load('Rover2.png'), (180, 180)),
    ]

    # Load arrow image for the minimap
    arrow_image = pygame.transform.scale(rocket_images[0], (20, 20))

    # Load the popup images for quadrants
    BottomLeft_image = pygame.image.load('RoverSelfie.png')
    TopLeft_image = pygame.image.load('Ascraeus_Mons.png')
    BottomRight_image = pygame.image.load('Arsia_Mons.png')
    TopRight_image = pygame.image.load('Pavonis_Mons.png')

    # Setup for rocket position and movement
    popup_image = BottomLeft_image
    image_index = 0
    image_rect = rocket_images[image_index].get_rect()
    image_rect.topleft = (large_image_width // 2, large_image_height // 2)
    move_speed = 9

    clock = pygame.time.Clock()

    # Rotation and animation timing
    rotation_angle = 0
    image_change_time = 100
    last_image_change = pygame.time.get_ticks()

    # Prompt setup and minimap opacity
    prompt_visible = False
    prompt_text = 'Press E to interact!'
    font = pygame.font.Font(None, 36)
    minimap_alpha = 150
    expanding_image = False
    expansion_scale = 0.0
    target_scale = 0.5
    scaling_speed = 0.05

    # Instruction text for player
    instruction_font = pygame.font.Font(None, 36)
    instruction_text = instruction_font.render("Press WASD to move", True, (255, 255, 255))

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            running = False

        # Handle movement and rotation logic
        moving = False
        if keys[pygame.K_w] and keys[pygame.K_d]:
            image_rect.y -= move_speed
            image_rect.x += move_speed
            rotation_angle = 315
            moving = True
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            image_rect.y -= move_speed
            image_rect.x -= move_speed
            rotation_angle = 45
            moving = True
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            image_rect.y += move_speed
            image_rect.x += move_speed
            rotation_angle = 225
            moving = True
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            image_rect.y += move_speed
            image_rect.x -= move_speed
            rotation_angle = 135
            moving = True
        elif keys[pygame.K_w] and image_rect.top > 0:
            image_rect.y -= move_speed
            rotation_angle = 0
            moving = True
        elif keys[pygame.K_a] and image_rect.left > 0:
            image_rect.x -= move_speed
            rotation_angle = 90
            moving = True
        elif keys[pygame.K_s] and image_rect.bottom < large_image_height:
            image_rect.y += move_speed
            rotation_angle = 180
            moving = True
        elif keys[pygame.K_d] and image_rect.right < large_image_width:
            image_rect.x += move_speed
            rotation_angle = 270
            moving = True

        # Keep the camera centered on the player
        camera_rect.center = image_rect.center

        # Clamp the camera to the map edges
        if camera_rect.left < 0:
            camera_rect.left = 0
        if camera_rect.right > large_image_width:
            camera_rect.right = large_image_width
        if camera_rect.top < 0:
            camera_rect.top = 0
        if camera_rect.bottom > large_image_height:
            camera_rect.bottom = large_image_height

        screen.fill((0, 0, 0))  # Clear the screen

        # Draw the background map
        screen.blit(large_image, (0 - camera_rect.left, 0 - camera_rect.top))

        # Animate the rocket if it's moving
        if moving:
            current_time = pygame.time.get_ticks()
            if current_time - last_image_change > image_change_time:
                image_index = (image_index + 1) % len(rocket_images)
                last_image_change = current_time

        # Rotate the rocket based on movement direction
        rotated_image = pygame.transform.rotate(rocket_images[image_index], rotation_angle)
        rotated_rect = rotated_image.get_rect(center=image_rect.center)
        screen.blit(rotated_image, rotated_rect.move(-camera_rect.left, -camera_rect.top))

        # Display instruction text
        screen.blit(instruction_text, (10, 10))

        # Draw the minimap with transparency
        transparent_minimap = pygame.Surface((500, 300), pygame.SRCALPHA)
        transparent_minimap.set_alpha(minimap_alpha)
        transparent_minimap.blit(minimap_image, (0, 0))
        minimap_rect = pygame.Rect(screen_width - 410, 10, 400, 300)
        screen.blit(transparent_minimap, minimap_rect.topleft)

        # Update the minimap player's position
        minimap_scale_x = minimap_rect.width / large_image_width
        minimap_scale_y = minimap_rect.height / large_image_height
        minimap_player_x = int((image_rect.x * minimap_scale_x) + minimap_rect.x)
        minimap_player_y = int((image_rect.y * minimap_scale_y) + minimap_rect.y)

        arrow_rotated = pygame.transform.rotate(arrow_image, -rotation_angle)
        arrow_rect = arrow_rotated.get_rect(center=(minimap_player_x, minimap_player_y))
        screen.blit(arrow_rotated, arrow_rect.topleft)

        # Check pixel color on the minimap to trigger interactions
        minimap_player_pos = (minimap_player_x - minimap_rect.x, minimap_player_y - minimap_rect.y)
        if 0 <= minimap_player_pos[0] < minimap_image.get_width() and 0 <= minimap_player_pos[1] < minimap_image.get_height():
            current_pixel_color = minimap_image.get_at((minimap_player_pos[0], minimap_player_pos[1]))
        else:
            current_pixel_color = (0, 0, 0)

        # Handle quadrant image display logic
        if current_pixel_color[1] > 40:
            prompt_visible = True
            screen_center_x = screen_width // 2
            screen_center_y = screen_height // 2
            player_screen_x = image_rect.centerx - camera_rect.left
            player_screen_y = image_rect.centery - camera_rect.top

            if player_screen_x <= screen_center_x and player_screen_y <= screen_center_y:
                popup_image = TopLeft_image
            elif player_screen_x > screen_center_x and player_screen_y <= screen_center_y:
                popup_image = TopRight_image
            elif player_screen_x < screen_center_x and player_screen_y > screen_center_y:
                popup_image = BottomLeft_image
            elif player_screen_x > screen_center_x and player_screen_y > screen_center_y:
                popup_image = BottomRight_image
        else:
            prompt_visible = False

        # Display prompt and handle interaction
        if prompt_visible and not expanding_image:
            prompt_surface = font.render(prompt_text, True, (255, 255, 255))
            screen.blit(prompt_surface, (10, screen_height - 40))

            if keys[pygame.K_e]:
                expanding_image = True
                expansion_scale = 0.0

        # Handle image expansion effect
        if expanding_image:
            expansion_scale += scaling_speed
            if expansion_scale >= target_scale:
                expansion_scale = target_scale

            scaled_image = pygame.transform.scale(popup_image, (int(popup_image.get_width() * 0.43 * expansion_scale),
                                                                int(popup_image.get_height() * 0.43 * expansion_scale)))
            scaled_rect = scaled_image.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(scaled_image, scaled_rect)

        # Reset expansion if the player moves
        if moving and expanding_image:
            expanding_image = False

        # Update the display and control frame rate
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
