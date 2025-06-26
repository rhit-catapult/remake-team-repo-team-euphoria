import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Part Three Test Game")
clock = pygame.time.Clock()


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (100, 200, 255)

# Font
font = pygame.font.SysFont(None, 32)
# Define the pop-up area (centered, smaller than the window)
AREA_WIDTH, AREA_HEIGHT = 500, 400
AREA_X, AREA_Y = (WIDTH - AREA_WIDTH) // 2, (HEIGHT - AREA_HEIGHT) // 2
area_rect = pygame.Rect(0, 0, 800, 600)

# Kyle sprite
class Kyle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("kyle (2).png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        # Clamp Kyle inside the pop-up area (edges are hitboxes)
        if self.rect.left < area_rect.left:
            self.rect.left = area_rect.left
        if self.rect.right > area_rect.right:
            self.rect.right = area_rect.right
        if self.rect.top < area_rect.top:
            self.rect.top = area_rect.top
        if self.rect.bottom > area_rect.bottom:
            self.rect.bottom = area_rect.bottom

# Claudia sprite (3.png)
class Claudia(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("3.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 80))
        self.rect = self.image.get_rect(center=(x, y))

# Instantiate Kyle at the bottom center of the area
kyle = Kyle(AREA_X + AREA_WIDTH // 2, AREA_Y + AREA_HEIGHT - 40)
# Instantiate Claudia at the center of the area
claudia = Claudia(AREA_X + AREA_WIDTH // 2, AREA_Y + AREA_HEIGHT // 2)

# Game state
STATE_PLAY = "play"
STATE_CUTSCENE = "cutscene"
game_state = STATE_PLAY

# Button logic
def draw_talk_button():
    btn_width, btn_height = 220, 60
    btn_rect = pygame.Rect(WIDTH//2 - btn_width//2, HEIGHT - 80, btn_width, btn_height)
    pygame.draw.rect(screen, GRAY, btn_rect)
    pygame.draw.rect(screen, BLACK, btn_rect, 3)
    text_surf = font.render("Talk to Claudia", True, BLACK)
    text_rect = text_surf.get_rect(center=btn_rect.center)
    screen.blit(text_surf, text_rect)
    return btn_rect

# Main loop
running = True
show_talk_button = False
btn_rect = pygame.Rect(0, 0, 0, 0)
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and show_talk_button and game_state == STATE_PLAY:
            if btn_rect.collidepoint(event.pos):
                game_state = STATE_CUTSCENE

    if game_state == STATE_PLAY:
        kyle.move(keys)

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, area_rect)
    screen.blit(claudia.image, claudia.rect)
    screen.blit(kyle.image, kyle.rect)

    show_talk_button = False
    btn_rect = pygame.Rect(0, 0, 0, 0)
    if game_state == STATE_PLAY:
        # Check distance between Kyle and Claudia
        dx = kyle.rect.centerx - claudia.rect.centerx
        dy = kyle.rect.centery - claudia.rect.centery
        distance = (dx**2 + dy**2) ** 0.5
        if distance <= 30:
            show_talk_button = True
            btn_rect = draw_talk_button()
    elif game_state == STATE_CUTSCENE:
        # Show cutscene
        cutscene_text = font.render("Cutscene: Talking to Claudia...", True, BLACK)
        screen.blit(cutscene_text, (WIDTH//2 - cutscene_text.get_width()//2, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()


