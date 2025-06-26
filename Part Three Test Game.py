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

# Fonts
font = pygame.font.SysFont(None, 28)

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
        # Clamp Kyle inside the window
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

# Claudia sprite
class Claudia(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("3.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 80))
        self.rect = self.image.get_rect(center=(x, y))

# Instantiate Kyle and Claudia
kyle = Kyle(WIDTH // 2, HEIGHT - 60)
claudia = Claudia(WIDTH // 2, HEIGHT // 2)

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

#Backgrounds (load and scale them)
bg_center = pygame.transform.scale(pygame.image.load("kyle_house.png"), (WIDTH, HEIGHT))
bg_house = pygame.transform.scale(pygame.image.load("KH_new.png"), (WIDTH, HEIGHT))
bg_left = pygame.transform.scale(pygame.image.load("left field.png"), (WIDTH, HEIGHT))
bg_right = pygame.transform.scale(pygame.image.load("cobble stone.png"), (WIDTH, HEIGHT))
bg_street1 = pygame.transform.scale(pygame.image.load("Road to the house.png"), (WIDTH, HEIGHT))
bg_street2 = pygame.transform.scale(pygame.image.load("Road to the house.png"), (WIDTH, HEIGHT))

# Backgrounds for cutscene
bg1 = pygame.transform.scale(pygame.image.load("cobble stone.png"), (WIDTH, HEIGHT))  # Messages 1–7
bg2 = pygame.transform.scale(pygame.image.load("GH_inside.png"), (WIDTH, HEIGHT))  # Messages 8+

# Textbox setup
TEXTBOX_COLOR = (240, 240, 240)
TEXTBOX_HEIGHT = 150
textbox_rect = pygame.Rect(50, HEIGHT - TEXTBOX_HEIGHT - 30, WIDTH - 100, TEXTBOX_HEIGHT)

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

# Main loop
running = True
show_talk_button = False
btn_rect = pygame.Rect(0, 0, 0, 0)
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == STATE_PLAY and event.type == pygame.MOUSEBUTTONDOWN and show_talk_button:
            if btn_rect.collidepoint(event.pos):
                game_state = STATE_CUTSCENE
        elif game_state == STATE_CUTSCENE and event.type == pygame.MOUSEBUTTONDOWN:
            if current_message < len(messages) - 1:
                current_message += 1

    if game_state == STATE_PLAY:
        kyle.move(keys)

    # Draw everything
    if game_state == STATE_PLAY:
        screen.fill(WHITE)
        screen.blit(claudia.image, claudia.rect)
        screen.blit(kyle.image, kyle.rect)
        # Check distance between Kyle and Claudia
        dx = kyle.rect.centerx - claudia.rect.centerx
        dy = kyle.rect.centery - claudia.rect.centery
        distance = (dx**2 + dy**2) ** 0.5
        show_talk_button = distance <= 30
        btn_rect = draw_talk_button() if show_talk_button else pygame.Rect(0, 0, 0, 0)
    elif game_state == STATE_CUTSCENE:
        # Pick background
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
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()


