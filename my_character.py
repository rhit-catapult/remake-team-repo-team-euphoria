@ -1,73 +0,0 @@
import pygame
import sys


class Kyle:
    def __init__(self, screen: pygame.Surface, x, y, image_filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_filename)

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
<<<<<<< HEAD
        if pressed_keys[pygame.K_LEFT]:
<<<<<<< Updated upstream
            kyle.x = kyle.x - 0.09
        if pressed_keys[pygame.K_RIGHT]:
            kyle.x = kyle.x + 0.09
        if pressed_keys[pygame.K_UP]:
            kyle.y = kyle.y - 0.09
        if pressed_keys[pygame.K_DOWN]:
            kyle.y = kyle.y + 0.09
=======
            kyle.x = kyle.x - 0.05
        if pressed_keys[pygame.K_RIGHT]:
            kyle.x = kyle.x + 0.05
        if pressed_keys[pygame.K_UP]:
            kyle.y = kyle.y - 0.05
        if pressed_keys[pygame.K_DOWN]:
            kyle.y = kyle.y + 0.05
>>>>>>> Stashed changes
=======
        if pressed_keys[pygame.K_a]:
            kyle.x = kyle.x - 1
        if pressed_keys[pygame.K_d]:
            kyle.x = kyle.x + 1
        if pressed_keys[pygame.K_w]:
            kyle.y = kyle.y - 1
        if pressed_keys[pygame.K_s]:
            kyle.y = kyle.y + 1
>>>>>>> 4dc527b060b12df42269bef4e2a186ca20b8cf15

        bg_image = pygame.image.load("Living_Room.png")
        pygame.display.set_caption("Kyle on Top of Background")

        kyle.draw()
        screen.blit(bg_image, (0, 0))
        pygame.display.update()







if __name__ == "__main__":
    test_character()

    pygame.display.set_caption("My Liable Sweetheart")
