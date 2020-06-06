import pygame
import random
from terrain import terrain

class background:
    def __init__(self, screensize, backgroundcolor=pygame.color.THECOLORS["black"], decoterrain=False, starcolor=pygame.color.THECOLORS["white"]):
        self.starcolor = starcolor[:-1]
        self.backgroundcolor = backgroundcolor[:-1]
        self.screensize = screensize

        #create surface that can later be edited with a reference array terrain bitmap
        self.surface = pygame.Surface(self.screensize)
        self.surface.fill(self.backgroundcolor)

        #star
        star = pygame.Surface([5, 5])
        star.fill(self.backgroundcolor)
        #pygame.draw.circle(star, self.starcolor, (int(star.get_rect().w / 2), int(star.get_rect().h / 2)), 2)
        pygame.draw.rect(star, self.starcolor, ((0, 0), (2, 2)))

        #generate n number of stars with random locations
        self.generateStars(star, int((self.screensize[0] * self.screensize[1])/2600.0))

        if decoterrain:
            deco = terrain(screensize)
            deco.generateTerrain()
            deco.draw(self.surface)

        self.surface.convert()
        return

    def generateStars(self, star, n):
        stars = [[random.randrange(0, self.screensize[0]), random.randrange(0, self.screensize[1])] for x in range(n)]

        for i in stars:
            self.surface.blit(star, i)

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))
