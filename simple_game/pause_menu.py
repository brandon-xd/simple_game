# pause_menu.py
import pygame
import sys

class PauseMenu:
    def __init__(self, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height

        # Initialize menu variables
        self.options = ["Resume", "Volume", "Quit Game"]
        self.selected_option = 0
        self.volume = 0.5
        self.dragging_slider = False  # Variable to track slider dragging

    def draw_menu(self):
        # Display pause menu
        self.screen.fill((255, 255, 255))
        pause_text = self.font.render("Paused", True, (0, 0, 0))
        pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(pause_text, pause_rect)

        # Display menu options
        for i, option in enumerate(self.options):
            option_text = self.font.render(option, True, (0, 0, 0))
            option_rect = option_text.get_rect(center=(self.width // 2, self.height // 2 + i * 50))
            self.screen.blit(option_text, option_rect)

        # Display volume slider
        volume_text = self.font.render(f"Volume: {int(self.volume * 100)}%", True, (0, 0, 0))
        volume_rect = volume_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(volume_text, volume_rect)

        volume_slider_rect = pygame.Rect(
            self.width // 2 - 100, self.height // 2 + 75, 200, 10
        )
        volume_slider_handle_rect = pygame.Rect(
            volume_slider_rect.left + int(self.volume * volume_slider_rect.width) - 5,
            volume_slider_rect.centery - 5,
            10,
            10,
        )
        pygame.draw.rect(self.screen, (0, 0, 0), volume_slider_rect, 2)
        pygame.draw.ellipse(self.screen, (0, 0, 0), volume_slider_handle_rect)

        # Highlight the selected option
        selected_rect = option_rect.copy()
        selected_rect.inflate_ip(10, 10)
        pygame.draw.rect(self.screen, (0, 0, 0), selected_rect, 2)

        # Update the display
        pygame.display.flip()

    def handle_menu_input(self):
        keys = pygame.key.get_pressed()

        # Handle menu navigation
        if keys[pygame.K_w]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif keys[pygame.K_s]:
            self.selected_option = (self.selected_option + 1) % len(self.options)

        # Adjust volume with A and D keys
        if self.selected_option == 1:
            if keys[pygame.K_a] and self.volume > 0:
                self.volume -= 0.01
            elif keys[pygame.K_d] and self.volume < 1:
                self.volume += 0.01
            pygame.mixer.music.set_volume(self.volume)

        self.draw_menu()

    def handle_mouse_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.volume_rect.collidepoint(event.pos):
                    self.dragging_slider = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging_slider = False
        elif event.type == pygame.MOUSEMOTION and self.dragging_slider:
            # Move volume slider with the mouse
            new_slider_x = event.pos[0] - volume_slider_rect.width // 2
            new_slider_x = max(self.width // 2 - 100, min(new_slider_x, self.width // 2 + 100 - volume_slider_rect.width))
            self.volume = (new_slider_x - (self.width // 2 - 100)) / (200 - volume_slider_rect.width)
            pygame.mixer.music.set_volume(self.volume)

        self.draw_menu()

    def run(self):
        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.selected_option == 0:
                            paused = False  # Resume the game
                        elif self.selected_option == 2:
                            pygame.quit()  # Quit the game
                if hasattr(event, 'pos'):  # Ensure the event has the 'pos' attribute
                    self.handle_mouse_input(event)  # Handle mouse input
            self.handle_menu_input()

            # Limit frames per second
            pygame.time.Clock().tick(60)
