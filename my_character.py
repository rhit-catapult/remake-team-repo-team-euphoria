import pygame
import sys


class Kyle:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(kyle)
        self.last_hit_time = 0

    #def draw(self):




def test_character():
    # TODO: change this function to test your class
    screen = pygame.display.set_mode((640, 480))
    character = Kyle(screen, 400, 400)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill("white")

        pygame.display.update()







if __name__ == "__main__":
    test_character()
