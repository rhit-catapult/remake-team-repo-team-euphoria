import pygame
import sys
import random
import math

pygame.init()

# Initialize mixer for music
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Complete Dating Sim Adventure")
clock = pygame.time.Clock()
FPS = 60

# ===== GAME STATES =====
# Part 1 states
TITLE, CENTER, LEFT, RIGHT, HOUSE, CUTSCENE1 = "title", "center", "left", "right", "house", "cutscene1"

# Part 2 states  
AREA1, AREA2, CUTSCENE2 = "area1", "area2", "cutscene2"

# Part 3 states
PART3_PLAY, PART3_CUTSCENE, PART3_DIALOG = "part3_play", "part3_cutscene", "part3_dialog"

# Part 4 states
PART4_GAME, PART4_OVER = "part4_game", "part4_over"

game_state = TITLE

# ===== COLORS =====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (0, 0, 255)
DARK_GRAY = (80, 80, 80)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BG_COLOR = (10, 10, 30)

# ===== PART 1 ASSETS =====
bg_title = pygame.transform.scale(pygame.image.load("Title Screen 1.png"), (WIDTH, HEIGHT))
bg_center = pygame.transform.scale(pygame.image.load("kyle_house.png"), (WIDTH, HEIGHT))
bg_house = pygame.transform.scale(pygame.image.load("KH_new.png"), (WIDTH, HEIGHT))
bg_left = pygame.transform.scale(pygame.image.load("left field.png"), (WIDTH, HEIGHT))
bg_right = pygame.transform.scale(pygame.image.load("cobble stone.png"), (WIDTH, HEIGHT))

# ===== PART 2 ASSETS =====
area1_bg = pygame.transform.scale(pygame.image.load("Road to the house.png"), (WIDTH, HEIGHT))
area2_bg = pygame.transform.scale(pygame.image.load("GH new.png"), (WIDTH, HEIGHT))

# ===== PART 3 ASSETS =====
part3_bg = pygame.transform.scale(pygame.image.load("Living_Room.png"), (WIDTH, HEIGHT))
bg1 = pygame.transform.scale(pygame.image.load("Living_Room.png"), (WIDTH, HEIGHT))
bg2 = pygame.transform.scale(pygame.image.load("dindin room.jpg"), (WIDTH, HEIGHT))

# ===== PART 4 ASSETS =====
part4_bg = pygame.transform.scale(pygame.image.load("cobble stone.png"), (WIDTH, HEIGHT))

# ===== KYLE CLASS (FROM PART 1) =====
class Kyle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = {
            "up": pygame.image.load("kyle_back.png").convert_alpha(),
            "down": pygame.image.load("kyle (2).png").convert_alpha(),
            "left": pygame.image.load("kyle_left.png").convert_alpha(),
            "right": pygame.image.load("kyle_right.png").convert_alpha()
        }
        for key in self.sprites:
            self.sprites[key] = pygame.transform.scale(self.sprites[key], (40, 60))
        self.facing = "down"
        self.image = self.sprites[self.facing]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.facing = "up"
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.facing = "down"
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing = "left"
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing = "right"
        self.image = self.sprites[self.facing]

