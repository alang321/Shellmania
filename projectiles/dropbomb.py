import pygame
from Vector import Vector2d
from explosion import explosion
from particles import particle


class dropbomb:
    width = 6
    height = 20

    g = 9.80065
    rho = 1.225
    Cd = 0.7
    S = 0.005

    def __init__(self, pos, dir, velocity, terrain, wind, entities, player, m=1.0, color=pygame.color.THECOLORS["red"]):
        #vel pos
        self.velocity = velocity * dir
        self.pos = pos

        #references
        self.terrain = terrain
        self.entities = entities
        self.entities[1].append(self)
        self.delete = False
        #player that fired the missile
        self.player = player

        self.m = m

        self.color = color
        #main sprite
        self.sprite = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.sprite.get_rect()
        pygame.draw.ellipse(self.sprite, self.color, ((0, 3), (self.width, self.height)))
        pygame.draw.rect(self.sprite, self.color, ((0, 0), (self.width, 4)))


        #trail particle
        self.trailcounter = 0
        self.traillength = 5
        self.trailhistory = [None] * self.traillength
        self.trailinterval = 0.001
        self.timesincetrail = self.trailinterval
        self.currentindex = self.traillength-1
        return

    def draw(self, screen):
        screen.blit(self.sprite, [self.pos[0] - (self.rect.w / 2), self.pos[1] - self.rect.h/2])

    def update(self, dt):
        #this list holds all the forces acting on the missile
        forces = [self._forcedrag(), self._forcegravity()]

        #update position and velocity depeneing on the timestep
        for i in range(2):
            self.velocity[i] += (sum([j[i] for j in forces]) / self.m) * dt
            self.pos[i] += 20.0 * self.velocity[i] * dt

        #if new pos is outside bounds delete
        if 0 < self.pos[0] < self.terrain.bounds[0] - 1.0:
            #if new pos is under ground explode
            if self.terrain.heightmap[int(self.pos[0])] < self.pos[1]:
                explosion([self.pos[0], self.terrain.heightmap[int(self.pos[0])]], self.terrain, self.entities, self.player, 15, 0.4, 0.3, 0.8)
                self.delete = True
        else:
            self.delete = True

    def _forcedrag(self):
        dragtotal = self.Cd * self.S * 0.5 * self.rho * self.velocity.lengthsquared()
        return self.velocity.getuvec() * dragtotal

    # calculates the force of gravity in x and y direction
    def _forcegravity(self):
        return Vector2d(0, (self.g * self.m))