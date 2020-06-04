import pygame
from Vector import Vector2d
from explosion import explosion
import numpy as np
from particles import particle


class bouncybomb:
    width = 10
    height = 10

    g = 9.80065
    rho = 1.225
    Cd = 0.7
    S = 0.005

    def __init__(self, pos, dir, velocity, terrain, wind, entities, player, m=1.0, color=pygame.color.THECOLORS["red"]):
        #vel pos
        self.velocity = velocity * dir
        self.pos = pos

        self.maxbounces = 1
        self.bounces = 0
        self.coeffrest = 0.6

        #references
        self.terrain = terrain
        self.entities = entities
        self.entities[1].append(self)
        self.delete = False
        #player that fired the missile
        self.player = player
        self.wind = wind

        self.m = m

        self.color = color
        #main sprite
        self.sprite = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.sprite.get_rect()
        pygame.draw.circle(self.sprite, self.color, [int(self.rect.w / 2.0), int(self.rect.h / 2.0)], 4)

        #trail particle
        trailsurface = pygame.Surface([7 * 2 + 5, 7 * 2 + 5])
        trailsurface.fill((0, 0, 0))
        trailsurface.set_colorkey((0, 0, 0))
        pygame.draw.circle(trailsurface, self.color, [int(self.rect.w / 2.0), int(self.rect.h / 2.0)], 2)
        self.trailsurface = trailsurface
        self.trailinterval = 0.003
        self.timesincetrail = 0.0
        return

    def draw(self, screen):
        screen.blit(self.sprite, [self.pos[0] - (self.rect.w / 2), self.pos[1] - self.rect.h/2])

    def update(self, dt):
        forces = [self._forcegravity(), self._forcedrag(), self.wind.force]

        for i in range(2):
            self.velocity[i] += (sum([j[i] for j in forces]) / self.m) * dt
            self.pos[i] += 20.0 * self.velocity[i] * dt

        if 0 < self.pos[0] < self.terrain.bounds[0]-1: # check if in bounds to avoid out of bounds array call in next line
            if self.pos[1] >= self.terrain.heightmap[int(self.pos[0])]: # check if at groundlevel
                self.bounces += 1
                if self.bounces <= self.maxbounces:

                    normal = self.terrain.normalmap[int(self.pos[0])]

                    newposset = False

                    for i in np.arange(0, 9, 0.3):
                        vec = normal * i
                        newpos = [self.pos[0] + vec.x, self.pos[1] + vec.y]

                        if newpos[1] < self.terrain.heightmap[int(newpos[0])]:
                            self.pos = newpos
                            newposset = True
                            break

                    if not newposset:
                        self.pos[1] = float(self.terrain.heightmap[int(self.pos[0])])

                    #newvelocity
                    self.velocity = self.velocity.getreflectionvect(self.terrain.normalmap[int(self.pos[0])]) * self.coeffrest
                else:
                    explosion(self.pos, self.terrain, self.entities, self.player)
                    self.delete = True
        else:
            self.delete = True


    def _forcedrag(self):
        dragtotal = self.Cd * self.S * 0.5 * self.rho * self.velocity.length() ** 2
        return self.velocity.getuvec() * dragtotal

    # calculates the force of gravity in x and y direction
    def _forcegravity(self):
        return Vector2d(0, (self.g * self.m))