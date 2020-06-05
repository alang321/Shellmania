import pygame
from Vector import Vector2d
from particles import particle
import random
from projectiles.dropbomb import dropbomb

class airstrike:
    _name = "Airstrike"

    width = 5
    height = 5

    g = 9.80065
    rho = 1.225
    Cd = 0.7
    S = 0.005

    def __init__(self, pos, dir, velocity, terrain, wind, entities, player, m=1.0, color=pygame.color.THECOLORS["red"]):
        #vel pos
        self.velocity = velocity * dir
        self.pos = pos

        #whether or not the missile has impacted the ground
        self.impacted = False
        #how long the projectile is alive after impact
        self.maxtimealive = 2.5
        self.alivetimer = 0.0
        self.bombdelay = 2.0
        self.bombsdeployed = False

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
        pygame.draw.circle(self.sprite, self.color, [int(self.rect.w / 2.0), int(self.rect.h / 2.0)], 2)

        #smoke
        self.timesincesmoke = 0.2
        self.smokeinterval = 0.1
        return

    def draw(self, screen):
        screen.blit(self.sprite, [self.pos[0] - (self.rect.w / 2), self.pos[1] - self.rect.h/2])

    def update(self, dt):
        if not self.impacted:
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
                    #delete missile
                    self.impacted = True
            else:
                self.delete = True
        else:
            self.alivetimer += dt
            if self.alivetimer < self.maxtimealive:
                self.timesincesmoke += dt
                if self.timesincesmoke > self.smokeinterval:
                    self.timesincesmoke = 0.0
                    dir = Vector2d(random.randint(-5, 5), -38.0).getuvec()
                    radius = 5
                    smoke = pygame.Surface([radius * 2 + 2, radius * 2 + 2])
                    smoke.fill((0, 0, 0))
                    smoke.set_colorkey((0, 0, 0))
                    pygame.draw.circle(smoke, self.color, (int(smoke.get_rect().w / 2), int(smoke.get_rect().h / 2)),radius)
                    particle(self.pos.copy(), smoke, random.randint(2, 5), dir, 1.25, 0.19, self.entities[2], True, 0.0, self.wind, 8.0)

                if not self.bombsdeployed and self.alivetimer > self.bombdelay:
                    self.bombsdeployed = True
                    distance = 27
                    for i in range(-2, 3):
                        dropbomb([self.pos[0] + i * distance, -20], Vector2d(0.0, 1.0), random.randint(20, 27), self.terrain, self.wind, self.entities, self.player, 10.0, self.color)

            else:
                self.delete = True

    def _forcedrag(self):
        dragtotal = self.Cd * self.S * 0.5 * self.rho * self.velocity.lengthsquared()
        return self.velocity.getuvec() * dragtotal

    # calculates the force of gravity in x and y direction
    def _forcegravity(self):
        return Vector2d(0, (self.g * self.m))