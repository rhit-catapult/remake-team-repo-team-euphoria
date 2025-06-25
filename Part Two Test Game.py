import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Part Two Test Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GRAY = (180, 180, 180)

# Game states
AREA1, AREA2, CUTSCENE = "area1", "area2", "cutscene"
game_state = AREA1

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

# Instantiate Kyle in Area 1 (spawn near left-bottom)
kyle = Kyle(80, HEIGHT - 80)

# Borders for Area 1
border_top_1 = pygame.Rect(0, 0, WIDTH, 10)
border_left_1 = pygame.Rect(0, 0, 10, HEIGHT)
border_bottom_1 = pygame.Rect(0, HEIGHT - 10, WIDTH, 10)

# Borders for Area 2
border_right_2 = pygame.Rect(WIDTH - 10, 0, 10, HEIGHT)
border_bottom_2 = pygame.Rect(0, HEIGHT - 10, WIDTH, 10)
border_top_2 = pygame.Rect(0, 300, WIDTH, 10)

# Door hitbox in Area 2 (centered on the 300px border)
door_width, door_height = 60, 10
door_x = WIDTH // 2 - door_width // 2
door_y = 300 - door_height

door_hitbox = pygame.Rect(door_x, door_y, door_width, door_height)

# Button for cutscene
font = pygame.font.SysFont(None, 30)
def draw_enter_house_button():
    btn_width, btn_height = 200, 50
    btn_rect = pygame.Rect(WIDTH//2 - btn_width//2, HEIGHT - btn_height - 20, btn_width, btn_height)
    pygame.draw.rect(screen, GRAY, btn_rect)
    text_surf = font.render("Enter the house", True, BLACK)
    text_rect = text_surf.get_rect(center=btn_rect.center)
    screen.blit(text_surf, text_rect)
    return btn_rect

# Main loop
running = True
show_cutscene_button = False
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and show_cutscene_button and game_state == AREA2:
            if enter_house_btn_rect.collidepoint(event.pos):
                game_state = CUTSCENE

    if game_state == AREA1:
        kyle.move(keys)
        # Area 1 borders
        if kyle.rect.left < border_left_1.right:
            kyle.rect.left = border_left_1.right
        if kyle.rect.top < border_top_1.bottom:
            kyle.rect.top = border_top_1.bottom
        if kyle.rect.bottom > border_bottom_1.top:
            kyle.rect.bottom = border_bottom_1.top
        # Transition to Area 2 (right edge)
        if kyle.rect.right >= WIDTH:
            game_state = AREA2
            kyle.rect.left = 10  # Enter Area 2 from left
    elif game_state == AREA2:
        kyle.move(keys)
        # Area 2 borders
        if kyle.rect.right > border_right_2.left:
            kyle.rect.right = border_right_2.left
        if kyle.rect.bottom > border_bottom_2.top:
            kyle.rect.bottom = border_bottom_2.top
        if kyle.rect.top < border_top_2.bottom:
            # Only block if not in the door area
            if not kyle.rect.colliderect(door_hitbox.inflate(10, 10)):
                kyle.rect.top = border_top_2.bottom
        # Transition back to Area 1 (left edge)
        if kyle.rect.left < 0:
            game_state = AREA1
            kyle.rect.right = WIDTH - 10
    screen.fill(WHITE)
    if game_state == AREA1:
        # Draw Area 1 borders
        pygame.draw.rect(screen, BLACK, border_top_1)
        pygame.draw.rect(screen, BLACK, border_left_1)
        pygame.draw.rect(screen, BLACK, border_bottom_1)
    elif game_state == AREA2:
        # Draw Area 2 borders
        pygame.draw.rect(screen, BLACK, border_right_2)
        pygame.draw.rect(screen, BLACK, border_bottom_2)
        pygame.draw.rect(screen, BLACK, border_top_2)
        # Draw door
        pygame.draw.rect(screen, (200, 100, 0), door_hitbox)
        # Show 'Enter the house' button if Kyle is within 20px of the door
        if kyle.rect.colliderect(door_hitbox.inflate(20, 20)):
            print('Kyle is within 20px of the door!')  # DEBUG
            show_cutscene_button = True
            enter_house_btn_rect = draw_enter_house_button()
        else:
            show_cutscene_button = False
    if game_state == CUTSCENE:
        screen.fill((220, 220, 220))
        # TODO: Place your cutscene logic here
        text = font.render("Cutscene goes here!", True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
    # Draw Kyle
    if game_state != CUTSCENE:
        screen.blit(kyle.image, kyle.rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
