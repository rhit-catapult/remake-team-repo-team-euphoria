import pygame
import sys


class Kyle:
    def __init__(self, screen: pygame.Surface, x, y, image_filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_filename)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))





def test_character():
    screen = pygame.display.set_mode((1000, 800))
    kyle = Kyle(screen, 500, 50, "kyle (2).png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            kyle.x = kyle.x - 5
        if pressed_keys[pygame.K_RIGHT]:
            kyle.x = kyle.x + 5
        if pressed_keys[pygame.K_UP]:
            kyle.y = kyle.y - 5
        if pressed_keys[pygame.K_DOWN]:
            kyle.y = kyle.y + 5



        bg_image = pygame.image.load("Living_Room.png")

        kyle.draw()
        screen.blit(bg_image, (0, 0))
        pygame.display.update()







if __name__ == "__main__":
    test_character()

    pygame.display.set_caption("My Liable Sweetheart")
