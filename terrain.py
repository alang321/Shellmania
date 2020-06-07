import pygame
import numpy
from Vector import Vector2d
import random

class terrain:
    bedrockheight = 10

    def __init__(self, bounds, groundcolor=pygame.color.THECOLORS["green"]):
        self.bounds = bounds
        self.groundcolor = (193, 68, 14)
        self.backgroundcolor = pygame.color.THECOLORS["black"][:-1]

        #create surface that can later be edited with a reference array terrain bitmap
        self.surface = pygame.Surface(self.bounds)
        self.surface.set_colorkey(self.backgroundcolor)

        #height for each x pos
        self.heightmap = [None] * self.bounds[0]
        #normal vcector for each xpos
        self.normalmap = [None] * self.bounds[0]
        #true false bitmap
        self.bitmap = None
        return

    def generateTerrain(self):
        #generates a bool array which dictates where ground and where background is
        self.bitmap = numpy.full((self.bounds[0], self.bounds[1]), False)

        rand = []

        #generate x amount of random sin functions that get overlayed over each other to create random hilly terrain
        for i in range(7):
            gain = random.randint(int(self.bounds[1] / 4.5), int(self.bounds[1] / 2.3))
            freq = random.randint(int(self.bounds[0] / 40), int(self.bounds[0] / 8))
            phaseshift = random.randint(0, self.bounds[0] / 2)
            rand.append([gain, freq, phaseshift])


        for i in range(self.bounds[0]):
            height = 0.0
            for j in rand:
                height += self.bounds[1] / 2 + numpy.sin(i/j[1] + j[2]) * j[0]
            height = height/len(rand)

            for j in range(0, self.bounds[1]):
                if (self.bounds[1] - height) < j or j >= self.bounds[1] - self.bedrockheight:
                    self.bitmap[i, j] = True
                else:
                    self.bitmap[i, j] = False

        self.updateSurface(range(0, self.bounds[0]))

    def updateHeightmap(self, rangex):
        for i in rangex:
            self.heightmap[i] = self.bounds[0]-1
            for j in range(self.bounds[1]):
                if self.bitmap[i, j]:
                    self.heightmap[i] = j
                    break

    def updateNormalmap(self, rangex):
        distance = 7

        for i in rangex:
            origin = [max(float(i - distance), 0.0), float(self.heightmap[max(i - distance, 0)])]
            target = [float(min(i + distance, self.bounds[0]-1)), float(self.heightmap[min(i + distance, self.bounds[0] - 1)])]
            self.normalmap[i] = Vector2d.getvectorfrompoints(origin, target).getuvec().getnormalvec()
        return

    #update part of the terrain surface to reflect changes in bitmap
    def updateSurface(self, rangex):
        refarray = pygame.surfarray.pixels3d(self.surface)

        for i in rangex:
            for j in range(0, self.bounds[1]):
                if self.bitmap[i, j]:
                    refarray[i, j] = self.groundcolor
                else:
                    refarray[i, j] = self.backgroundcolor

        self.updateHeightmap(rangex)
        self.updateNormalmap(rangex)

    def draw(self, screen):
        print("draw terrain")
        screen.blit(self.surface, (0, 0))
        #for i in range(0, self.bounds[0], 10):
            #pygame.draw.aaline(screen, pygame.color.THECOLORS["white"], [i, self.heightmap[i]], [i + 30.0 * self.normalmap[i].x, self.heightmap[i] + 30.0 * self.normalmap[i].y])

