import numpy as np
import pygame
import pygame.gfxdraw
from Vector import Vector2d
from particles import particle



class explosion2:

    def __init__(self, pos, terrain, entities, r=30.0, damage=0.8):
        self.pos = pos
        self.terrain = terrain
        self.players = entities[0]
        self.damage = damage
        self.blastradius = r

        self.maxdamagedropoff = 0.5

        if self.pos[1] > self.terrain.bounds[1] - self.terrain.bedrockheight - 1:
            self.pos[1] = self.terrain.bounds[1] - self.terrain.bedrockheight - 1


        surface = pygame.Surface([r*2+10, r*2+10])
        surface.fill((0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        pygame.gfxdraw.filled_circle(surface, int(surface.get_rect().w/2), int(surface.get_rect().h/2), int(self.blastradius+2), pygame.color.THECOLORS["orange"])
        #surface.fill(pygame.color.THECOLORS["red"])
        particle(pos, surface, 2, Vector2d(0.0, 0.0), 0.0, 0.0, entities[2], True)

        self._playerhits()
        self._destroyterrain()
        return

    def _playerhits(self):
        for i in self.players:
            distance = self._distance(i.pos, self.pos)
            if distance < self.blastradius + i.width/2:
                i.hit(self.damage-self.damage*(distance/self.blastradius)*self.maxdamagedropoff)

    def _distance(self, pos1, pos2):
        vector = [pos1[0] - pos2[0], pos1[1] - pos2[1]]
        return np.linalg.norm(vector)

    def _destroyterrain(self):
        rangex = range(int(max(self.pos[0] - self.blastradius, 0)),
                       int(min(self.pos[0] + self.blastradius, self.terrain.bounds[0])))
        rangey = range(int(max(self.pos[1] - self.blastradius, 0)),
                       int(min(self.pos[1] + self.blastradius, self.terrain.bounds[1] - self.terrain.bedrockheight)))

        for i in rangex:
            for j in rangey:
                if self._distance([i, j], self.pos) < self.blastradius:
                    self.terrain.bitmap[i, j] = False

        # drop down overhangs and floating parts
        for i in rangex:
            self._sort(self.terrain.bitmap[i])



        self.terrain.updateSurface(rangex)

    def _sort(self, bitmap):
        for i in range(int(self.pos[1]), int(self.pos[1]-self.blastradius)-1, -1):
            if bitmap[i]:
                for j in range(i, 0, -1):
                    if not bitmap[j]:
                        self._move(bitmap, [i+1, j])
                        return
                self._move(bitmap, [i+1, 0])
                return

    def _move(self, bitmap, deleterange):
        length = deleterange[0] - deleterange[1]

        for i in range(deleterange[1], deleterange[0]):
            bitmap[i] = False

        for i in range(deleterange[0], self.terrain.bounds[1]-1):
            if bitmap[i]:
                for j in range(i - length, i):
                    bitmap[j] = True
                return
