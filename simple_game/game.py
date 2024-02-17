# game.py
import pygame
import random
import os
from pause_menu import PauseMenu

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Scrolling Game")

        # Set up player
        self.player_size = 50
        self.player_x = self.width // 2 - self.player_size // 2
        self.player_y = self.height - 2 * self.player_size
        self.player_speed = 5
        self.is_jumping = False
        self.jump_count = 10

        # Set up obstacles
        self.obstacle_width = 20
        self.obstacle_height = 20
        self.obstacle_speed = 5
        self.obstacle_gap = 9000  # Gap between obstacles
        self.obstacle_frequency = 1  # Lower values for less frequent obstacles
        self.obstacles = []

        # Set up lives
        self.lives = 3

        # Set up font
        self.font = pygame.font.Font(None, 36)

        # Load the jumping sound effect
        self.jump_sound = pygame.mixer.Sound(os.path.join("sounds", "jump_sound.mp3"))

        # Load the collision sound effect (you can replace this with your specific collision sound)
        self.collision_sound = pygame.mixer.Sound(os.path.join("sounds", "collision_sound.mp3"))

        # Load the game start sound
        self.game_start_sound = pygame.mixer.Sound(os.path.join("sounds", "game_start.mp3"))

        # Load the background music
        pygame.mixer.music.load(os.path.join("sounds", "background_music.mp3"))
        pygame.mixer.music.set_volume(0.5)  # Set initial volume (adjust as needed)
        pygame.mixer.music.play(-1)  # Loop the background music

        # Set initial volume for menu
        self.volume = 0.5

        # Load the heart image
        self.heart_image = pygame.image.load(os.path.join("models", "heart.jpg"))
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))

        # Set up start screen
        self.start_screen_text = self.font.render("Press SPACE to start", True, (0, 0, 0))
        self.start_screen_rect = self.start_screen_text.get_rect(center=(self.width // 2, self.height // 2))

        # Set up game over screen
        self.game_over_text = self.font.render("Game Over - Press SPACE to try again", True, (0, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(center=(self.width // 2, self.height // 2))

        # Initialize pause menu
        self.pause_menu = PauseMenu(self.screen, self.font, self.width, self.height)

    def handle_events(self):
        # Event handling code goes here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Pause menu handling
        if keys[pygame.K_ESCAPE]:
            self.pause_menu.run()

    def update(self):
        # Update logic goes here
        keys = pygame.key.get_pressed()

        # Move player
        if keys[pygame.K_a] and self.player_x > 0:
            self.player_x -= self.player_speed
        if keys[pygame.K_d] and self.player_x < self.width - self.player_size:
            self.player_x += self.player_speed

        # Jumping mechanics
        if not self.is_jumping:
            if keys[pygame.K_SPACE]:
                self.jump_sound.play()  # Play the jump sound
                self.is_jumping = True
        else:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.player_y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

        # Generate random obstacles with a gap on the ground
        if random.randrange(0, 100) < self.obstacle_frequency:
            self.obstacles.append([self.width, self.height - self.obstacle_height - self.player_size])

        # Move obstacles
        for obstacle in self.obstacles:
            obstacle[0] -= self.obstacle_speed

        # Remove off-screen obstacles
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle[0] + self.obstacle_width > 0]

        # Check for collisions with obstacles
        for obstacle in self.obstacles:
            if (
                self.player_x < obstacle[0] + self.obstacle_width
                and self.player_x + self.player_size > obstacle[0]
                and self.player_y + self.player_size > obstacle[1]
            ):
                # Decrease lives but do not reset player position on collision
                self.lives -= 1
                self.obstacles.remove(obstacle)  # Remove the collided obstacle
                self.collision_sound.play()  # Play the collision sound effect

    def draw(self):
        # Drawing code goes here
        # Fill the screen with a white color
        self.screen.fill((255, 255, 255))

        # Draw the player
        pygame.draw.rect(self.screen, (0, 0, 255), (self.player_x, self.player_y, self.player_size, self.player_size))

        # Draw the ground (green)
        pygame.draw.rect(self.screen, (0, 255, 0), (0, self.height - self.player_size, self.width, self.player_size))

        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (255, 0, 0), (obstacle[0], obstacle[1], self.obstacle_width, self.obstacle_height))

        # Draw lives in the top right corner
        for i in range(self.lives):
            self.screen.blit(self.heart_image, (self.width - (i + 1) * 40, 10))

        # Check for game over
        if self.lives == 0:
            # Display game over screen
            self.screen.blit(self.game_over_text, self.game_over_rect)

    def run(self):
        running = True

        while running:
            self.handle_events()
            self.update()
            self.draw()

            # Update the display
            pygame.display.flip()

            # Limit frames per second
            pygame.time.Clock().tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
