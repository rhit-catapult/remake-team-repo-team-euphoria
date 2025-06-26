import pygame
import sys

# Initialize Pygame
pygame.init()

# Initialize mixer for music
pygame.mixer.init()

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
<<<<<<< HEAD
TITLE, AREA1, AREA2, CUTSCENE = "title", "area1", "area2", "cutscene"
game_state = TITLE

=======
AREA1, AREA2, CUTSCENE = "area1", "area2", "cutscene"
game_state = AREA1
area1 = pygame.transform.scale(pygame.image.load("Road to the house.png"), (WIDTH, HEIGHT))
area2 = pygame.transform.scale(pygame.image.load("GH new.png"), (WIDTH, HEIGHT))
<<<<<<< Updated upstream
=======
>>>>>>> 4a1087656a71021f4bc288784e96f3c13a4788cf
>>>>>>> Stashed changes
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
door_y = 300 - door_height - 2  # Place the door just above the border
door_hitbox = pygame.Rect(door_x, door_y, door_width, door_height)

# Button for cutscene
font = pygame.font.SysFont(None, 30)
def draw_enter_house_button():
    # Place the button at the bottom of the screen
    btn_width, btn_height = 220, 60
    btn_rect = pygame.Rect(WIDTH//2 - btn_width//2, HEIGHT - 80, btn_width, btn_height)
    pygame.draw.rect(screen, GRAY, btn_rect)
    pygame.draw.rect(screen, BLACK, btn_rect, 3)  # Optional: add border for visibility
    text_surf = font.render("Enter the house", True, BLACK)
    text_rect = text_surf.get_rect(center=btn_rect.center)
    screen.blit(text_surf, text_rect)
    return btn_rect

# Main loop
running = True
show_cutscene_button = False
enter_house_btn_rect = pygame.Rect(0, 0, 0, 0)  # Always define the button rect
music_playing = False
while running:
    pygame.display.update()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and show_cutscene_button and game_state == AREA2:
            if enter_house_btn_rect.collidepoint(event.pos):
                game_state = CUTSCENE
        # If on title screen, pressing any key or mouse click starts the game
        if game_state == TITLE and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            game_state = AREA1
            if music_playing:
                pygame.mixer.music.stop()
                music_playing = False

    if game_state == TITLE:
        if not music_playing:
            pygame.mixer.music.load('Renai Circulation恋愛サーキュレーション歌ってみたなみりん.mp3')
            pygame.mixer.music.play(-1)
            music_playing = True
        # Draw your title screen here
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 60)
        title_text = font.render("Part Two Test Game", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 60))
        font_small = pygame.font.SysFont(None, 30)
        prompt_text = font_small.render("Press any key to start", True, (0, 0, 0))
        screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2 + 20))
        pygame.display.flip()
        clock.tick(60)
        continue
    else:
        if music_playing:
            pygame.mixer.music.stop()
            music_playing = False

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
    if game_state == AREA1:
        screen.blit(area1, (0, 0))
    elif game_state == AREA2:
        screen.blit(area2, (0, 0))
    elif game_state == CUTSCENE:
        screen.fill((220, 220, 220))
    if game_state == AREA1:
        pass  # No borders or extra drawing in AREA1
    elif game_state == AREA2:
        # Draw door
        pygame.draw.rect(screen, (200, 100, 0), door_hitbox)
        # Show 'Enter the house' button if Kyle is within 10px of the door
        if kyle.rect.colliderect(door_hitbox.inflate(30, 30)):
            show_cutscene_button = True
            enter_house_btn_rect = draw_enter_house_button()
        else:
            show_cutscene_button = False
            enter_house_btn_rect = pygame.Rect(0, 0, 0, 0)  # Reset when not in zone
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
