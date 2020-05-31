import pygame
import numpy as np
from missile import missile
from Vector import Vect
from particles import particle
import random
import pygame.gfxdraw

class tank:
    #counts how many instances there are
    _counter = 0

    #drawing
    body = ((0, 15.0), (2.5, 20.0), (22.5, 20.0), (25, 15), (18.5, 15.0), (15.5, 12.0), (9.5, 12.0), (6.5, 15.0))
    #turret length in pixel
    turretLength = 13.0
    #turret origin distance from ground
    turretstart = 5.0
    width = 25.0
    height = 40.0

    m = 10000
    g = 9.80065

    key_fire = pygame.K_SPACE
    key_left = pygame.K_a
    key_right = pygame.K_d

    smokeinterval = 0.1



    def __init__(self, name, xpos, terrain, entities, color=pygame.color.THECOLORS["red"]):
        tank._counter += 1
        self.number = tank._counter
        self.health = 1

        self.entities = entities
        self.entities[0].append(self)

        #playercontrolled
        self.turretVector = [0.0, -1.0]
        self.turretEndpoint = []
        self.turretOrigin = []
        self.shootingPower = 0.0


        # speed in pixels per second
        self.speed = 50.0

        #toggles
        self.drawToggle = True



        self.font = pygame.font.SysFont('Arial', 10)


        if name == "":
            self.name = "Player " + str(self.number)
        else:
            self.name = name

        self.color = color
        self.terrain = terrain



        self.timesincesmoke = 0.0
        smoke = pygame.Surface([7 * 2 + 5, 7 * 2 + 5])
        smoke.fill((0, 0, 0))
        smoke.set_colorkey((0, 0, 0))
        pygame.gfxdraw.filled_circle(smoke, int(smoke.get_rect().w / 2), int(smoke.get_rect().h / 2), 7, pygame.color.THECOLORS["grey"])
        self.smoke = smoke

        fireorange = pygame.Surface([7 * 2 + 5, 7 * 2 + 5])
        fireorange.fill((0, 0, 0))
        fireorange.set_colorkey((0, 0, 0))
        pygame.gfxdraw.filled_circle(fireorange, int(fireorange.get_rect().w / 2), int(fireorange.get_rect().h / 2), 4, pygame.color.THECOLORS["orange"])
        self.fireorange = fireorange

        self.sprite = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.sprite.get_rect()

        self.controlActive = False
        self.delete = False
        self.destroyed = False

        self.pos = [float(xpos), 0.0]
        self._setonground()
        return

    def _setonground(self):
        #get height at x loaction from terrain
        height = float(self.terrain.heightmap[int(self.pos[0])])

        relpos = self.pos[0] - float(int(self.pos[0])) - 0.5

        if relpos < 0:
            heightdifference = height - float(self.terrain.heightmap[max(int(self.pos[0]) - 1, 0)])
        else:
            heightdifference = height - float(self.terrain.heightmap[min(int(self.pos[0]) + 1, self.terrain.bounds[0]-1)])

        self.pos[1] = height - heightdifference * abs(relpos)


    def update(self, dt):
        if self.destroyed:
            self.timesincesmoke += dt
            if self.timesincesmoke > self.smokeinterval:
                self.timesincesmoke = 0.0 + 0.1 * self.smokeinterval * random.randint(0, 3)
                dir = [random.randint(-5, 5), -38.0]
                norm = dir/np.linalg.norm(dir)
                smoke = pygame.Surface([7 * 2 + 5, 7 * 2 + 5])
                smoke.set_colorkey((0, 0, 0))
                smoke.blit(self.smoke, (0, 0))
                particle(self.pos.copy(), smoke, random.randint(2, 5), norm, 35.0, 0.19, self.entities[2], True, 5.0)

        #calcualte turrent origin and endpoint
        self.turretOrigin = [self.pos[0] + self.turretstart * self.terrain.normalmap[int(self.pos[0])].x, self.pos[1] + self.turretstart * self.terrain.normalmap[int(self.pos[0])].y]
        self.turretVector = self._getTurretUnitVector()
        #caclulates the endpoint of the turrent
        self.turretEndpoint = [self.turretOrigin[0] + self.turretLength * self.turretVector[0], self.turretOrigin[1] + self.turretLength * self.turretVector[1]]

        #set on ground
        self._setonground()
        return

    def fire(self, shootingpower):
        if self.controlActive:
            missile(self.turretEndpoint.copy(), self.turretVector.copy(), 22.0*shootingpower, self.terrain, self.entities, 1.0, self.color)
            particle(self.turretEndpoint.copy(), self.fireorange, 0.5, self.turretVector, 20.0, 1.0, self.entities[2], True)

    #move, moves right if true is passed
    def move(self, dir, dt):

        if self.controlActive:
            dirvector = [dir * -self.terrain.normalmap[int(self.pos[0])].y, dir * self.terrain.normalmap[int(self.pos[0])].x]

            newx = self.pos[0] + dirvector[0] * dt * self.speed

            #pygame.draw.line(screen, pygame.color.THECOLORS["white"], [self.pos[0], self.pos[1]], [self.pos[0] + dirvector[0] * 40, self.pos[1] + dirvector[1] * 40], 2)

            if 0 < newx < self.terrain.bounds[0] - 1 and abs(self.terrain.heightmap[int(max(min(self.pos[0]+dir*5, self.terrain.bounds[0]-1), 0.0))] - self.terrain.heightmap[int(max(min(self.pos[0]+dir*3, self.terrain.bounds[0]-1), 0.0))]) < 22:
                self.pos[0] = newx

    def hit(self, damage):
        if not self.destroyed:
            self.health -= damage

            if self.health <= 0.0:
                self.destroyed = True
                self.controlActive = False
            return

    #draw the tank with the current values for position and angle
    def draw(self, screen):
        if self.drawToggle:
            self.sprite.fill((0, 0, 0, 0))
            #pygame.draw.line(screen, self.color, self.turretOrigin, self.turretEndpoint, 3)
            pygame.draw.line(screen, self.color, self.turretOrigin, self.turretEndpoint, 3)
            pygame.draw.polygon(self.sprite, self.color, self.body)

            rotated = self._rotatetankaroundpos(self.sprite, self.terrain.normalmap[int(self.pos[0])].findCCWAngle(Vect(0.0, -1.0)))

            screen.blit(rotated, (self.pos[0] - rotated.get_width() / 2.0, self.pos[1] - rotated.get_height() / 2.0))
        if not self.destroyed:
            textsurface = self.font.render(self.name, False, self.color)
            pygame.draw.rect(screen, self.color, ((self.pos[0]-13, self.pos[1]-33), (26, 4)), 1)
            pygame.draw.rect(screen, self.color, ((self.pos[0]-13, self.pos[1]-33), (26*max(self.health, 0.0), 4)))
            screen.blit(textsurface, (self.pos[0]-textsurface.get_rect().w/2, self.pos[1]-50))
        return

    #rotates sprite around the pos of the tank, angle is CCW positive
    def _rotatetankaroundpos(self, surface, angle):
        rot_image = pygame.transform.rotate(surface, angle)
        return rot_image

    #return the turret angle limited by bounds
    def _getTurretUnitVector(self):
        target = [float(i) for i in pygame.mouse.get_pos()]

        if self.turretOrigin != target and self.controlActive:
            mousevec = [target[0] - self.turretOrigin[0], target[1] - self.turretOrigin[1]]

            umousevec = mousevec / np.linalg.norm(mousevec)
            return [umousevec[0], umousevec[1]]
        else:
            return self.turretVector

    def _forcegravity(self):
        return [0, (self.g * self.m)]