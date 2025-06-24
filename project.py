import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader - Single Bouncer")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player
player_img = pygame.Surface((50, 30))
player_img.fill(WHITE)
player_x = WIDTH // 2
player_y = HEIGHT - 50
player_speed = 5

# Bullet
bullet_img = pygame.Surface((5, 10))
bullet_img.fill(RED)
bullets = []
bullet_speed = -7

# Alien
alien_img = pygame.Surface((60, 40))
alien_img.fill((0, 255, 0))
alien_x = random.randint(100, WIDTH - 100)
alien_y = 50
alien_dx = 4
alien_dy = 2
alien_hitpoints = 20
font = pygame.font.SysFont(None, 36)

running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    # --- Handle Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Handle Input ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:  # Limit number of bullets
            bullets.append([player_x + 22, player_y])

    # --- Update Bullets ---
    for bullet in bullets[:]:
        bullet[1] += bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # --- Move Alien ---
    alien_x += alien_dx
    alien_y += alien_dy

    # Bounce off walls
    if alien_x <= 0 or alien_x >= WIDTH - 60:
        alien_dx *= -1
    if alien_y <= 0 or alien_y >= HEIGHT // 2:
        alien_dy *= -1

    # --- Collision Detection ---
    alien_rect = pygame.Rect(alien_x, alien_y, 60, 40)
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
        if alien_rect.colliderect(bullet_rect):
            bullets.remove(bullet)
            alien_hitpoints -= 1

    # --- Draw Everything ---
    screen.blit(player_img, (player_x, player_y))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))
    if alien_hitpoints > 0:
        screen.blit(alien_img, (alien_x, alien_y))
    else:
        win_text = font.render("You defeated the alien!", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))

    # Draw HP
    hp_text = font.render(f"Alien HP: {alien_hitpoints}", True, WHITE)
    screen.blit(hp_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()