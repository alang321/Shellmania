import pygame
from Vector import Vector2d
from explosion import explosion
from particles import particle
import numpy as np


class nuke:
    _name = "Nuke"

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
        self.wind = wind

        self.m = m

        self.color = color

        self.color = color
        # main sprite
        self.sprite = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.sprite.get_rect()
        pygame.draw.ellipse(self.sprite, self.color, ((0, 3), (self.width, self.height)))
        pygame.draw.rect(self.sprite, self.color, ((0, 0), (self.width, 4)))

    def draw(self, screen):
        #rotate the sprite in the direcction of the velocity vector
        rotated = pygame.transform.rotate(self.sprite, np.rad2deg(self.velocity.findCCWAngle(Vector2d(0.0, 1.0))))
        screen.blit(rotated, (self.pos[0] - rotated.get_rect().w / 2.0, self.pos[1] - rotated.get_rect().h / 2.0))

    def update(self, dt):
        #this list holds all the forces acting on the missile
        forces = [self._forcedrag(), self._forcegravity(), self.wind.force]

        #update position and velocity depeneing on the timestep
        for i in range(2):
            self.velocity[i] += (sum([j[i] for j in forces]) / self.m) * dt
            self.pos[i] += 20.0 * self.velocity[i] * dt

        #if new pos is outside bounds delete
        if 0 < self.pos[0] < self.terrain.bounds[0] - 1.0:
            #if new pos is under ground explode
            if self.terrain.heightmap[int(self.pos[0])] < self.pos[1]:
                explosion(self.pos, self.terrain, self.entities, self.player, 65, 1, 0.4)

                flash = pygame.Surface([self.terrain.bounds[0], self.terrain.bounds[1]])
                flash.fill(pygame.color.THECOLORS["white"])
                particle([flash.get_rect().w/2, flash.get_rect().h/2], flash, 2.5, Vector2d(0, 0), 0, 0.0, self.entities[2], True, 0.3)

                self.delete = True
        else:
            self.delete = True


    def _forcedrag(self):
        dragtotal = self.Cd * self.S * 0.5 * self.rho * self.velocity.lengthsquared()
        return -1 * self.velocity.getuvec() * dragtotal

    # calculates the force of gravity in x and y direction
    def _forcegravity(self):
        return Vector2d(0, (self.g * self.m))