import pygame
import numpy as np
from missile import missile
from Vector import Vector2d
from particles import particle
import random

class player:
    #drawing
    body = ((0, 15.0), (2.5, 20.0), (22.5, 20.0), (25, 15), (18.5, 15.0), (15.5, 12.0), (9.5, 12.0), (6.5, 15.0))
    #turret length in pixel
    turretLength = 13.0
    #turret origin distance from ground
    turretstart = 5.0
    #maximum turrent angle in radians
    maxturretangle = 90.0 * (np.pi/180.0)
    width = 25.0
    height = 40.0

    key_fire = pygame.K_SPACE
    key_left = pygame.K_a
    key_right = pygame.K_d

    smokeinterval = 0.1

    def __init__(self, name, terrain, wind, entities, aliveplayers, color=pygame.color.THECOLORS["red"]):
        #references
        self.entities = entities
        self.entities[0].append(self)
        self.terrain = terrain
        self.aliveplayers = aliveplayers
        self.wind = wind

        self.color = color
        self.name = name
        #helath from 0 to 1
        self.health = 1.0

        #counters
        self.shotcounter = 0
        self.kills = 0
        self.wins = 0

        #shooting
        self.shootingstarttime = 0.0
        self.minshotpower = 0.1
        self.shotcharging = False
        self.fullpowershottime = 1.5  # time to charge full power shot in seconds

        # player name font
        self.font = pygame.font.SysFont('Arial', 10)

        #turret
        self.turretVector = Vector2d(random.randint(-5.0, 5.0), -5.0).getuvec()
        self.turretEndpoint = []
        self.turretOrigin = []

        # speed in pixels per second
        self.speed = 50.0
        #if moving left or right
        self.left = False
        self.right = False

        #surfaces
        #smoke surface
        self.timesincesmoke = 0.0
        smoke = pygame.Surface([7 * 2 + 5, 7 * 2 + 5])
        smoke.fill((0, 0, 0))
        smoke.set_colorkey((0, 0, 0))
        pygame.draw.circle(smoke, pygame.color.THECOLORS["grey"], (int(smoke.get_rect().w / 2), int(smoke.get_rect().h / 2)), 7)
        self.smoke = smoke
        #fire
        fireorange = pygame.Surface([7 * 2 + 5, 7 * 2 + 5])
        fireorange.fill((0, 0, 0))
        fireorange.set_colorkey((0, 0, 0))
        pygame.draw.circle(fireorange, pygame.color.THECOLORS["orange"], (int(fireorange.get_rect().w / 2), int(fireorange.get_rect().h / 2)), 4)
        self.fireorange = fireorange
        #body
        self.sprite = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        #text
        self.textsurface = self.font.render(self.name, False, self.color)

        #toggles
        self.drawToggle = True
        self.delete = False
        self.controlActive = False
        self.destroyed = False
        return

    def respawn(self, xpos):
        self.pos = [float(xpos), 0.0]

        self.kills = 0
        self.health = 1.0
        self.controlActive = False
        self.left = False
        self.right = False
        self.shotcharging = False
        self.destroyed = False
        self.shotcounter = 0

    def _setonground(self):
        #get height at x loaction from terrain
        height = float(self.terrain.heightmap[int(self.pos[0])])

        relpos = self.pos[0] - float(int(self.pos[0])) - 0.5

        if relpos < 0:
            heightdifference = height - float(self.terrain.heightmap[max(int(self.pos[0]) - 1, 0)])
        else:
            heightdifference = height - float(self.terrain.heightmap[min(int(self.pos[0]) + 1, self.terrain.bounds[0] - 1)])

        self.pos[1] = height - heightdifference * abs(relpos)


    def update(self, dt):
        #smoke system
        if self.destroyed:
            self.timesincesmoke += dt
            if self.timesincesmoke > self.smokeinterval:
                self.timesincesmoke = 0.0 + 0.1 * self.smokeinterval * random.randint(0, 3)
                dir = Vector2d(random.randint(-5, 5), -38.0).getuvec()
                smoke = pygame.Surface([7 * 2 + 5, 7 * 2 + 5])
                smoke.set_colorkey((0, 0, 0))
                smoke.blit(self.smoke, (0, 0))
                particle(self.pos.copy(), smoke, random.randint(2, 5), dir, 1.75, 0.19, self.entities[2], True, self.wind, False, 10.0)

        #move in the direction of movedir,if movedir is 0 dont move
        if self.left:
            self.move(dt, -1.0)
        elif self.right:
            self.move(dt, 1.0)

        #calcualte turrent origin and endpoint
        self.turretOrigin = [self.pos[0] + self.turretstart * self.terrain.normalmap[int(self.pos[0])].x, self.pos[1] + self.turretstart * self.terrain.normalmap[int(self.pos[0])].y]
        #get the turrent direction as a unit vector
        self.turretVector = self._getTurretUnitVector()
        #caclulates the endpoint of the turrent
        self.turretEndpoint = [self.turretOrigin[0] + self.turretLength * self.turretVector.x, self.turretOrigin[1] + self.turretLength * self.turretVector.y]

        #set on ground
        self._setonground()
        return

    #draw the tank with the current values for position and angle
    def draw(self, screen):
        if self.drawToggle:
            self.sprite.fill((0, 0, 0, 0))
            #turret
            pygame.draw.line(screen, self.color, self.turretOrigin, self.turretEndpoint, 3)
            #body
            pygame.draw.polygon(self.sprite, self.color, self.body)

            #rotate body
            rotated = pygame.transform.rotate(self.sprite, np.rad2deg(self.terrain.normalmap[int(self.pos[0])].find360CCWAngle(Vector2d(0.0, -1.0))))

            #draw
            screen.blit(rotated, (self.pos[0] - rotated.get_width() / 2.0, self.pos[1] - rotated.get_height() / 2.0))
        #draw text and health bar
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, ((self.pos[0]-13, self.pos[1]-33), (26, 4)), 1)
            pygame.draw.rect(screen, self.color, ((self.pos[0]-13, self.pos[1]-33), (26*max(self.health, 0.0), 4)))
            screen.blit(self.textsurface, (self.pos[0]-self.textsurface.get_rect().w/2, self.pos[1]-50))
        return

    #moves into dir, which should be positive or negative 1, left neg, right pos
    def move(self, dt, movedir):
        if self.controlActive and movedir != 0.0:
            #movement direction vector, normal vector to the surface normal
            dirvector = -movedir * self.terrain.normalmap[int(self.pos[0])].getnormalvec()

            newx = self.pos[0] + dirvector.x * dt * self.speed

            #checks if newpos is in bounds and if height difference exceeds maximum
            if 0 < newx < self.terrain.bounds[0] - 1 and abs(self.terrain.heightmap[int(max(min(self.pos[0]+movedir*5, self.terrain.bounds[0]-1), 0.0))] - self.terrain.heightmap[int(max(min(self.pos[0]+movedir*3, self.terrain.bounds[0]-1), 0.0))]) < 22:
                self.pos[0] = newx

    def firekeyevent(self, eventtype, elapsedtime):
        if self.controlActive:
            if eventtype == pygame.KEYDOWN:
                self.shotcharging = True
                self.shootingstarttime = elapsedtime
            elif eventtype == pygame.KEYUP and self.shotcharging:
                self.shotcharging = False
                self.fire(min(max((elapsedtime - self.shootingstarttime) / self.fullpowershottime, self.minshotpower), 1.0))
        else:
            self.shotcharging = False

    #shoot a missile in turret vect direction
    def fire(self, shootingpower):
        if self.controlActive:
            self.shotcounter += 1
            missile(self.turretEndpoint.copy(), self.turretVector.copy(), 22.0*shootingpower, self.terrain, self.wind, self.entities, self, 1.0, self.color)
            particle(self.turretEndpoint.copy(), self.fireorange, 0.5, self.turretVector.copy(), 1.5, 1.0, self.entities[2], True)

    #substract damage from health, if helath nis les than 0 set to destroyed
    def hit(self, damage, player):
        if not self.destroyed:
            self.health -= damage

            #if health <0 player is destroyed
            if self.health <= 0.0:
                self.health = 0.0
                self.destroyed = True
                self.controlActive = False
                self.aliveplayers.remove(self)
                if player != self:
                    player.kills += 1
            return

    #return the turret angle limited by bounds
    def _getTurretUnitVector(self):
        target = [float(i) for i in pygame.mouse.get_pos()]


        if self.turretOrigin != target and self.controlActive:
            mousevec = Vector2d.getvectorfrompoints(self.turretOrigin, target).getuvec()

            angle = mousevec.find360CCWAngle(self.terrain.normalmap[int(self.pos[0])])

            if self.maxturretangle < angle < 2 * np.pi - self.maxturretangle:
                if np.pi < angle:
                    return self.terrain.normalmap[int(self.pos[0])].getrotatedvect(self.maxturretangle)
                else:
                    return self.terrain.normalmap[int(self.pos[0])].getrotatedvect(-self.maxturretangle)

            return mousevec
        else:
            angle = self.turretVector.find360CCWAngle(self.terrain.normalmap[int(self.pos[0])])

            if self.maxturretangle < angle < 2 * np.pi - self.maxturretangle:
                if np.pi < angle:
                    return self.terrain.normalmap[int(self.pos[0])].getrotatedvect(self.maxturretangle)
                else:
                    return self.terrain.normalmap[int(self.pos[0])].getrotatedvect(-self.maxturretangle)

            return self.turretVector