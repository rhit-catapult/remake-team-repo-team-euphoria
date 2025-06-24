import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dating Sim Adventure")
clock = pygame.time.Clock()

# Game states
TITLE, CENTER, LEFT, RIGHT, HOUSE, CUTSCENE, SECOND_TITLE, STREET1, STREET2 = (
    "title", "center", "left", "right", "house", "cutscene", "second_title", "street1", "street2"
)
game_state = TITLE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (80, 80, 80)
#Backgrounds (load and scale them)
bg_title = pygame.transform.scale(pygame.image.load("Title Screen 1.png"), (WIDTH, HEIGHT))
bg_center = pygame.transform.scale(pygame.image.load("kyle_house.png"), (WIDTH, HEIGHT))
bg_house = pygame.transform.scale(pygame.image.load("KHouse_inside.png"), (WIDTH, HEIGHT))
#bg_left = pygame.transform.scale(pygame.image.load("bg_left.png"), (WIDTH, HEIGHT))
#bg_right = pygame.transform.scale(pygame.image.load("bg_right.png"), (WIDTH, HEIGHT))
bg_street1 = pygame.transform.scale(pygame.image.load("Road to the house.png"), (WIDTH, HEIGHT))
bg_street2 = pygame.transform.scale(pygame.image.load("Road to the house.png"), (WIDTH, HEIGHT))
#bg_second_title = pygame.transform.scale(pygame.image.load("bg_second_title.png"), (WIDTH, HEIGHT))

# Kyle
class Kyle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Load all directional sprites ONCE
        self.sprites = {
            "up": pygame.image.load("kyle_back.png").convert_alpha(),
            "down": pygame.image.load("kyle (2).png").convert_alpha(),
            "left": pygame.image.load("kyle_left.png").convert_alpha(),
            "right": pygame.image.load("kyle_right.png").convert_alpha()
        }

        # Resize them all
        for key in self.sprites:
            self.sprites[key] = pygame.transform.scale(self.sprites[key], (40, 60))

        self.facing = "down"  # Default direction
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

        # Update sprite based on direction
        self.image = self.sprites[self.facing]

