

import pygame
import sys



# Screen size & colors
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dating Sim Prototype")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

FONT = pygame.font.SysFont(None, 30)
BIGFONT = pygame.font.SysFont(None, 50)

clock = pygame.time.Clock()

# Game States
TITLE = "title"
TITLE2 = "title2"  # Added missing TITLE2
CENTER = "center"
LEFT = "left"
RIGHT = "right"
HOUSE = "house"
STREET1 = "street1"
STREET2 = "street2"

# Define Kyle sprite class
class Kyle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
