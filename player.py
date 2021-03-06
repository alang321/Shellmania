import pygame
import numpy as np
from projectiles.bouncybomb import bouncybomb
from projectiles.missile import missile
from projectiles.airstrike import airstrike
from projectiles.teleportermissile import teleportermissile
from projectiles.nuke import nuke
from Vector import Vector2d
import random
from particles import particle
from playerinventory import playerinventory

class player:

    #this holds the current player if there is one
    _currentplayer = None

    weapon = bouncybomb

    #drawing
    body = ((0, 15.0), (2.5, 20.0), (22.5, 20.0), (25, 15), (18.5, 15.0), (15.5, 12.0), (9.5, 12.0), (6.5, 15.0))
    #turret length in pixel
    turretLength = 13.0
    #turret origin distance from ground
    turretstart = 5.0
    width = 25.0
    height = 40.0

    smokeinterval = 0.1

    def __init__(self, settings, name, terrain, wind, entities, aliveplayers, color=pygame.color.THECOLORS["red"]):
        #references
        self.entities = entities
        self.entities[0].append(self)
        self.terrain = terrain
        self.aliveplayers = aliveplayers
        self.wind = wind
        self.settings = settings

        #default inventory
        nrmissile = -1 if self.settings.inventory['Infinite missiles'] else self.settings.inventory['Amount missile']
        nrbouncybomb = -1 if self.settings.inventory['Infinite bouncybombs'] else self.settings.inventory['Amount bouncybomb']
        nrairstrike = -1 if self.settings.inventory['Infinite airstrikes'] else self.settings.inventory['Amount airstrike']
        nrteleporter = -1 if self.settings.inventory['Infinite teleporters'] else self.settings.inventory['Amount teleporter']
        nrnukes = -1 if self.settings.inventory['Infinite nukes'] else self.settings.inventory['Amount nuke']

        self.defaultinventory = playerinventory([missile, bouncybomb, airstrike, teleportermissile, nuke], [nrmissile, nrbouncybomb, nrairstrike, nrteleporter, nrnukes], 0, self)

        #maximum height difference the player can drive over
        self.maxheightdiff = self.settings.gamevalues['Max height diff']


        # maximum turrent angle in radians
        self.maxturretangle = self.settings.gamevalues["Max turret angle"] * (np.pi / 180.0)

        #fuel in seconds
        self.usefuel = self.settings.gamevalues["Enable fuel"]
        self.initialfuel = float(self.settings.gamevalues["Initial fuel"])
        self.fuel = self.initialfuel

        self.color = color
        self.name = name
        #helath from 0 to 1
        self.initialhealth = self.settings.gamevalues["Initial health"]
        self.health = self.initialhealth

        #counters
        self.shotcounter = 0
        self.kills = 0
        self.wins = 0

        # set to true if tank is at a new position, so that body gets redrawn
        self.newpos = True

        #shooting
        self.shootingstarttime = 0.0
        self.minshotpower = 0.1
        self.shotcharging = False
        self.fullpowershottime = self.settings.gamevalues["Fullpower shot time"] # time to charge full power shot in seconds
        self.shootingratio = self.settings.gamevalues["Shot power"]

        # player name font
        self.font = pygame.font.SysFont('Calibri', 11)

        #turret
        self.turretVector = Vector2d(0.0, -1.0)
        self.turretEndpoint = []
        self.turretOrigin = []

        # speed in pixels per second
        self.speed = self.settings.gamevalues["Player speed"]
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
        fireorange = pygame.Surface([7 * 2 + 2, 7 * 2 + 2])
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

        self.fuel = self.initialfuel

        self.kills = 0
        self.health = self.initialhealth
        self.controlActive = False
        self.left = False
        self.right = False
        self.shotcharging = False
        self.destroyed = False
        self.shotcounter = 0

        #inventory
        self.inventory = self.defaultinventory.copy()

        #set tank on ground and update turret vector
        self.setonground()
        self.turretVector = Vector2d(random.randint(-5.0, 5.0), -5.0).getuvec()
        self.updateTurret()

    def setonground(self):
        #get height at x loaction from terrain
        height = float(self.terrain.heightmap[int(self.pos[0])])

        relpos = self.pos[0] - float(int(self.pos[0])) - 0.5

        if relpos < 0:
            heightdifference = height - float(self.terrain.heightmap[max(int(self.pos[0]) - 1, 0)])
        else:
            heightdifference = height - float(self.terrain.heightmap[min(int(self.pos[0]) + 1, self.terrain.bounds[0] - 1)])

        self.pos[1] = height - heightdifference * abs(relpos)

        self.newpos = True


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
                particle(self.pos.copy(), smoke, random.randint(2, 5), dir, 1.75, 0.19, self.entities[2], True, 0.0, self.wind, 8.0)

        if self.controlActive:
            #move in the direction of movedir,if movedir is 0 dont move
            if self.left:
                self.move(dt, -1.0)
            elif self.right:
                self.move(dt, 1.0)

            self.updateTurret()
            return

    #draw the tank with the current values for position and angle
    def draw(self, screen):
        if self.drawToggle:
            self.sprite.fill((0, 0, 0, 0))
            #turret
            pygame.draw.line(screen, self.color, self.turretOrigin, self.turretEndpoint, 3)

            #only draw rotated body when pos is updated
            if self.newpos:
                self.newpos = False
                #body
                pygame.draw.polygon(self.sprite, self.color, self.body)
                #rotate body
                self.rotatedbody = pygame.transform.rotate(self.sprite, np.rad2deg(self.terrain.normalmap[int(self.pos[0])].findCCWAngle(Vector2d(0.0, -1.0))))

            #draw
            screen.blit(self.rotatedbody, (self.pos[0] - self.rotatedbody.get_width() / 2.0, self.pos[1] - self.rotatedbody.get_height() / 2.0))

            #draw text and health bar
            if not self.destroyed:
                #fuelbar
                if self.usefuel:
                    pygame.draw.rect(screen, self.color, ((self.pos[0]-13, self.pos[1]-28), (26, 4)), 1)
                    pygame.draw.rect(screen, self.color, ((self.pos[0]-13, self.pos[1]-28), (26*max(self.fuel/self.initialfuel, 0.0), 4)))

                #health bar
                pygame.draw.rect(screen, self.color, ((self.pos[0]-13, self.pos[1]-33), (26, 4)), 1)
                pygame.draw.rect(screen, self.color, ((self.pos[0]-13, self.pos[1]-33), (26*max(self.health/self.initialhealth, 0.0), 4)))

                screen.blit(self.textsurface, (self.pos[0]-self.textsurface.get_rect().w/2, self.pos[1]-50))
        return

    #this method gets called when the players is moved, or when explosion happens, so it falls on ground
    def updateTurret(self):
        #calcualte turrent origin and endpoint
        self.turretOrigin = [self.pos[0] + self.turretstart * self.terrain.normalmap[int(self.pos[0])].x, self.pos[1] + self.turretstart * self.terrain.normalmap[int(self.pos[0])].y]
        #get the turrent direction as a unit vector
        self.turretVector = self._getTurretUnitVector()
        #caclulates the endpoint of the turrent
        self.turretEndpoint = [self.turretOrigin[0] + self.turretLength * self.turretVector.x, self.turretOrigin[1] + self.turretLength * self.turretVector.y]

    def nextitem(self):
        if self.controlActive:
            self.inventory.nextnonzero()

    def previousitem(self):
        if self.controlActive:
            self.inventory.previousnonzero()

    #moves into dir, which should be positive or negative 1, left neg, right pos
    def move(self, dt, movedir):
        if self.fuel >= 0 or not self.usefuel:
            #movement direction vector, normal vector to the surface normal
            dirvector = -movedir * self.terrain.normalmap[int(self.pos[0])].getnormalvec()

            newx = self.pos[0] + dirvector.x * dt * self.speed

            #checks if newpos is in bounds and if height difference exceeds maximum
            if 0 < newx < self.terrain.bounds[0] - 1 and abs(self.terrain.heightmap[int(max(min(self.pos[0]+movedir*5, self.terrain.bounds[0]-1), 0.0))] - self.terrain.heightmap[int(max(min(self.pos[0]+movedir*3, self.terrain.bounds[0]-1), 0.0))]) <= self.maxheightdiff:
                self.fuel -= dt
                self.pos[0] = newx
                self.setonground()

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
            weapon = self.inventory.usecurrent(True)
            if weapon != None:
                self.shotcounter += 1
                weapon(self.turretEndpoint.copy(), self.turretVector.copy(), self.terrain.bounds[0]*0.02*self.shootingratio*shootingpower, self.terrain, self.wind, self.entities, self, 1.0, self.color)
                particle(self.turretEndpoint.copy(), self.fireorange, 0.5, self.turretVector.copy(), 1.5, 1.0, self.entities[2], True)

    #substract damage from health, if helath nis les than 0 set to destroyed
    def hit(self, damage, player):
        if not self.destroyed:
            self.health -= damage

            #if health <0 player is destroyed
            if self.health <= 0.0:
                self.health = 0.0
                self.destroyed = True
                #if self is the current player dont remove from aliveplayers, so index can be found and a switch to next tplayer can be made, it is removed from the aliveplayer list in turnlogic
                if not self == player._currentplayer:
                    self.aliveplayers.remove(self)

                self.controlActive = False
                if player != self:
                    player.inventory.addtoitemamount(nuke, 1)
                    player.kills += 1
            return

    #return the turret angle limited by bounds
    def _getTurretUnitVector(self):
        if self.controlActive:
            target = [float(i) for i in pygame.mouse.get_pos()]

            if self.turretOrigin != target:
                mousevec = Vector2d.getvectorfrompoints(self.turretOrigin, target).getuvec()

                return self._limitvecangle(mousevec, self.terrain.normalmap[int(self.pos[0])])
        else:
            return self._limitvecangle(self.turretVector, self.terrain.normalmap[int(self.pos[0])])

    #return the vector limited by the maximum angle bounds
    def _limitvecangle(self, target, reference):

        angle = target.findCCWAngle(reference)

        #if outside of limit return rotated to max angle, else return target vector
        if self.maxturretangle < angle < 2 * np.pi - self.maxturretangle:
            if np.pi < angle:
                return reference.getrotatedvect(self.maxturretangle)
            else:
                return reference.getrotatedvect(-self.maxturretangle)
        else:
            return target
