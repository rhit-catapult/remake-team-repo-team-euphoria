import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dating Sim Prototype")

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

FONT = pygame.font.SysFont(None, 30)
BIGFONT = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

# Game States
TITLE = "title"
CENTER = "center"
LEFT = "left"
RIGHT = "right"
HOUSE = "house"
STREET1 = "street1"
STREET2 = "street2"

# Player
class Kyle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

kyle = Kyle(WIDTH // 2, HEIGHT // 2)

# Borders & hitboxes
center_top_border = pygame.Rect(0, 0, WIDTH, 50)
center_bottom_border = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

left_left_border = pygame.Rect(0, 0, 50, HEIGHT)
left_right_border = pygame.Rect(WIDTH - 50, 0, 50, HEIGHT)

right_left_border = pygame.Rect(0, 0, 50, HEIGHT)
right_right_border = pygame.Rect(WIDTH - 50, 0, 50, HEIGHT)

house_x, house_y, house_width, house_height = 325, 50, 150, 150
house_door = pygame.Rect(house_x + 55, house_y + 130, 40, 20)
first_house_border = pygame.Rect(house_x, house_y, house_width, house_height)

car_border = pygame.Rect(WIDTH - 120, HEIGHT - 120, 80, 50)
house_scene_border = pygame.Rect(0, 0, WIDTH, HEIGHT)

# UI Button
class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = GRAY
        self.text_surf = FONT.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Game state data
game_state = TITLE
buttons = []
active_button = None

# --- Utility functions ---
def clear_buttons():
    global buttons, active_button
    buttons.clear()
    active_button = None

def add_button(rect, text):
    btn = Button(rect, text)
    buttons.append(btn)
    return btn

def change_scene(new_scene):
    global game_state
    game_state = new_scene
    clear_buttons()
    if new_scene == CENTER:
        kyle.rect.center = (WIDTH // 2, HEIGHT // 2)
    elif new_scene == LEFT:
        kyle.rect.center = (100, HEIGHT // 2)
    elif new_scene == RIGHT:
        kyle.rect.center = (WIDTH - 100, HEIGHT // 2)
    elif new_scene == HOUSE:
        kyle.rect.center = (WIDTH // 2, HEIGHT - 100)
    elif new_scene == STREET1:
        kyle.rect.center = (WIDTH // 4, HEIGHT // 2)
    elif new_scene == STREET2:
        kyle.rect.center = (WIDTH // 4, HEIGHT // 2)

# --- Collision Handling ---
def handle_collisions():
    global active_button

    if game_state == CENTER:
        if kyle.rect.colliderect(left_left_border):
            change_scene(LEFT)
        if kyle.rect.colliderect(right_right_border):
            change_scene(RIGHT)

        if kyle.rect.top < center_top_border.bottom:
            kyle.rect.top = center_top_border.bottom
        if kyle.rect.bottom > center_bottom_border.top:
            kyle.rect.bottom = center_bottom_border.top

        if kyle.rect.colliderect(first_house_border) and not kyle.rect.colliderect(house_door):
            if kyle.rect.centery < house_y + house_height // 2:
                kyle.rect.bottom = first_house_border.top
            else:
                kyle.rect.top = first_house_border.bottom

        if kyle.rect.colliderect(house_door.inflate(10, 10)):
            if active_button is None:
                active_button = add_button((WIDTH // 2 - 100, HEIGHT - 40, 200, 30), "Enter Your House")
        elif active_button and active_button.text == "Enter Your House":
            clear_buttons()

        if kyle.rect.colliderect(car_border.inflate(10, 10)):
            if active_button is None:
                active_button = add_button((WIDTH // 2 - 50, HEIGHT - 40, 100, 30), "Drive")
        elif active_button and active_button.text == "Drive":
            clear_buttons()

    elif game_state == LEFT:
        if kyle.rect.colliderect(left_right_border):
            change_scene(CENTER)

    elif game_state == RIGHT:
        if kyle.rect.colliderect(right_left_border):
            change_scene(CENTER)

    elif game_state == HOUSE:
        kyle.rect.clamp_ip(house_scene_border)
        if kyle.rect.bottom >= HEIGHT - 50:
            if active_button is None:
                active_button = add_button((WIDTH // 2 - 100, HEIGHT - 40, 200, 30), "Leave the house")
        elif active_button and active_button.text == "Leave the house":
            clear_buttons()

    elif game_state == STREET1:
        if kyle.rect.top < 400:
            kyle.rect.top = 400
        if kyle.rect.bottom > HEIGHT - 50:
            kyle.rect.bottom = HEIGHT - 50
        if kyle.rect.right >= WIDTH:
            change_scene(STREET2)

    elif game_state == STREET2:
        if kyle.rect.top < 400:
            kyle.rect.top = 400
        if kyle.rect.bottom > HEIGHT - 50:
            kyle.rect.bottom = HEIGHT - 50
        if kyle.rect.left <= 0:
            change_scene(STREET1)

# --- Scene Drawing ---
def draw_title_scene():
    screen.fill(WHITE)
    title_text = BIGFONT.render("Dating Sim Prototype", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    if not buttons:
        add_button((WIDTH // 2 - 100, HEIGHT // 2, 200, 50), "Start")

    for btn in buttons:
        btn.draw(screen)

def draw_center_scene():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BROWN, first_house_border)
    pygame.draw.rect(screen, BLACK, house_door)
    pygame.draw.rect(screen, RED, car_border)
    pygame.draw.rect(screen, BLACK, center_top_border)
    pygame.draw.rect(screen, BLACK, center_bottom_border)

def draw_left_scene():
    screen.fill(GREEN)
    pygame.draw.rect(screen, BLACK, left_left_border)
    pygame.draw.rect(screen, BLACK, left_right_border)

def draw_right_scene():
    screen.fill(GREEN)
    pygame.draw.rect(screen, BLACK, right_left_border)
    pygame.draw.rect(screen, BLACK, right_right_border)

def draw_house_scene():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BROWN, house_scene_border)

def draw_street1_scene():
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 400))
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 50, WIDTH, 50))

def draw_street2_scene():
    screen.fill(GRAY)
    new_house = pygame.Rect(WIDTH // 2 - 200, 50, 400, 300)
    new_door = pygame.Rect(WIDTH // 2 - 40, 310, 80, 40)
    pygame.draw.rect(screen, BROWN, new_house)
    pygame.draw.rect(screen, BLACK, new_door)
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 400))
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 50, WIDTH, 50))

# --- Main Game Loop ---
def main():
    global active_button
    running = True

    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn.is_clicked(pos):
                        if btn.text == "Start":
                            change_scene(CENTER)
                        elif btn.text == "Enter Your House":
                            change_scene(HOUSE)
                        elif btn.text == "Leave the house":
                            change_scene(CENTER)
                        elif btn.text == "Drive":
                            change_scene(STREET1)
                        clear_buttons()

        if game_state != TITLE:
            kyle.move(keys)
            handle_collisions()

        # Draw the current scene
        if game_state == TITLE:
            draw_title_scene()
        elif game_state == CENTER:
            draw_center_scene()
        elif game_state == LEFT:
            draw_left_scene()
        elif game_state == RIGHT:
            draw_right_scene()
        elif game_state == HOUSE:
            draw_house_scene()
        elif game_state == STREET1:
            draw_street1_scene()
        elif game_state == STREET2:
            draw_street2_scene()

        # Draw player & buttons
        if game_state != TITLE:
            screen.blit(kyle.image, kyle.rect)
        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    change_scene(TITLE)
    main()
