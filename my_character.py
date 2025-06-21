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
    # TODO: change this function to test your class
    screen = pygame.display.set_mode((640, 480))
    kyle = Kyle(screen, 300, 50, "kyle.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            kyle.x = kyle.x - 0.4
        if pressed_keys[pygame.K_RIGHT]:
            kyle.x = kyle.x + 0.4
        if pressed_keys[pygame.K_UP]:
            kyle.y = kyle.y - 0.4
        if pressed_keys[pygame.K_DOWN]:
            kyle.y = kyle.y + 0.4

        screen.fill("gray")

        kyle.draw()
        pygame.display.update()







if __name__ == "__main__":
    test_character()
