import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Bullet Hell - Stage Mode")

clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 28)

# Load backgrounds and audio


# Background music

pygame.mixer.music.set_volume(0.5)

# Game state
game_over = False
player_won = False
show_end_scene = False
end_alpha = 0
end_fade_start = 0
end_music_played = False

# Player setup
player_width, player_height = 60, 15
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - 60, player_width, player_height)
player_speed = 7.5
player_health = 6
player_bullets = []
player_bullet_speed = -8
can_shoot = False
last_shot_time = 0
SHOT_COOLDOWN = 150

# Alien setup
alien_size = 100
alien = pygame.Rect(random.randint(0, WIDTH - alien_size), 50, alien_size, alien_size)
alien_speed = 4
alien_vx, alien_vy = 0, 0
alien_bullets = []
alien_bullet_speed = 4
alien_health = 0

# Timers and stages
alien_fire_timer = 0
ALIEN_FIRE_INTERVAL = 20
stage = 1
survival_time = 30
start_ticks = None

# Dialogue and fade-in
fade_in = True
fade_alpha = 255
dialog_after_fade = False
dialog_index = 0
intro_dialog = [
    "Kyle: Ugh, what happened?",
    "Claudia: Hey?! Why are you awake?",
    "Claudia: I guess I didn’t put enough drugs in that drink.",
    "Kyle: WHAT?! YOU DRUGGED ME?!",
    "Kyle: WHY WOULD YOU DO THIS?!",
    "Claudia: You’re lonely and no one will remember you.",
    "Claudia: Your skin is perfect and I need it for my collection.",
    "Claudia: Enough talking, time to die.",
    "Kyle: AHHHH! GET AWAY!"
]
transition_dialog = [
    "*Kyle finds and picks a knife up off the ground",
    "Claudia: LET ME CUT OFF YOUR SKIN!"
]
show_transition_dialog = False
transition_index = 0
ok_button = pygame.Rect(WIDTH // 2 + 200, HEIGHT - 100, 100, 40)

def draw_text(surface, text, rect, font, color):
    words = text.split(' ')
    line = ''
    lines = []
    for word in words:
        test_line = f"{line} {word}".strip()
        if font.size(test_line)[0] < rect.width - 20:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)
    for i, l in enumerate(lines):
        surface.blit(font.render(l, True, color), (rect.x + 10, rect.y + 10 + i * 30))

# MAIN GAME LOOP
while True:
    background = pygame.image.load("cobble stone.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    girlfriend = pygame.image.load("3.png").convert_alpha()
    girlfriend = pygame.transform.scale(girlfriend, (alien_size, alien_size))
    player_img = pygame.image.load("kyle (2).png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (75, 75))
    player_bullet_img = pygame.image.load("projectile 1.png").convert_alpha()
    player_bullet_img = pygame.transform.scale(player_bullet_img, (150, 100))
    alien_bullet_img = pygame.image.load("projectile 1.png").convert_alpha()
    alien_bullet_img = pygame.transform.scale(alien_bullet_img, (150, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if dialog_after_fade and ok_button.collidepoint(mouse_pos):
                dialog_index += 1
                if dialog_index >= len(intro_dialog):
                    dialog_after_fade = False
                    start_ticks = pygame.time.get_ticks()
            elif show_transition_dialog and ok_button.collidepoint(mouse_pos):
                transition_index += 1
                if transition_index >= len(transition_dialog):
                    show_transition_dialog = False
                    stage = 2
                    alien.x, alien.y = WIDTH // 2 - alien_size // 2, 50
                    alien_health = 20
                    alien_vx, alien_vy = 4.5, 4.5
                    ALIEN_FIRE_INTERVAL = 13
                    can_shoot = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_d] and player.right < WIDTH:
        player.x += player_speed
    if keys[pygame.K_w] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_s] and player.bottom < HEIGHT - player_height:
        player.y += player_speed

    current_time = pygame.time.get_ticks()

    if fade_in:
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(int(fade_alpha))
        screen.blit(fade_surface, (0, 0))
        if fade_alpha > 0:
            fade_alpha -= 255 / (FPS * 5)
        else:
            fade_in = False
            dialog_after_fade = True


    elif dialog_after_fade or show_transition_dialog:
        box_rect = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 100)
        pygame.draw.rect(screen, WHITE, box_rect)
        pygame.draw.rect(screen, BLACK, box_rect, 4)
        if dialog_after_fade:
            draw_text(screen, intro_dialog[dialog_index], box_rect, font, BLACK)
        else:
            draw_text(screen, transition_dialog[transition_index], box_rect, font, BLACK)
        pygame.draw.rect(screen, GREEN, ok_button)
        pygame.draw.rect(screen, BLACK, ok_button, 2)
        screen.blit(font.render("OK", True, BLACK), (ok_button.centerx - 20, ok_button.centery - 12))

    elif not game_over:
        if stage == 1:
            dx = player.centerx - alien.centerx
            dy = player.centery - alien.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                alien.x += int((dx / dist) * alien_speed)
                alien.y += int((dy / dist) * alien_speed)
        elif stage == 2:
            alien.x += alien_vx
            alien.y += alien_vy
            if alien.left <= 0 or alien.right >= WIDTH:
                alien_vx *= -1
            if alien.top <= 0:
                alien.top = 0
                alien_vy *= -1
            if alien.bottom >= HEIGHT - 100:  # Claudia stays above the ground
                alien.bottom = HEIGHT - 100
                alien_vy *= -1

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
                alien_bullets.append({"rect": bullet, "vel": (vel_x, vel_y)})

        for bullet in alien_bullets[:]:
            bullet["rect"].x += bullet["vel"][0]
