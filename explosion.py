import numpy as np
from particles import particle
import pygame
import pygame.gfxdraw

class explosion:

    def __init__(self, pos, terrain, entities, r=40.0, damage=0.8):
        self.pos = pos
        self.terrain = terrain
        self.players = entities[0]
        self.damage = damage
        self.blastradius = r

        #at maximum distance the damage is halved
        self.maxdamagedropoff = 0.5


        if self.pos[1] > self.terrain.bounds[1] - self.terrain.bedrockheight - 1:
            self.pos[1] = self.terrain.bounds[1] - self.terrain.bedrockheight - 1


        surface = pygame.Surface([r*2+10, r*2+10])
        surface.fill((0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        pygame.gfxdraw.filled_circle(surface, int(surface.get_rect().w/2), int(surface.get_rect().h/2), int(self.blastradius+2), pygame.color.THECOLORS["red"])
        #surface.fill(pygame.color.THECOLORS["red"])
        particle(pos, surface, 2, [0.0, 0.0], 0.0, 0.0, entities[2], True)

        self._playerhits()
        self._destroyterrain()
        return

    def _playerhits(self):
        for i in self.players:
            distance = self._distance(i.pos, self.pos)
            if distance < self.blastradius+12:
                i.hit(self.damage-self.damage*(distance/self.blastradius)*self.maxdamagedropoff)

    def _distance(self, pos1, pos2):
        vector = [pos1[0] - pos2[0], pos1[1] - pos2[1]]
        return np.linalg.norm(vector)

    def _destroyterrain(self):
        rangex = range(int(max(self.pos[0]-self.blastradius, 0)), int(min(self.pos[0]+self.blastradius, self.terrain.bounds[0])))
        rangey = range(int(max(self.pos[1], 0)), int(min(self.pos[1]+self.blastradius, self.terrain.bounds[1]-self.terrain.bedrockheight)))
        rangey2 = range(0, int(min(self.pos[1], self.terrain.bounds[1]-self.terrain.bedrockheight)))

        for i in rangex:
            for j in rangey:
                if self._distance([i, j], self.pos) < self.blastradius:
                    self.terrain.bitmap[i, j] = False
            for j in rangey2:
                self.terrain.bitmap[i, j] = False


        self.terrain.updateSurface(rangex)