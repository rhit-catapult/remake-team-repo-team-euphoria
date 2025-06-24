import pygame
import sys
import os

# === Setup ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scene Teleport Game")

FPS = 75
clock = pygame.time.Clock()

# === Asset Loading ===
def load_image(path, fallback_color=(255, 0, 0), size=(40, 40)):
    if os.path.exists(path):
        return pygame.transform.scale(pygame.image.load(path), size)
    else:
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        return surf

# Load player sprite
player_image = load_image("player_image.png")

# Load background images (scene backgrounds)
backgrounds = [
    load_image("assets/background0.png", fallback_color=(255, 255, 255), size=(WIDTH, HEIGHT)),
    load_image("assets/background1.png", fallback_color=(0, 255, 0), size=(WIDTH, HEIGHT))
]

# === Classes ===
class Kyle:
    def __init__(self, screen: pygame.Surface, x, y, image_filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_filename)
        self.speed = 10
        self.rect = self.image.get_rect()

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self):
        ## Draw kyle
        # self.rect = self.image.get_rect()
        self.screen.blit(self.image, self.rect)

class Scene:
    def __init__(self, screen, background_img, obstacles, img_obstacles):
        self.background = background_img
        self.box_obstacles = obstacles  # List of pygame.Rect (hitboxes)
        self.img_obstacles = img_obstacles

        self.screen = screen

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        for obs in self.box_obstacles:
            pygame.draw.rect(surface, (100, 100, 100), obs, 2)  # Draw building hitbox outlines

        for img, pos in self.img_obstacles:
            self.screen.blit(img, (pos.x, pos.y))

# === Game Data ===
player = Kyle(screen, WIDTH // 2, HEIGHT // 2, "kyle (2).png")
# player_group = pygame.sprite.Group(player)

kyleimg = pygame.image.load("kyle_left.png")
# Example building hitboxes for each scene
scenes = [
    Scene(screen, backgrounds[0], [pygame.Rect(150, 150, 100, 100), pygame.Rect(400, 300, 120, 80),],
          [(kyleimg, pygame.Rect(200, 50, 100, 100))]),
    Scene(screen, backgrounds[1], [pygame.Rect(200, 100, 150, 150)], [])
]

current_scene = 0

# === Game Loop ===

def hitbox_helper(hitbox_i):
    if player.rect.colliderect(hitbox_i):
        # Simple collision response: push player back (basic)
        if keys[pygame.K_LEFT]:
            player.rect.left = hitbox_i.right
        if keys[pygame.K_RIGHT]:
            player.rect.right = hitbox_i.left
        if keys[pygame.K_UP]:
            player.rect.top = hitbox_i.bottom
        if keys[pygame.K_DOWN]:
            player.rect.bottom = hitbox_i.top

running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    # === Events ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # === Movement ===
    keys = pygame.key.get_pressed()
    player.move(keys)

    # === Teleport Check ===
    if player.rect.right < 0:
        current_scene = (current_scene + 1) % len(scenes)
        player.rect.left = WIDTH
    elif player.rect.left > WIDTH:
        current_scene = (current_scene + 1) % len(scenes)
        player.rect.right = 0
    elif player.rect.top > HEIGHT:
        current_scene = (current_scene + 1) % len(scenes)
        player.rect.bottom = 0
    elif player.rect.bottom < 0:
        current_scene = (current_scene + 1) % len(scenes)
        player.rect.top = HEIGHT

    # === Collision with building hitboxes ===
    for hitbox in scenes[current_scene].box_obstacles:
        hitbox_helper(hitbox)

    for img in scenes[current_scene].img_obstacles:
        # (image, rectangle)
        # 0         1
        hitbox_helper(img[1])

    # === Drawing ===
    scenes[current_scene].draw(screen)
    player.draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
