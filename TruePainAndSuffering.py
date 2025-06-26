import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Fight - Dog Arena")

clock = pygame.time.Clock()
FPS = 60

# Load images
player_img = pygame.transform.scale(pygame.image.load("kyle (2).png"), (60, 60))
dog_img = pygame.transform.scale(pygame.image.load("Dog_Boss.png"), (120, 120))
bullet_img = pygame.transform.scale(pygame.image.load("projectile 1.png"), (12, 24))

# Game state
game_state = "boss"  # You'd switch to this when entering from the RIGHT scene

# Player
player = pygame.Rect(WIDTH // 2 - 30, HEIGHT - 80, 60, 60)
player_speed = 5
player_health = 5
player_bullets = []
player_bullet_speed = -7
can_shoot = True

# Boss
boss = pygame.Rect(WIDTH // 2 - 60, 100, 120, 120)
boss_health = 30
boss_speed = 2
boss_bullets = []
boss_bullet_speed = 5
boss_fire_timer = 0
BOSS_FIRE_INTERVAL = 60  # Shoot every second

font = pygame.font.SysFont(None, 36)
game_over = False
player_won = False

while True:
    screen.fill((30, 0, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == "boss" and not game_over:
        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_d] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_SPACE] and can_shoot and len(player_bullets) < 1:
            bullet = pygame.Rect(player.centerx - 6, player.top - 20, 12, 24)
            player_bullets.append(bullet)

        # Boss AI (move left and right)
        boss.x += boss_speed
        if boss.left <= 0 or boss.right >= WIDTH:
            boss_speed *= -1

        # Boss firing
        boss_fire_timer += 1
        if boss_fire_timer >= BOSS_FIRE_INTERVAL:
            boss_fire_timer = 0
            dx = player.centerx - boss.centerx
            dy = player.centery - boss.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                vx = dx / dist * boss_bullet_speed
                vy = dy / dist * boss_bullet_speed
                bullet = pygame.Rect(boss.centerx - 12, boss.bottom, 24, 24)
                boss_bullets.append({"rect": bullet, "vel": (vx, vy)})

        # Move boss bullets
        for bullet in boss_bullets[:]:
            bullet["rect"].x += bullet["vel"][0]
            bullet["rect"].y += bullet["vel"][1]
            if not screen.get_rect().colliderect(bullet["rect"]):
                boss_bullets.remove(bullet)
            elif bullet["rect"].colliderect(player):
                boss_bullets.remove(bullet)
                player_health -= 1
                if player_health <= 0:
                    game_over = True
                    player_won = False

        # Move player bullets
        for bullet in player_bullets[:]:
            bullet.y += player_bullet_speed
            if bullet.bottom < 0:
                player_bullets.remove(bullet)
            elif bullet.colliderect(boss):
                boss_health -= 1
                player_bullets.remove(bullet)
                if boss_health <= 0:
                    game_over = True
                    player_won = True

        # Draw
        screen.blit(dog_img, boss.topleft)
        for bullet in boss_bullets:
            screen.blit(bullet_img, bullet["rect"].topleft)
        for bullet in player_bullets:
            screen.blit(bullet_img, bullet.topleft)
        screen.blit(player_img, player.topleft)

        # UI
        hp_text = font.render(f"Health: {player_health}", True, (255, 255, 255))
        screen.blit(hp_text, (10, 10))
        boss_hp_text = font.render(f"Boss HP: {boss_health}", True, (255, 100, 100))
        screen.blit(boss_hp_text, (10, 40))

    elif game_over:
        msg = "You defeated the Dog Boss!" if player_won else "You were defeated..."
        msg_surface = font.render(msg, True, (255, 255, 255))
        screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)