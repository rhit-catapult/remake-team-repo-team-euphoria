from symtable import Class

import pygame
import sys

import pygame

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Sprite")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Sprite class
class Kyle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Sprite size
        self.image.fill(BLUE)                  # Sprite color
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BORDER_WIDTH = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hitbox Border Game")

#Sprite class


# Player settings
player_size = 40
player_color = BLUE
player_speed = 5

# Player spawn at bottom-right
player_rect = pygame.Rect(
    SCREEN_WIDTH - BORDER_WIDTH - player_size,
    SCREEN_HEIGHT - BORDER_WIDTH - player_size,
    player_size,
    player_size
)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw borders
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, BORDER_WIDTH))  # Top
    pygame.draw.rect(screen, BLACK, (0, 0, BORDER_WIDTH, SCREEN_HEIGHT))  # Left
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - BORDER_WIDTH, SCREEN_WIDTH, BORDER_WIDTH))  # Bottom
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, SCREEN_HEIGHT))  # Right

    # Draw player
    pygame.draw.rect(screen, player_color, player_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling
    # Key press handling (WASD)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Left
        player_rect.x -= player_speed
    if keys[pygame.K_d]:  # Right
        player_rect.x += player_speed
    if keys[pygame.K_w]:  # Up
        player_rect.y -= player_speed
    if keys[pygame.K_s]:  # Down
        player_rect.y += player_speed

    # Collision with borders
    player_rect.left = max(player_rect.left, BORDER_WIDTH)
    player_rect.right = min(player_rect.right, SCREEN_WIDTH - BORDER_WIDTH)
    player_rect.top = max(player_rect.top, BORDER_WIDTH)
    player_rect.bottom = min(player_rect.bottom, SCREEN_HEIGHT - BORDER_WIDTH)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
