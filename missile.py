import pygame
import numpy as np
from explosion import explosion
from explosion2 import explosion2
from particles import particle


class missile:
    width = 6
    height = 6

    g = 9.80065
    rho = 1.225
    Cd = 0.7
    S = 0.005

    def __init__(self, pos, dir, velocity, terrain, entities, m=1, color=pygame.color.THECOLORS["red"]):
        self.dir = dir
        self.velocity = [self.dir[0] * velocity, self.dir[1] * velocity]
        self.pos = pos
        self.terrain = terrain
        self.entities = entities

        self.entities[1].append(self)

        self.m = m
        self.sprite = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.sprite.get_rect()
        self.color = color

        pygame.draw.circle(self.sprite, self.color, [int(self.rect.w / 2.0), int(self.rect.h / 2.0)], 2)

        trailsurface = pygame.Surface([7 * 2 + 5, 7 * 2 + 5])
        trailsurface.fill((0, 0, 0))
        trailsurface.set_colorkey((0, 0, 0))
        pygame.draw.circle(trailsurface, self.color, [int(self.rect.w / 2.0), int(self.rect.h / 2.0)], 2)
        self.trailsurface = trailsurface

        self.delete = False

        self.trailinterval = 0.003
        self.timesincesmoke = 0.0
        return

    def draw(self, screen):
        screen.blit(self.sprite, [self.pos[0] - (self.rect.w / 2), self.pos[1] - self.rect.h/2])

    def update(self, dt):
        self.timesincesmoke += dt
        if self.timesincesmoke > self.trailinterval:
            self.timesincesmoke = 0.0
            trailsurface = pygame.Surface([6, 6])
            trailsurface.set_colorkey((0, 0, 0))
            trailsurface.blit(self.trailsurface, (0, 0))
            particle(self.pos.copy(), trailsurface, 0.2, [0.0, 0.0], 0, 0, self.entities[2], True)

        if not self.terrain.heightmap[int(self.pos[0])] < self.pos[1]:
            forces = [self._forcedrag(), self._forcegravity()]

            for i in range(2):
                self.velocity[i] += (sum([j[i] for j in forces]) / self.m) * dt
                self.pos[i] += 30 * self.velocity[i] * dt

            if not 0 < self.pos[0] < self.terrain.bounds[0] - 1.0:
                self.delete = True
            #recalculate the direction vector of the projectile
            self.dir = self.velocity / np.linalg.norm(self.velocity)
        else:
            explosion2(self.pos, self.terrain, self.entities)
            self.delete = True


    def _forcedrag(self):
        v = np.linalg.norm(self.velocity)
        dragtotal = self.Cd * self.S * 0.5 * self.rho * v ** 2
        return [-self.dir[0] * dragtotal, -self.dir[1] * dragtotal]

    # calculates the force of gravity in x and y direction
    def _forcegravity(self):
        return [0, (self.g * self.m)]