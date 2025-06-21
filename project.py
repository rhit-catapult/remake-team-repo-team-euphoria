import pygame
import sys

import random
import time



def main():
    # turn on pygame
    pygame.init()

    # create a screen
    pygame.display.set_caption("My Liable Sweetheart")
    # TODO: Change the size of the screen as you see fit!
    screen = pygame.display.set_mode((900, 700))
    # creates a Character from the my_character.py file


    # let's set the framerate
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)  # this sets the framerate of your game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # TODO: Add you events code

        # TODO: Fill the screen with whatever background color you like!
        screen.fill((255, 255, 255))

        # draws the character every frame


        # TODO: Add your project code

        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()


main()
