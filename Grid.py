import pygame
import sys


#Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Part Three Test Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GRAY = (180, 180, 180)
FURNITURE_PANEL_WIDTH = 40


def draw_grid(screen) -> None:
    pixel_gap = 20
    num_horizontal_lines = HEIGHT // pixel_gap + 1  # an extra just in case
    num_vertical_lines = (WIDTH - FURNITURE_PANEL_WIDTH) // pixel_gap + 1
    for i in range(0, num_horizontal_lines):
        pygame.draw.line(screen, (225, 225, 225), (FURNITURE_PANEL_WIDTH, i * pixel_gap),
                         (WIDTH, i * pixel_gap))
    for i in range(0, num_vertical_lines):
        pygame.draw.line(screen, (225, 225, 225), (FURNITURE_PANEL_WIDTH + i * pixel_gap, 0),
                         (FURNITURE_PANEL_WIDTH + i * pixel_gap, HEIGHT))


    #Main loop
running = True
show_cutscene_button = False
enter_house_btn_rect = pygame.Rect(0, 0, 0, 0)  # Always define the button rect
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GRAY)
    draw_grid(screen)
    pygame.display.update()
    clock.tick(60)