def test_character():

    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()


    kyle = Kyle(500, 400)  # Middle of screen

    running = True
    while running:
        screen.fill((255, 255, 255))  # Clear screen each frame with white

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        kyle.move(keys)

        screen.blit(kyle.image, kyle.rect)  # Draw Kyle
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


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
#kyle = Kyle()
#sprites = pygame.sprite.Group(kyle)
kyle = Kyle(WIDTH // 2, HEIGHT // 2)

# Buttons
start_button = Button("Play", (WIDTH//2 - 60, HEIGHT - 80, 120, 40), lambda: change_scene(CENTER))
enter_house_button = Button("Enter Your House", (WIDTH//2 - 100, HEIGHT - 40, 200, 30), lambda: change_scene(HOUSE))
leave_house_button = Button("Leave the House", (WIDTH//2 - 100, HEIGHT - 40, 200, 30), lambda: change_scene(CENTER))
drive_button = Button("Drive", (WIDTH//2 - 60, HEIGHT - 40, 120, 30), lambda: change_scene(CUTSCENE))
next_button = Button("Next", (WIDTH//2 - 60, HEIGHT//2 - 20, 120, 40), lambda: change_scene(STREET1))
enter_new_house_button = Button("Enter the house?", (WIDTH//2 - 100, HEIGHT - 40, 200, 30), lambda: sys.exit())

# Hitboxes
wall_top = pygame.Rect(0, 0, WIDTH, 10)
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

# Car hitbox (bottom-right)
car_box = pygame.Rect(WIDTH - 100, HEIGHT - 100, 80, 60)

# New larger house (in STREET2)
new_house = pygame.Rect(WIDTH // 2 - 150, 50, 300, 200)
new_house_door = pygame.Rect(WIDTH // 2 - 30, 230, 60, 10)

# Scene transition
def change_scene(scene):
    global game_state
    game_state = scene
    if scene in [CENTER, STREET1]:
        kyle.rect.center = (WIDTH // 2, HEIGHT // 2)
    elif scene == LEFT:
        kyle.rect.center = (WIDTH - 60, HEIGHT // 2)
    elif scene == RIGHT:
        kyle.rect.center = (60, HEIGHT // 2)
    elif scene == HOUSE:
        kyle.rect.center = (WIDTH // 2, HEIGHT // 2)
    elif scene == STREET2:
        kyle.rect.center = (60, HEIGHT // 2)

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
    elif game_state == STREET1:
        if kyle.rect.top <= 400: kyle.rect.top = 400
        if kyle.rect.bottom >= HEIGHT - 400: kyle.rect.bottom = HEIGHT - 400
        if kyle.rect.right >= WIDTH: change_scene(STREET2)
    elif game_state == STREET2:
        if kyle.rect.top <= 400: kyle.rect.top = 400
        if kyle.rect.bottom >= HEIGHT - 400: kyle.rect.bottom = HEIGHT - 400
        if kyle.rect.left <= 0: change_scene(STREET1)

def handle_house_collisions():
    for wall in house_walls:
        if kyle.rect.colliderect(wall):
            if wall.top == house_area.top: kyle.rect.top = wall.bottom
            elif wall.left == house_area.left: kyle.rect.left = wall.right
            elif wall.right == house_area.right: kyle.rect.right = wall.left
            elif wall.bottom == house_area.bottom:
                if not kyle.rect.colliderect(house_door.inflate(10, 10)):
                    kyle.rect.bottom = wall.top

# Main loop
running = True
while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if game_state == TITLE and start_button.is_clicked(pos): start_button.action()
            elif game_state == CENTER and kyle.rect.colliderect(house_door.inflate(10, 10)):
                if enter_house_button.is_clicked(pos): enter_house_button.action()
            elif game_state == HOUSE and kyle.rect.colliderect(house_exit.inflate(10, 10)):
                if leave_house_button.is_clicked(pos): leave_house_button.action()
            elif game_state == CENTER and kyle.rect.colliderect(car_box.inflate(10, 10)):
                if drive_button.is_clicked(pos): drive_button.action()
            elif game_state == SECOND_TITLE and next_button.is_clicked(pos): next_button.action()
            elif game_state == STREET2 and kyle.rect.colliderect(new_house_door.inflate(10, 10)):
                if enter_new_house_button.is_clicked(pos): enter_new_house_button.action()
        if game_state == TITLE:
            screen.blit(bg_title, (0, 0))
        elif game_state == CENTER:
            screen.blit(bg_center, (0, 0))
        elif game_state == HOUSE:
            screen.blit(bg_house, (0, 0))
        #elif game_state == LEFT:
            #screen.blit(bg_left, (0, 0))
        #elif game_state == RIGHT:
            #screen.blit(bg_right, (0, 0))
        elif game_state == STREET1:
            screen.blit(bg_street1, (0, 0))
        elif game_state == STREET2:
            screen.blit(bg_street2, (0, 0))
        elif game_state == SECOND_TITLE:
            #screen.blit(bg_second_title, (0, 0))
            pass
        else:
            screen.fill(WHITE)
    if game_state != TITLE:
        kyle.move(keys)


    if game_state == TITLE:
        start_button.draw(screen)

    elif game_state == CENTER:
        pygame.draw.rect(screen, DARK_GRAY, house_area, 2)
        pygame.draw.rect(screen, BLUE, house_door)
        pygame.draw.rect(screen, BLACK, car_box, 2)

        handle_wall_collisions()
        handle_house_collisions()

        if kyle.rect.colliderect(house_door.inflate(10, 10)):
            enter_house_button.draw(screen)
        elif kyle.rect.colliderect(car_box.inflate(10, 10)):
            drive_button.draw(screen)

        pygame.draw.rect(screen, BLACK, wall_left)
        pygame.draw.rect(screen, BLACK, wall_right)
        pygame.draw.rect(screen, BLACK, wall_top)
        pygame.draw.rect(screen, BLACK, wall_bottom)

    elif game_state == HOUSE:
        pygame.draw.rect(screen, BLUE, house_exit)
        handle_wall_collisions()
        if kyle.rect.colliderect(house_exit.inflate(10, 10)):
            leave_house_button.draw(screen)

    elif game_state == LEFT or game_state == RIGHT:
        handle_wall_collisions()
        if game_state == LEFT:
            pygame.draw.rect(screen, BLACK, wall_left)
        else:
            pygame.draw.rect(screen, BLACK, wall_right)

    elif game_state == CUTSCENE:
        game_state = SECOND_TITLE

    elif game_state == SECOND_TITLE:
        next_button.draw(screen)

    elif game_state == STREET1:
        handle_wall_collisions()
        pygame.draw.rect(screen, BLACK, (0, 400, WIDTH, 10))
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - 400, WIDTH, 10))
        pygame.draw.rect(screen, BLACK, wall_right)

    elif game_state == STREET2:
        handle_wall_collisions()
        pygame.draw.rect(screen, BLACK, (0, 400, WIDTH, 10))
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - 400, WIDTH, 10))
        pygame.draw.rect(screen, BLACK, wall_left)
        pygame.draw.rect(screen, DARK_GRAY, new_house, 2)
        pygame.draw.rect(screen, BLUE, new_house_door)

        if kyle.rect.colliderect(new_house_door.inflate(10, 10)):
            enter_new_house_button.draw(screen)


    screen.blit(kyle.image, kyle.rect)
    pygame.display.flip()
    clock.tick(60)

# Exit cleanly
pygame.quit()
sys.exit()