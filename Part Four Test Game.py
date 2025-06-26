import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Bullet Hell - Stage Mode")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BG_COLOR = (10, 10, 30)

# Player
player_width, player_height = 60, 15
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - 60, player_width, player_height)
player_speed = 6
player_health = 5
player_bullets = []
player_bullet_speed = -8
can_shoot = False
last_shot_time = 0
SHOT_COOLDOWN = 150  # milliseconds

# Alien
alien_size = 100
alien = pygame.Rect(random.randint(0, WIDTH - alien_size), random.randint(0, HEIGHT - alien_size), alien_size, alien_size)
alien_speed = 3.0  # 2x faster in Stage 1
alien_vx, alien_vy = 0, 0  # Used in Stage 2
alien_bullets = []
alien_bullet_speed = 4
alien_health = 0

# Firing timers
alien_fire_timer = 0
ALIEN_FIRE_INTERVAL = 20  # 3 shots/sec at 60 FPS

# Stage / Timer
stage = 1
survival_time = 30
start_ticks = None  # Start after countdown

# Fonts
font = pygame.font.SysFont(None, 36)

# Game state
game_over = False
player_won = False

# Countdown
countdown_active = True
countdown_start_time = pygame.time.get_ticks()
countdown_duration = 3000  # 3 seconds

# Game loop

while True:
    background = pygame.image.load("cobble stone.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    girlfriend = pygame.image.load("3.png").convert_alpha()
    girlfriend = pygame.transform.scale(girlfriend, (alien_size, alien_size))

    player_bullet_img = pygame.image.load("projectile 1.png").convert_alpha()
    player_bullet_img = pygame.transform.scale(player_bullet_img, (150, 100))

    alien_bullet_img = pygame.image.load("projectile 1.png").convert_alpha()
    alien_bullet_img = pygame.transform.scale(alien_bullet_img, (150, 100))

    player_img = pygame.image.load("kyle (2).png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (75, 75))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_d] and player.right < WIDTH:
        player.x += player_speed
    if keys[pygame.K_w] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_s] and player.bottom < HEIGHT:
        player.y += player_speed

    current_time = pygame.time.get_ticks()

    # === Countdown Display ===
    if countdown_active:
        elapsed = current_time - countdown_start_time
        remaining = 3 - elapsed // 1000
        if elapsed < countdown_duration:
            if remaining > 0:
                countdown_text = font.render(str(remaining), True, WHITE)
            else:
                countdown_text = font.render("GO!", True, WHITE)
            screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2))
        else:
            countdown_active = False
            if stage == 1:
                start_ticks = pygame.time.get_ticks()
            elif stage == 2:
                # already set in transition
                pass

    elif not game_over:
        # === Player Shooting ===
        if can_shoot and keys[pygame.K_SPACE] and current_time - last_shot_time > SHOT_COOLDOWN:
            bullet = pygame.Rect(player.centerx - 4, player.top - 10, 8, 20)
            player_bullets.append(bullet)
            last_shot_time = current_time

        # === Move Alien ===
        if stage == 1:
            # Follow player
            dx = player.centerx - alien.centerx
            dy = player.centery - alien.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                vel_x = (dx / dist) * alien_speed
                vel_y = (dy / dist) * alien_speed
                alien.x += int(vel_x)
                alien.y += int(vel_y)
        elif stage == 2:
            # Bounce around
            alien.x += alien_vx
            alien.y += alien_vy

            if alien.left <= 0:
                alien.left = 0
                alien_vx *= -1
            elif alien.right >= WIDTH:
                alien.right = WIDTH
                alien_vx *= -1
            if alien.top <= 0:
                alien.top = 0
                alien_vy *= -1
            elif alien.bottom >= HEIGHT:
                alien.bottom = HEIGHT
                alien_vy *= -1

        # === Alien Fire ===
        alien_fire_timer += 1
        if alien_fire_timer >= ALIEN_FIRE_INTERVAL:
            alien_fire_timer = 0
            dx = player.centerx - alien.centerx
            dy = player.centery - alien.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                vel_x = (dx / dist) * alien_bullet_speed
                vel_y = (dy / dist) * alien_bullet_speed
                bullet = pygame.Rect(alien.centerx, alien.centery, 24, 24)
                alien_bullets.append({
                    "rect": bullet,
                    "vel": (vel_x, vel_y)
                })

        # === Move Alien Bullets ===
        for bullet in alien_bullets[:]:
            bullet["rect"].x += bullet["vel"][0]
            bullet["rect"].y += bullet["vel"][1]
            if not screen.get_rect().colliderect(bullet["rect"]):
                alien_bullets.remove(bullet)
            elif bullet["rect"].colliderect(player):
                alien_bullets.remove(bullet)
                player_health -= 1
                if player_health <= 0:
                    game_over = True
                    player_won = False

        # === Move Player Bullets ===
        for bullet in player_bullets[:]:
            bullet.y += player_bullet_speed
            if bullet.bottom < 0:
                player_bullets.remove(bullet)
            elif bullet.colliderect(alien) and stage == 2:
                alien_health -= 1
                player_bullets.remove(bullet)
                if alien_health <= 0:
                    game_over = True
                    player_won = True

        # === Stage Transition ===
        if stage == 1:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds >= survival_time:
                stage = 2
                countdown_active = True
                countdown_start_time = pygame.time.get_ticks()
                can_shoot = True
                alien_health = 20
                alien_vx = 4.5  # Bounce speed
                alien_vy = 4.5
                ALIEN_FIRE_INTERVAL = 13

        # === Draw ===
        screen.blit(girlfriend, alien.topleft)
        for bullet in alien_bullets:
            screen.blit(alien_bullet_img, bullet["rect"].topleft)
        for bullet in player_bullets:
            screen.blit(player_bullet_img, bullet.topleft)
        screen.blit(player_img, player.topleft)

        # UI
        health_text = font.render(f"Health: {player_health}", True, WHITE)
        screen.blit(health_text, (10, 10))
        if stage == 1 and start_ticks:
            time_left = max(0, int(survival_time - (pygame.time.get_ticks() - start_ticks) / 1000))
            timer_text = font.render(f"Survive: {time_left}s", True, WHITE)
            screen.blit(timer_text, (10, 40))
        elif stage == 2:
            alien_hp_text = font.render(f"Alien HP: {alien_health}", True, WHITE)
            screen.blit(alien_hp_text, (10, 40))

    elif game_over:
        # msg = "You Survived and Won!" if player_won else "You were Defeated!"

        if player_won: 
            msg = "You Survived and Won!" 
            msg_surface = font.render(msg, True, WHITE)
            screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT // 2))

        else:
            msg = "You were Defeated!"
            msg_surface = font.render(msg, True, WHITE)
            screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)