# ===== CLAUDIA CLASS (FROM PART 3) =====
class Claudia(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("3.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 80))
        self.rect = self.image.get_rect(center=(x, y))

# ===== BUTTON CLASS =====
class Button:
    def __init__(self, text, rect, action):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.action = action
        self.font = pygame.font.SysFont(None, 30)
        self.color = GRAY

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ===== INSTANTIATE CHARACTERS =====
kyle = Kyle(WIDTH // 2, HEIGHT // 2)
claudia = Claudia(WIDTH // 2, HEIGHT // 2)

# ===== PART 1 BUTTONS =====
start_button = Button("Play", (WIDTH//2 - 60, HEIGHT - 80, 120, 40), lambda: change_scene(CENTER))
enter_house_button = Button("Enter Your House", (WIDTH//2 - 100, HEIGHT - 40, 200, 30), lambda: change_scene(HOUSE))
leave_house_button = Button("Leave the House", (WIDTH//2 - 100, HEIGHT - 40, 200, 30), lambda: change_scene(CENTER))
drive_button = Button("Drive", (WIDTH//2 - 60, HEIGHT - 40, 120, 30), lambda: None)

# ===== PART 1 HITBOXES =====
wall_top = pygame.Rect(0, 0, WIDTH, 20)
wall_bottom = pygame.Rect(0, HEIGHT - 10, WIDTH, 10)
wall_left = pygame.Rect(0, 0, 10, HEIGHT)
wall_right = pygame.Rect(WIDTH - 10, 0, 10, HEIGHT)

# House hitboxes (center scene)
house_area = pygame.Rect(WIDTH // 2 - 100, 30, 200, 150)
house_door = pygame.Rect(WIDTH // 2 - 20, 170, 40, 10)
house_walls = [
    pygame.Rect(house_area.left, house_area.top, house_area.width, 10),
    pygame.Rect(house_area.left, house_area.top, 10, house_area.height),
    pygame.Rect(house_area.right - 10, house_area.top, 10, house_area.height),
    pygame.Rect(house_area.left, house_area.bottom - 10, house_area.width, 10),
]
house_exit = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 30, 40, 20)

# Car hitbox (in CENTER scene)
car_box = pygame.Rect(WIDTH - 100, HEIGHT - 100, 80, 60)

# ===== PART 2 HITBOXES =====
border_top_1 = pygame.Rect(0, 0, WIDTH, 10)
border_left_1 = pygame.Rect(0, 0, 10, HEIGHT)
border_bottom_1 = pygame.Rect(0, HEIGHT - 10, WIDTH, 10)
border_right_2 = pygame.Rect(WIDTH - 10, 0, 10, HEIGHT)
border_bottom_2 = pygame.Rect(0, HEIGHT - 10, WIDTH, 10)
border_top_2 = pygame.Rect(0, 320, WIDTH, 10)
door_width, door_height = 60, 10
door_x = WIDTH // 2 - door_width // 2
door_y = 320 - door_height - 2
door_hitbox = pygame.Rect(door_x, door_y, door_width, door_height)

# ===== PART 4 VARIABLES =====
# Player
player_width, player_height = 60, 15
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - 60, player_width, player_height)
player_speed = 6
player_health = 6
player_bullets = []
player_bullet_speed = -8
can_shoot = False
last_shot_time = 0
SHOT_COOLDOWN = 150

# Alien
alien_size = 100
alien = pygame.Rect(random.randint(0, WIDTH - alien_size), random.randint(0, HEIGHT - alien_size), alien_size, alien_size)
alien_speed = 3.0
alien_vx, alien_vy = 0, 0
alien_bullets = []
alien_bullet_speed = 4
alien_health = 0

# Firing timers
alien_fire_timer = 0
ALIEN_FIRE_INTERVAL = 20

# Stage / Timer
stage = 1
survival_time = 30
start_ticks = None

# Game state
game_over = False
player_won = False

# Countdown
countdown_active = True
countdown_start_time = pygame.time.get_ticks()
countdown_duration = 3000

# ===== GLOBAL VARIABLES =====
music_playing = False
font = pygame.font.SysFont(None, 30)
next_btn_rect = pygame.Rect(0, 0, 0, 0)
show_next_button = False
show_cutscene_button = False
enter_house_btn_rect = pygame.Rect(0, 0, 0, 0)
show_talk_button = False
talk_btn_rect = pygame.Rect(0, 0, 0, 0)

# ===== PART 4 ASSETS =====
girlfriend = pygame.transform.scale(pygame.image.load("3.png").convert_alpha(), (alien_size, alien_size))
player_bullet_img = pygame.transform.scale(pygame.image.load("projectile 1.png").convert_alpha(), (150, 100))
alien_bullet_img = pygame.transform.scale(pygame.image.load("projectile 1.png").convert_alpha(), (150, 100))
player_img = pygame.transform.scale(pygame.image.load("kyle (2).png").convert_alpha(), (75, 75))

# ===== PART 3 DIALOG SYSTEM =====
# Textbox setup
TEXTBOX_HEIGHT = 150
textbox_rect = pygame.Rect(50, HEIGHT - TEXTBOX_HEIGHT - 30, WIDTH - 100, TEXTBOX_HEIGHT)
TEXTBOX_COLOR = (240, 240, 240)

# All 25 messages
messages = [
    "Claudia: WOWIE ZOWIE IT IS SOOOOOO NICE TO FINALLY SEE YOU!! *hugs Kyle weirdly tight* AND FEEL YOU!!",
    "Kyle: Um *gently pushes Claudia away and backs up* Yeah, it's nice to meet you too",
    "Claudia: Anything for you Kyle, you're perfect",
    "Kyle: Um… Ok",
    "Kyle: So is it fine if we talk to each other about ourselves because I didn't really get to re-",
    "Claudia: NO! Um I mean no, we have to eat dinner first. You must be very hungry.",
    "Kyle: Ok that works I guess",
    "(They both head to the dining room where there is a massive amount of food)",
    "Kyle: Oh this looks wonderful! You must be rich or something",
    "Claudia: Yeah… you could say I receive a lot of money from my job",
    "Kyle: If I may ask, what is your Job?",
    "Claudia: Um…*stammers* Oh! I work in a butcher shop and take the hides off of the produce",
    "Kyle: Oh.. That's interesting *in his head*- good thing she makes a lot of money. That's what I need",
    "Claudia: Well anyway, let's sit down",
    "(They sit down)",
    "Claudia: First, let's make a Toast",
    "Kyle: Sure. To who?",
    "Claudia: You silly!",
    "Kyle: Ok, sure. *in his head again*-Good thing she is into me this good. I won't even have to do anything in this relationship at this rate!",
    "Claudia: *pours a bottle of champagne for them both* -Ahem. I do this Toast to Kyle Thompson, the perfect person, with the perfect skin, face and hair. I honor that he will make for a fine piece to my collection.",
    "Kyle: That was a bit odd, but ok.",
    "Claudia: Well, let's drink up",
    "Kyle: Ok",
    "(They both drink the champagne)",
    "(Claudia stares at Kyle rather than sipping her champagne, and he looks back to her grinning right at him)",
    "(Confused, he tries to ask Claudia what she is looking at him for but instantly get hit with a wave of nausea and passes out moments later)"
]

current_message = 0

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines

# ===== SCENE TRANSITION FUNCTION =====
def change_scene(scene):
    global game_state
    game_state = scene
    if scene == CENTER:
        kyle.rect.center = (WIDTH // 2, HEIGHT // 2)
    elif scene == LEFT:
        kyle.rect.center = (WIDTH - 60, HEIGHT // 2)
    elif scene == RIGHT:
        kyle.rect.center = (60, HEIGHT // 2)
    elif scene == HOUSE:
        kyle.rect.center = (WIDTH // 2, HEIGHT // 2)
    elif scene == AREA1:
        kyle.rect.center = (80, HEIGHT - 80)
    elif scene == AREA2:
        kyle.rect.left = 10

# ===== PART 1 FUNCTIONS =====
def handle_wall_collisions():
    if kyle.rect.colliderect(wall_top): kyle.rect.top = wall_top.bottom
    if kyle.rect.colliderect(wall_bottom): kyle.rect.bottom = wall_bottom.top

    if game_state == CENTER:
        if kyle.rect.colliderect(wall_left): change_scene(LEFT)
        if kyle.rect.colliderect(wall_right): change_scene(RIGHT)
    elif game_state == LEFT:
        if kyle.rect.colliderect(wall_left): kyle.rect.left = wall_left.right
        if kyle.rect.right >= WIDTH: change_scene(CENTER)
    elif game_state == RIGHT:
        if kyle.rect.colliderect(wall_right): kyle.rect.right = wall_right.left
        if kyle.rect.left <= 0: change_scene(CENTER)

def handle_house_collisions():
    for wall in house_walls:
        if kyle.rect.colliderect(wall):
            if wall.top == house_area.top: kyle.rect.top = wall.bottom
            elif wall.left == house_area.left: kyle.rect.left = wall.right
            elif wall.right == house_area.right: kyle.rect.right = wall.left
            elif wall.bottom == house_area.bottom:
                if not kyle.rect.colliderect(house_door.inflate(10, 10)):
                    kyle.rect.bottom = wall.top

def draw_next_button():
    btn_width, btn_height = 120, 40
    btn_rect = pygame.Rect(WIDTH//2 - btn_width//2, HEIGHT//2 + 60, btn_width, btn_height)
    pygame.draw.rect(screen, GRAY, btn_rect)
    pygame.draw.rect(screen, BLACK, btn_rect, 2)
    text_surf = font.render("Next", True, BLACK)
    text_rect = text_surf.get_rect(center=btn_rect.center)
    screen.blit(text_surf, text_rect)
    return btn_rect

# ===== PART 2 FUNCTIONS =====
def draw_enter_house_button():
    btn_width, btn_height = 220, 60
    btn_rect = pygame.Rect(WIDTH//2 - btn_width//2, HEIGHT - 80, btn_width, btn_height)
    pygame.draw.rect(screen, GRAY, btn_rect)
    pygame.draw.rect(screen, BLACK, btn_rect, 3)
    text_surf = font.render("Enter the house", True, BLACK)
    text_rect = text_surf.get_rect(center=btn_rect.center)
    screen.blit(text_surf, text_rect)
    return btn_rect

# ===== PART 3 FUNCTIONS =====
def draw_talk_button():
    btn_width, btn_height = 220, 60
    btn_rect = pygame.Rect(WIDTH//2 - btn_width//2, HEIGHT - 80, btn_width, btn_height)
    pygame.draw.rect(screen, GRAY, btn_rect)
    pygame.draw.rect(screen, BLACK, btn_rect, 3)
    text_surf = font.render("Talk to Claudia", True, BLACK)
    text_rect = text_surf.get_rect(center=btn_rect.center)
    screen.blit(text_surf, text_rect)
    return btn_rect

# ===== MAIN GAME LOOP =====
running = True
while running:
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            # Part 1 interactions
            if game_state == TITLE and start_button.is_clicked(pos):
                start_button.action()
                if music_playing:
                    pygame.mixer.music.stop()
                    music_playing = False
            elif game_state == CENTER and kyle.rect.colliderect(house_door.inflate(10, 10)):
                if enter_house_button.is_clicked(pos): enter_house_button.action()
            elif game_state == HOUSE and kyle.rect.colliderect(house_exit.inflate(10, 10)):
                if leave_house_button.is_clicked(pos): leave_house_button.action()
            elif game_state == CENTER and kyle.rect.colliderect(car_box.inflate(10, 10)):
                if drive_button.is_clicked(pos):
                    game_state = CUTSCENE1
            elif game_state == CUTSCENE1 and show_next_button:
                if next_btn_rect.collidepoint(pos):
                    game_state = AREA1
                    kyle.rect.center = (80, HEIGHT - 80)

            # Part 2 interactions
            elif game_state == AREA2 and show_cutscene_button and enter_house_btn_rect.collidepoint(pos):
                game_state = CUTSCENE2

            # Part 3 interactions
            elif game_state == PART3_PLAY and show_talk_button and talk_btn_rect.collidepoint(pos):
                game_state = PART3_DIALOG
                current_message = 0

            # Part 3 dialog progression
            elif game_state == PART3_DIALOG and event.type == pygame.MOUSEBUTTONDOWN:
                if current_message < len(messages) - 1:
                    current_message += 1
                else:
                    # Dialog finished, transition to Part 4
                    game_state = PART4_GAME
                    # Reset Part 4 variables
                    player_health = 4
                    player_bullets = []
                    alien_bullets = []
                    alien_health = 0
                    stage = 1
                    countdown_active = True
                    countdown_start_time = pygame.time.get_ticks()
                    can_shoot = False
                    alien = pygame.Rect(random.randint(0, WIDTH - alien_size), random.randint(0, HEIGHT - alien_size), alien_size, alien_size)
                    player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - 60, player_width, player_height)

    # ===== MOVEMENT HANDLING =====
    if game_state in [CENTER, LEFT, RIGHT, HOUSE, AREA1, AREA2, PART3_PLAY]:
        kyle.move(keys)
    elif game_state == PART4_GAME and not countdown_active and not game_over:
        # Part 4 movement
        if keys[pygame.K_a] and player.left > 0:
            player.x = int(player.x - player_speed)
        if keys[pygame.K_d] and player.right < WIDTH:
            player.x = int(player.x + player_speed)
        if keys[pygame.K_w] and player.top > 0:
            player.y = int(player.y - player_speed)
        if keys[pygame.K_s] and player.bottom < HEIGHT:
            player.y = int(player.y + player_speed)

    # ===== PART 1 LOGIC =====
    if game_state in [CENTER, LEFT, RIGHT, HOUSE]:
        handle_wall_collisions()
        if game_state == CENTER:
            handle_house_collisions()

    # ===== PART 2 LOGIC =====
    if game_state == AREA1:
        # Area 1 borders
        if kyle.rect.left < border_left_1.right:
            kyle.rect.left = border_left_1.right
        if kyle.rect.top < border_top_1.bottom:
            kyle.rect.top = border_top_1.bottom
        if kyle.rect.bottom > border_bottom_1.top:
            kyle.rect.bottom = border_bottom_1.top
        # Transition to Area 2
        if kyle.rect.right >= WIDTH:
            game_state = AREA2
            kyle.rect.left = 10
    elif game_state == AREA2:
        # Area 2 borders
        if kyle.rect.right > border_right_2.left:
            kyle.rect.right = border_right_2.left
        if kyle.rect.bottom > border_bottom_2.top:
            kyle.rect.bottom = border_bottom_2.top
        if kyle.rect.top < border_top_2.bottom:
            if not kyle.rect.colliderect(door_hitbox.inflate(10, 10)):
                kyle.rect.top = border_top_2.bottom
        # Transition back to Area 1
        if kyle.rect.left < 0:
            game_state = AREA1
            kyle.rect.right = WIDTH - 10

    # ===== PART 4 LOGIC =====
    if game_state == PART4_GAME:
        # Countdown Display
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
        elif not game_over:
            # Player Shooting
            if can_shoot and keys[pygame.K_SPACE] and current_time - last_shot_time > SHOT_COOLDOWN:
                bullet = pygame.Rect(player.centerx - 4, player.top - 10, 8, 20)
                player_bullets.append(bullet)
                last_shot_time = current_time

            # Move Alien
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
                alien.x = int(alien.x + alien_vx)
                alien.y = int(alien.y + alien_vy)

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

            # Alien Fire
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

            # Move Alien Bullets
            for bullet in alien_bullets[:]:
                bullet["rect"].x = int(bullet["rect"].x + bullet["vel"][0])
                bullet["rect"].y = int(bullet["rect"].y + bullet["vel"][1])
                if not screen.get_rect().colliderect(bullet["rect"]):
                    alien_bullets.remove(bullet)
                elif bullet["rect"].colliderect(player):
                    alien_bullets.remove(bullet)
                    player_health -= 1
                    if player_health <= 0:
                        game_over = True
                        player_won = False

            # Move Player Bullets
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

            # Stage Transition
            if stage == 1:
                if start_ticks is not None:
                    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
                    if seconds >= survival_time:
                        stage = 2
                        countdown_active = True
                        countdown_start_time = pygame.time.get_ticks()
                        can_shoot = True
                        alien_health = 25
                        alien_vx = 4.5
                        alien_vy = 4.5
                        ALIEN_FIRE_INTERVAL = 13

    # ===== DRAWING =====
    # Part 1 scenes
    if game_state == TITLE:
        if not music_playing:
            pygame.mixer.music.load('Renai Circulation恋愛サーキュレーション歌ってみたなみりん.mp3')
            pygame.mixer.music.play(-1)
            music_playing = True
        screen.blit(bg_title, (0, 0))
        start_button.draw(screen)
    elif game_state == CENTER:
        if music_playing:
            pygame.mixer.music.stop()
            music_playing = False
        screen.blit(bg_center, (0, 0))
        if kyle.rect.colliderect(house_door.inflate(10, 10)):
            enter_house_button.draw(screen)
        elif kyle.rect.colliderect(car_box.inflate(10, 10)):
            drive_button.draw(screen)
    elif game_state == HOUSE:
        screen.blit(bg_house, (0, 0))
        if kyle.rect.colliderect(house_exit.inflate(10, 10)):
            leave_house_button.draw(screen)
    elif game_state == LEFT:
        screen.blit(bg_left, (0, 0))
    elif game_state == RIGHT:
        screen.blit(bg_right, (0, 0))
    elif game_state == CUTSCENE1:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 40)
        text = font.render("Driving to next part...", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        show_next_button = True
        next_btn_rect = draw_next_button()

    # Part 2 scenes
    elif game_state == AREA1:
        screen.blit(area1_bg, (0, 0))
        show_cutscene_button = False
        enter_house_btn_rect = pygame.Rect(0, 0, 0, 0)
    elif game_state == AREA2:
        screen.blit(area2_bg, (0, 0))
        # Draw door
        pygame.draw.rect(screen, (200, 100, 0), door_hitbox)
        # Show 'Enter the house' button if Kyle is within 30px of the door
        if kyle.rect.colliderect(door_hitbox.inflate(30, 30)):
            show_cutscene_button = True
            enter_house_btn_rect = draw_enter_house_button()
        else:
            show_cutscene_button = False
            enter_house_btn_rect = pygame.Rect(0, 0, 0, 0)
    elif game_state == CUTSCENE2:
        screen.fill((220, 220, 220))
        text = font.render("You have entered her house", True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
        # Add button to continue to Part 3
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_state = PART3_PLAY
            kyle.rect.center = (WIDTH // 2, HEIGHT - 60)
            claudia.rect.center = (WIDTH // 2, HEIGHT // 2)

    # Part 3 scenes
    elif game_state == PART3_PLAY:
        screen.blit(part3_bg, (0, 0))
        screen.blit(claudia.image, claudia.rect)
        screen.blit(kyle.image, kyle.rect)
        
        # Check distance between Kyle and Claudia
        dx = kyle.rect.centerx - claudia.rect.centerx
        dy = kyle.rect.centery - claudia.rect.centery
        distance = (dx**2 + dy**2) ** 0.5
        if distance <= 30:
            show_talk_button = True
            talk_btn_rect = draw_talk_button()
        else:
            show_talk_button = False
            talk_btn_rect = pygame.Rect(0, 0, 0, 0)
    elif game_state == PART3_DIALOG:
        # Pick background based on message number
        background = bg1 if current_message < 8 else bg2
        screen.blit(background, (0, 0))

        # Draw textbox
        pygame.draw.rect(screen, TEXTBOX_COLOR, textbox_rect)
        pygame.draw.rect(screen, BLACK, textbox_rect, 3)

        # Draw wrapped text
        wrapped_lines = wrap_text(messages[current_message], font, textbox_rect.width - 20)
        for i, line in enumerate(wrapped_lines):
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (textbox_rect.x + 10, textbox_rect.y + 10 + i * 30))
        
        # Add instruction to click to continue
        font_small = pygame.font.SysFont(None, 25)
        click_text = font_small.render("Click to continue...", True, BLACK)
        screen.blit(click_text, (WIDTH//2 - click_text.get_width()//2, HEIGHT - 20))
    elif game_state == PART3_CUTSCENE:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 40)
        text = font.render("Cutscene: Talking to Claudia...", True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
        # Add instruction to click to continue
        font_small = pygame.font.SysFont(None, 30)
        click_text = font_small.render("Click to continue to final battle...", True, BLACK)
        screen.blit(click_text, (WIDTH//2 - click_text.get_width()//2, HEIGHT//2 + 50))

    # Part 4 scenes
    elif game_state == PART4_GAME:
        screen.blit(part4_bg, (0, 0))
        
        if not countdown_active and not game_over:
            # Draw game elements
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
            if player_won: 
                msg = "You Survived and Won!" 
                msg_surface = font.render(msg, True, WHITE)
                screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT // 2))
            else:
                msg = "You were Defeated!"
                msg_surface = font.render(msg, True, WHITE)
                screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT // 2))

    # Draw Kyle sprite (except in cutscenes and Part 4)
    if game_state not in [TITLE, CUTSCENE1, CUTSCENE2, PART3_DIALOG, PART4_GAME, PART4_OVER]:
        screen.blit(kyle.image, kyle.rect)

    pygame.display.flip()
    clock.tick(FPS)

# Exit cleanly
pygame.quit()
sys.exit() 