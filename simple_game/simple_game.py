import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Scrolling Game")

# Set up player
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size
player_speed = 5
is_jumping = False
jump_count = 10

# Set up obstacles
obstacle_width = 20
obstacle_height = 20
obstacle_speed = 5
obstacle_gap = 9000  # Gap between obstacles
obstacle_frequency = 1  # Lower values for less frequent obstacles
obstacles = []

# Set up lives
lives = 3

# Set up font
font = pygame.font.Font(None, 36)

# Initialize Pygame mixer
pygame.mixer.init()

# Load the jumping sound effect
jump_sound = pygame.mixer.Sound(os.path.join("sounds", "jump_sound.mp3"))

# Load the collision sound effect (you can replace this with your specific collision sound)
collision_sound = pygame.mixer.Sound(os.path.join("sounds", "collision_sound.mp3"))

# Load the game start sound
game_start_sound = pygame.mixer.Sound(os.path.join("sounds", "game_start.mp3"))

# Load the background music
pygame.mixer.music.load(os.path.join("sounds", "background_music.mp3"))
pygame.mixer.music.set_volume(0.5)  # Set initial volume (adjust as needed)
pygame.mixer.music.play(-1)  # Loop the background music

# Set initial volume for menu
volume = 0.5

# Load the heart image
heart_image = pygame.image.load(os.path.join("models", "heart.jpg"))
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Set up start screen
start_screen_text = font.render("Press SPACE to start", True, (0, 0, 0))
start_screen_rect = start_screen_text.get_rect(center=(width // 2, height // 2))

# Set up game over screen
game_over_text = font.render("Game Over - Press SPACE to try again", True, (0, 0, 0))
game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))

# Start screen loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Display start screen
    screen.fill((255, 255, 255))
    screen.blit(start_screen_text, start_screen_rect)

    # Update the display
    pygame.display.flip()

    if keys[pygame.K_SPACE]:
        game_start_sound.play()  # Play the game start sound
        break  # Exit the start screen loop when the spacebar is pressed

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Pause menu handling
    if keys[pygame.K_ESCAPE]:
        paused = True
        selected_option = 0

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            # Handle menu navigation
            if keys[pygame.K_w]:
                selected_option = (selected_option - 1) % 3
            elif keys[pygame.K_s]:
                selected_option = (selected_option + 1) % 3

            # Adjust volume with A and D keys
            if selected_option == 1:
                if keys[pygame.K_a] and volume > 0:
                    volume -= 0.01
                elif keys[pygame.K_d] and volume < 1:
                    volume += 0.01
                pygame.mixer.music.set_volume(volume)

            # Display pause menu
            screen.fill((255, 255, 255))
            pause_text = font.render("Paused", True, (0, 0, 0))
            pause_rect = pause_text.get_rect(center=(width // 2, height // 2 - 50))
            screen.blit(pause_text, pause_rect)

            # Display menu options
            resume_text = font.render("Resume", True, (0, 0, 0))
            resume_rect = resume_text.get_rect(center=(width // 2, height // 2 + 50))
            screen.blit(resume_text, resume_rect)

            volume_text = font.render(f"Volume: {int(volume * 100)}%", True, (0, 0, 0))
            volume_rect = volume_text.get_rect(center=(width // 2, height // 2 + 100))
            screen.blit(volume_text, volume_rect)

            quit_text = font.render("Quit Game", True, (0, 0, 0))
            quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 150))
            screen.blit(quit_text, quit_rect)

            # Highlight the selected option
            if selected_option == 0:
                pygame.draw.rect(screen, (0, 0, 0), resume_rect, 2)
            elif selected_option == 1:
                pygame.draw.rect(screen, (0, 0, 0), volume_rect, 2)
            elif selected_option == 2:
                pygame.draw.rect(screen, (0, 0, 0), quit_rect, 2)

            # Update the display
            pygame.display.flip()

            # Limit frames per second
            pygame.time.Clock().tick(60)

            if keys[pygame.K_SPACE]:
                # Execute the selected option
                if selected_option == 0:
                    paused = False  # Resume the game
                elif selected_option == 2:
                    pygame.quit()  # Quit the game

    # Move player
    if keys[pygame.K_a] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_d] and player_x < width - player_size:
        player_x += player_speed

    # Jumping mechanics
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            jump_sound.play()  # Play the jump sound
            is_jumping = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # Generate random obstacles with a gap on the ground
    if random.randrange(0, 100) < obstacle_frequency:
        obstacles.append([width, height - obstacle_height - player_size])

    # Move obstacles
    for obstacle in obstacles:
        obstacle[0] -= obstacle_speed

    # Remove off-screen obstacles
    obstacles = [obstacle for obstacle in obstacles if obstacle[0] + obstacle_width > 0]

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if (
            player_x < obstacle[0] + obstacle_width
            and player_x + player_size > obstacle[0]
            and player_y + player_size > obstacle[1]
        ):
            # Decrease lives but do not reset player position on collision
            lives -= 1
            obstacles.remove(obstacle)  # Remove the collided obstacle
            collision_sound.play()  # Play the collision sound effect

    # Fill the screen with a white color
    screen.fill((255, 255, 255))

    # Draw the player
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, player_size, player_size))

    # Draw the ground (green)
    pygame.draw.rect(screen, (0, 255, 0), (0, height - player_size, width, player_size))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

    # Draw lives in the top right corner
    for i in range(lives):
        screen.blit(heart_image, (width - (i + 1) * 40, 10))

    # Check for game over
    if lives == 0:
        # Display game over screen
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()

        # Wait for spacebar press to restart the game
        waiting_for_space = True
        while waiting_for_space:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_space = False

        # Reset game state
        lives = 3
        obstacles = []
        player_x = width // 2 - player_size // 2
        player_y = height - 2 * player_size

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(60)
