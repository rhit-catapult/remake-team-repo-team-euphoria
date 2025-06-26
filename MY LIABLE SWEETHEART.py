import pygame
import sys

#Part 1

pygame.init()

# Initialize mixer for music
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dating Sim Adventure")
clock = pygame.time.Clock()

# Game states
TITLE, CENTER, LEFT, RIGHT, HOUSE, CUTSCENE = "title", "center", "left", "right", "house", "cutscene"
game_state = TITLE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (0, 0, 255)
DARK_GRAY = (80, 80, 80)

# Background images
bg_title = pygame.transform.scale(pygame.image.load("Title Screen 1.png"), (WIDTH, HEIGHT))
bg_center = pygame.transform.scale(pygame.image.load("kyle_house.png"), (WIDTH, HEIGHT))
bg_house = pygame.transform.scale(pygame.image.load("KH_new.png"), (WIDTH, HEIGHT))
bg_left = pygame.transform.scale(pygame.image.load("left field.png"), (WIDTH, HEIGHT))
bg_right = pygame.transform.scale(pygame.image.load("cobble stone.png"), (WIDTH, HEIGHT))

# Kyle
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

# Buttons
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

# Instantiate player
kyle = Kyle(WIDTH // 2, HEIGHT // 2)

# Buttons
start_button = Button("Play", (WIDTH//2 - 60, HEIGHT - 80, 120, 40), lambda: change_scene(CENTER))
enter_house_button = Button("Enter Your House", (WIDTH//2 - 100, HEIGHT - 40, 200, 30), lambda: change_scene(HOUSE))
leave_house_button = Button("Leave the House", (WIDTH//2 - 100, HEIGHT - 40, 200, 30), lambda: change_scene(CENTER))

# Hitboxes
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

# Car hitbox and Drive button (in CENTER scene)
car_box = pygame.Rect(WIDTH - 100, HEIGHT - 100, 80, 60)
drive_button = Button("Drive", (WIDTH//2 - 60, HEIGHT - 40, 120, 30), lambda: None)

music_playing = False

# Scene transition
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
    elif game_state == CUTSCENE:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 40)
        text = font.render("Driving to next part...", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))


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

# Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Sprite size
        self.image.fill(BLUE)                  # Sprite color
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Add a Next button for the cutscene
def draw_next_button():
    btn_width, btn_height = 120, 40
    btn_rect = pygame.Rect(WIDTH//2 - btn_width//2, HEIGHT//2 + 60, btn_width, btn_height)
    pygame.draw.rect(screen, GRAY, btn_rect)
    pygame.draw.rect(screen, BLACK, btn_rect, 2)
    font = pygame.font.SysFont(None, 30)
    text_surf = font.render("Next", True, BLACK)
    text_rect = text_surf.get_rect(center=btn_rect.center)
    screen.blit(text_surf, text_rect)
    return btn_rect

# Main loop
running = True
level = 0
next_btn_rect = pygame.Rect(0, 0, 0, 0)
show_next_button = False
while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

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
                    game_state = CUTSCENE
            elif game_state == CUTSCENE and show_next_button:
                if next_btn_rect.collidepoint(pos):
                    # Transition to next cutscene or display a message
                    screen.fill(WHITE)
                    font = pygame.font.SysFont(None, 40)
                    text = font.render("Next part coming soon!", True, BLACK)
                    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    running = False

    if game_state != TITLE:
        kyle.move(keys)

    # Draw backgrounds for each scene
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
        handle_wall_collisions()
        handle_house_collisions()
        if kyle.rect.colliderect(house_door.inflate(10, 10)):
            enter_house_button.draw(screen)
        elif kyle.rect.colliderect(car_box.inflate(10, 10)):
            drive_button.draw(screen)
    elif game_state == HOUSE:
        screen.blit(bg_house, (0, 0))
        handle_wall_collisions()
        if kyle.rect.colliderect(house_exit.inflate(10, 10)):
            leave_house_button.draw(screen)
    elif game_state == LEFT:
        screen.blit(bg_left, (0, 0))
        handle_wall_collisions()
    elif game_state == RIGHT:
        screen.blit(bg_right, (0, 0))
        handle_wall_collisions()
    elif game_state == CUTSCENE:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 40)
        text = font.render("Driving to next part...", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        show_next_button = True
        next_btn_rect = draw_next_button()
    # Draw Kyle sprite
    screen.blit(kyle.image, kyle.rect)
    pygame.display.flip()
    clock.tick(60)


# Exit cleanly
pygame.quit()
sys.exit()

#Part 2

pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dating Sim Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
TEXTBOX_COLOR = (240, 240, 240)

# Fonts
font = pygame.font.SysFont(None, 28)
button_font = pygame.font.SysFont(None, 30)

# Game States
TITLE, VN_SCENE = "title", "vn_scene"
game_state = TITLE

# Backgrounds
bg_title = pygame.transform.scale(pygame.image.load("Title Screen 1.png"), (WIDTH, HEIGHT))
bg1 = pygame.transform.scale(pygame.image.load("claudia talk.png"), (WIDTH, HEIGHT))
bg2 = pygame.transform.scale(pygame.image.load("claudia din.jpg"), (WIDTH, HEIGHT))

# Textbox
TEXTBOX_HEIGHT = 150
textbox_rect = pygame.Rect(50, HEIGHT - TEXTBOX_HEIGHT - 30, WIDTH - 100, TEXTBOX_HEIGHT)

# Messages for VN
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
fade_in = True
fade_out = False
fade_alpha = 255
fade_speed = 5
vn_music_started = False
title_music_started = False

# Button class
class Button:
    def __init__(self, text, rect, action):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.action = action
        self.color = GRAY

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = button_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Start button
def start_vn_scene():
    global game_state, vn_music_started
    game_state = VN_SCENE
    pygame.mixer.music.stop()
    pygame.mixer.music.load("ytmp3free.cc_george-michaels-careless-whisper-slowed-instrumental-youtubemp3free.org.mp3")
    pygame.mixer.music.play(-1)
    vn_music_started = True

start_button = Button("Play", (WIDTH // 2 - 60, HEIGHT - 80, 120, 40), start_vn_scene)

# Text wrapping
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

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if game_state == TITLE and start_button.is_clicked(pos):
                start_button.action()
            elif game_state == VN_SCENE and not fade_out:
                if current_message < len(messages) - 1:
                    current_message += 1
                    if current_message == len(messages) - 1:
                        fade_out = True
                        fade_alpha = 0

    # === TITLE SCREEN ===
    if game_state == TITLE:
        if not title_music_started:
            pygame.mixer.music.load("Renai Circulation恋愛サーキュレーション歌ってみたなみりん.mp3")
            pygame.mixer.music.play(-1)
            title_music_started = True
        screen.blit(bg_title, (0, 0))
        start_button.draw(screen)

    # === VISUAL NOVEL SCENE ===
    elif game_state == VN_SCENE:
        background = bg1 if current_message <= 7 else bg2
        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, TEXTBOX_COLOR, textbox_rect)
        pygame.draw.rect(screen, BLACK, textbox_rect, 3)

        wrapped_lines = wrap_text(messages[current_message], font, textbox_rect.width - 20)
        for i, line in enumerate(wrapped_lines):
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (textbox_rect.x + 10, textbox_rect.y + 10 + i * 30))

        if fade_in:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha -= fade_speed
            if fade_alpha <= 0:
                fade_in = False
                fade_alpha = 0

        if fade_out and current_message == len(messages) - 1:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            if fade_alpha < 255:
                fade_alpha += fade_speed
            else:
                pygame.mixer.music.stop()
                running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()