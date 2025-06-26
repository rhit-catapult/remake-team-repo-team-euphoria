import pygame
import sys

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