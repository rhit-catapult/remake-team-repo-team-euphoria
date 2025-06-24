import pygame
import sys

pygame.init()

# Screen size & colors
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dating Sim Prototype")

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
TITLE2 = "title2"  # Added missing TITLE2
CENTER = "center"
LEFT = "left"
RIGHT = "right"
HOUSE = "house"
STREET1 = "street1"
STREET2 = "street2"

# Define Kyle sprite class
class Kyle(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, x, y, image_filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_filename)
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




def test_character():
    screen = pygame.display.set_mode((1000, 800))
kyle = Kyle(screen, 500, 50, "kyle (2).png")


# --- Hitboxes and borders for scenes ---

# Center scene boundaries and borders
center_top_border = pygame.Rect(0, 0, WIDTH, 50)
center_bottom_border = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

# Left scene borders
left_left_border = pygame.Rect(0, 0, 50, HEIGHT)
left_right_border = pygame.Rect(WIDTH - 50, 0, 50, HEIGHT)

# Right scene borders
right_left_border = pygame.Rect(0, 0, 50, HEIGHT)
right_right_border = pygame.Rect(WIDTH - 50, 0, 50, HEIGHT)

# First house (center scene) - solid rectangle + door
house_x, house_y, house_width, house_height = 325, 50, 150, 150
house_door_width, house_door_height = 40, 20

first_house_border = pygame.Rect(house_x, house_y, house_width, house_height)
house_door = pygame.Rect(
    house_x + house_width // 2 - house_door_width // 2,
    house_y + house_height - house_door_height,
    house_door_width,
    house_door_height
)

# House scene borders (full window)
house_scene_border = pygame.Rect(0, 0, WIDTH, HEIGHT)

# Car hitbox (bottom right small rectangle)
car_x, car_y, car_w, car_h = WIDTH - 120, HEIGHT - 120, 80, 50
car_border = pygame.Rect(car_x, car_y, car_w, car_h)

# Button class for interactive buttons
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

game_state = TITLE
active_button = None
buttons = []

# Function to clear buttons
def clear_buttons():
    global buttons, active_button
    buttons = []
    active_button = None

# Function to add a button
def add_button(rect, text):
    global buttons
    btn = Button(rect, text)
    buttons.append(btn)
    return btn

