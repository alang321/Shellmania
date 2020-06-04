import pygame
from Vector import Vector2d
from explosion import explosion
from particles import particle


class missile:
    _name = "Missile"

    width = 6
    height = 6

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

        #trail particle
        self.trailcounter = 0
        self.traillength = 5
        self.trailhistory = [None] * self.traillength
        self.trailinterval = 0.001
        self.timesincetrail = self.trailinterval
        self.currentindex = self.traillength-1
        return

    def draw(self, screen):
        #draw the trail
        #first from current pos to last point
        pygame.draw.line(screen, self.color, self.pos, self.trailhistory[self.currentindex], 4)
        # then all the other ones
        counter = 0
        for i in range(self.currentindex, self.currentindex - self.traillength+1, -1):
            counter += 1
            if self.trailhistory[i-1] == None:
                break
            else:
                pygame.draw.line(screen, self.color, self.trailhistory[i], self.trailhistory[i-1], 4)

    def update(self, dt):
        #this list holds all the forces acting on the missile
        forces = [self._forcedrag(), self._forcegravity(), self.wind.force]

        #update position and velocity depeneing on the timestep
        for i in range(2):
            self.velocity[i] += (sum([j[i] for j in forces]) / self.m) * dt
            self.pos[i] += 20.0 * self.velocity[i] * dt

        #trail system
        self.timesincetrail += dt
        if self.timesincetrail >= self.trailinterval:
            self.timesincetrail = 0.0
            self.currentindex = self.trailcounter % self.traillength
            self.trailhistory[self.currentindex] = self.pos.copy()
            self.trailcounter += 1


        #if new pos is outside bounds delete
        if 0 < self.pos[0] < self.terrain.bounds[0] - 1.0:
            #if new pos is under ground explode
            if self.terrain.heightmap[int(self.pos[0])] < self.pos[1]:
                explosion(self.pos, self.terrain, self.entities, self.player, 20, 0.7, 0.3)
                self.delete = True
        else:
            self.delete = True


    def _forcedrag(self):
        dragtotal = self.Cd * self.S * 0.5 * self.rho * self.velocity.length() ** 2
        return self.velocity.getuvec() * dragtotal

    # calculates the force of gravity in x and y direction
    def _forcegravity(self):
        return Vector2d(0, (self.g * self.m))