# Function to change scene, reposition Kyle accordingly
def change_scene(new_scene):
    global game_state, kyle, buttons, active_button
    game_state = new_scene
    clear_buttons()
    if new_scene == TITLE:
        kyle.rect.center = (WIDTH // 2, HEIGHT // 2)
    elif new_scene == CENTER:
        kyle.rect.center = (WIDTH // 2, HEIGHT // 2)
    elif new_scene == LEFT:
        kyle.rect.center = (100, HEIGHT // 2)
    elif new_scene == RIGHT:
        kyle.rect.center = (WIDTH - 100, HEIGHT // 2)
    elif new_scene == HOUSE:
        kyle.rect.center = (WIDTH // 2, HEIGHT - 100)
    elif new_scene == STREET1:
        # Spawn Kyle inside the 400px boundary zone horizontally and vertically
        kyle.rect.center = (WIDTH // 4, HEIGHT // 2)
    elif new_scene == STREET2:
        kyle.rect.center = (WIDTH // 4, HEIGHT // 2)

def handle_collisions():
    global game_state, active_button

    if game_state == CENTER:
        # Borders left/right scenes
        if kyle.rect.colliderect(left_left_border):
            change_scene(LEFT)
        if kyle.rect.colliderect(right_right_border):
            change_scene(RIGHT)

        # Prevent moving outside top/bottom borders
        if kyle.rect.top < center_top_border.bottom:
            kyle.rect.top = center_top_border.bottom
        if kyle.rect.bottom > center_bottom_border.top:
            kyle.rect.bottom = center_bottom_border.top

        # Collide with first house walls except door
        if kyle.rect.colliderect(first_house_border) and not kyle.rect.colliderect(house_door):
            if kyle.rect.centery < house_y + house_height // 2:
                kyle.rect.bottom = first_house_border.top
            else:
                kyle.rect.top = first_house_border.bottom

        # Check if near house door for "Enter Your House"
        if kyle.rect.colliderect(house_door.inflate(10, 10)):
            if active_button is None:
                active_button = add_button((WIDTH // 2 - 100, HEIGHT - 40, 200, 30), "Enter Your House")
        else:
            if active_button and active_button.text == "Enter Your House":
                clear_buttons()

        # Check if near car to offer "Drive" button
        if kyle.rect.colliderect(car_border.inflate(10, 10)):
            if active_button is None:
                active_button = add_button((WIDTH // 2 - 50, HEIGHT - 40, 100, 30), "Drive")
        else:
            if active_button and active_button.text == "Drive":
                clear_buttons()

    elif game_state == LEFT:
        # Allow travel back to center from right border only
        if kyle.rect.colliderect(left_right_border):
            change_scene(CENTER)
        # Borders top and bottom same as center scene
        if kyle.rect.top < center_top_border.bottom:
            kyle.rect.top = center_top_border.bottom
        if kyle.rect.bottom > center_bottom_border.top:
            kyle.rect.bottom = center_bottom_border.top

    elif game_state == RIGHT:
        # Allow travel back to center from left border only
        if kyle.rect.colliderect(right_left_border):
            change_scene(CENTER)
        # Borders top and bottom same as center scene
        if kyle.rect.top < center_top_border.bottom:
            kyle.rect.top = center_top_border.bottom
        if kyle.rect.bottom > center_bottom_border.top:
            kyle.rect.bottom = center_bottom_border.top

    elif game_state == HOUSE:
        # Fully bounded in house scene
        kyle.rect.clamp_ip(house_scene_border)
        # Leave house button if near bottom edge
        if kyle.rect.bottom >= HEIGHT - 50:
            if active_button is None:
                active_button = add_button((WIDTH // 2 - 100, HEIGHT - 40, 200, 30), "Leave the house")
        else:
            if active_button and active_button.text == "Leave the house":
                clear_buttons()

    elif game_state == STREET1:
        # Borders: 400 pixels from top and bottom create street area
        if kyle.rect.top < 400:
            kyle.rect.top = 400
        if kyle.rect.bottom > HEIGHT - 50:  # fixed bottom boundary
            kyle.rect.bottom = HEIGHT - 50

        # Border right side - going off right edge transitions to STREET2
        if kyle.rect.right >= WIDTH:
            change_scene(STREET2)

    elif game_state == STREET2:
        # Borders: 400 pixels top and bottom
        if kyle.rect.top < 400:
            kyle.rect.top = 400
        if kyle.rect.bottom > HEIGHT - 50:  # fixed bottom boundary
            kyle.rect.bottom = HEIGHT - 50

        # Left border returns to STREET1
        if kyle.rect.left <= 0:
            change_scene(STREET1)

        # Second house - solid walls + door (larger house)
        new_house_x, new_house_y, new_house_width, new_house_height = WIDTH // 2 - 200, 50, 400, 300
        new_house_door_width, new_house_door_height = 80, 40

        new_house_border = pygame.Rect(new_house_x, new_house_y, new_house_width, new_house_height)
        new_house_door = pygame.Rect(
            new_house_x + new_house_width // 2 - new_house_door_width // 2,
            new_house_y + new_house_height - new_house_door_height,
            new_house_door_width,
            new_house_door_height
        )

        # Collide with new house walls except door
        if kyle.rect.colliderect(new_house_border) and not kyle.rect.colliderect(new_house_door):
            if kyle.rect.centery < new_house_y + new_house_height // 2:
                kyle.rect.bottom = new_house_border.top
            else:
                kyle.rect.top = new_house_border.bottom

        # Check if near new house door for "Enter Your House"
        if kyle.rect.colliderect(new_house_door.inflate(10, 10)):
            if active_button is None:
                active_button = add_button((WIDTH // 2 - 100, HEIGHT - 40, 200, 30), "Enter Your House")
        else:
            if active_button and active_button.text == "Enter Your House":
                clear_buttons()

# Remove the old draw_title_scene and main duplicates at the bottom
# Keep only one main() and one draw_title_scene()

# Modified draw_title_scene:
def draw_title_scene():
    screen.fill(WHITE)
    title_text = BIGFONT.render("Dating Sim Prototype", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    # Create start button only if buttons list is empty
    if not buttons:
        start_button = Button((WIDTH // 2 - 100, HEIGHT // 2, 200, 50), "Start")
        buttons.append(start_button)

    # Draw all buttons
    for btn in buttons:
        btn.draw(screen)

# Single main loop handling events and drawing:
def main():
    global active_button, buttons

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
                        print(f"Button '{btn.text}' clicked!")  # Debug info
                        # Handle button clicks
                        if btn.text == "Start":
                            change_scene(CENTER)
                            buttons.clear()
                            active_button = None
                        elif btn.text == "Enter Your House":
                            change_scene(HOUSE)
                            buttons.clear()
                            active_button = None
                        elif btn.text == "Leave the house":
                            change_scene(CENTER)
                            buttons.clear()
                            active_button = None
                        elif btn.text == "Drive":
                            change_scene(STREET1)
                            buttons.clear()
                            active_button = None

        if game_state != TITLE:
            kyle.move(keys)
            handle_collisions()

        # Draw current scene
        if game_state == TITLE:
            draw_title_scene()
        #elif game_state == CENTER:
            #draw_center_scene()
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

        # Draw Kyle sprite (except in TITLE scene)
        if game_state != TITLE:
            screen.blit(kyle.image, kyle.rect)

        # Draw buttons (except TITLE, already drawn in draw_title_scene)
        if game_state != TITLE:
            for btn in buttons:
                btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    change_scene(TITLE)
    main()

def draw_center_scene():
    screen.fill(WHITE)
    # Draw house and door
    pygame.draw.rect(screen, BROWN, first_house_border)
    pygame.draw.rect(screen, BLACK, house_door)
    # Draw car
    pygame.draw.rect(screen, RED, car_border)
    # Draw borders top and bottom
    pygame.draw.rect(screen, BLACK, center_top_border)
    pygame.draw.rect(screen, BLACK, center_bottom_border)

def draw_left_scene():
    screen.fill(GREEN)
    pygame.draw.rect(screen, BLACK, left_left_border)
    pygame.draw.rect(screen, BLACK, left_right_border)

def draw_right_scene():
    screen.fill(GREEN)
    pygame.draw.rect(screen, BLACK, right_left_border)
    pygame.draw.rect(screen, BLACK, right_right_border)  # fixed argument order

def draw_house_scene():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BROWN, house_scene_border)

def draw_street1_scene():
    screen.fill(GRAY)
    # Draw boundaries for street 1 - top and bottom rectangles
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 400))  # top boundary
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 50, WIDTH, 50))  # bottom boundary

def draw_street2_scene():
    screen.fill(GRAY)
    # Draw new house
    new_house_x, new_house_y, new_house_width, new_house_height = WIDTH // 2 - 200, 50, 400, 300
    new_house_door_width, new_house_door_height = 80, 40
    new_house_border = pygame.Rect(new_house_x, new_house_y, new_house_width, new_house_height)
    new_house_door = pygame.Rect(
        new_house_x + new_house_width // 2 - new_house_door_width // 2,
        new_house_y + new_house_height - new_house_door_height,
        new_house_door_width,
        new_house_door_height
    )
    pygame.draw.rect(screen, BROWN, new_house_border)
    pygame.draw.rect(screen, BLACK, new_house_door)
    # Draw boundaries
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 400))  # top boundary
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 50, WIDTH, 50))  # bottom boundary

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
                if active_button and active_button.is_clicked(pos):
                    # Handle button actions
                    if active_button.text == "Start":
                        change_scene(CENTER)
                        clear_buttons()
                    elif active_button.text == "Enter Your House":
                        change_scene(HOUSE)
                        clear_buttons()
                    elif active_button.text == "Leave the house":
                        change_scene(CENTER)
                        clear_buttons()
                    elif active_button.text == "Drive":
                        change_scene(STREET1)  # Changed to STREET1 to fix bug
                        clear_buttons()

        if game_state != TITLE:
            kyle.move(keys)
            handle_collisions()

        # Draw current scene
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

        # Draw Kyle sprite
        if game_state != TITLE:
            screen.blit(kyle.image, kyle.rect)

        # Draw buttons if any
        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    change_scene(TITLE)
    main()


def draw_title_scene():
    screen.fill(WHITE)
    title_text = BIGFONT.render("Dating Sim Prototype", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    # Instead of recreating buttons every frame, create once on entering title scene
    if not buttons:
        start_button = Button((WIDTH // 2 - 100, HEIGHT // 2, 200, 50), "Start")
        buttons.append(start_button)

    for btn in buttons:
        btn.draw(screen)

# In main loop, do NOT clear buttons every frame, only on scene change

def main():
    global active_button, buttons

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
                        print(f"Button '{btn.text}' clicked!")  # Debug print to verify click
                        # Handle button actions
                        if btn.text == "Start":
                            change_scene(CENTER)
                            buttons.clear()
                            active_button = None
                        elif btn.text == "Enter Your House":
                            change_scene(HOUSE)
                            buttons.clear()
                            active_button = None
                        elif btn.text == "Leave the house":
                            change_scene(CENTER)
                            buttons.clear()
                            active_button = None
                        elif btn.text == "Drive":
                            change_scene(STREET1)
                            buttons.clear()
                            active_button = None

        if game_state != TITLE:
            kyle.move(keys)
            handle_collisions()

        # Draw current scene
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

        # Draw Kyle sprite
        if game_state != TITLE:
            screen.blit(kyle.image, kyle.rect)

        # Draw buttons if any (except title scene where buttons drawn inside its function)
        if game_state != TITLE:
            for btn in buttons:
                btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        kyle.draw()
    pygame.quit()
    sys.exit()
