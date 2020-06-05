import pygame
import pygame.gfxdraw
from Vector import Vector2d
from particles import particle
from particles import bouncyparticle
import random

class explosion:

    def __init__(self, pos, terrain, entities, player, r=10.0, damage=0.8, maxdropoff=0.5, particlescaling=1.2):
        #references
        self.playerlist = entities[0]
        self.particlelist = entities[2]
        #player that fired the missile that spawned the explosion
        self.player = player
        self.terrain = terrain

        #position
        self.pos = pos
        if self.pos[1] > self.terrain.bounds[1] - self.terrain.bedrockheight - 1:
            self.pos[1] = self.terrain.bounds[1] - self.terrain.bedrockheight - 1

        #max damage
        self.damage = damage
        #damage ratio at maximum distance from pos
        self.maxdamagedropoff = maxdropoff
        self.blastradius = r
        #for faster distance calculation
        self.blastradiussquared = self.blastradius**2

        #spawn explosion particles
        self._explosionparticles(particlescaling)

        #calculate which players where hit andd for how much damage
        self._playerhits()
        #destroy the terrain in a circular pattern around pos
        self._destroyterrain()

        #set all players on ground
        self._setplayersonground()
        return

    def _explosionparticles(self, particlescaling):
        dirt = pygame.Surface([4, 4])
        dirt.fill((0, 0, 0))
        dirt.set_colorkey((0, 0, 0))
        #pygame.gfxdraw.filled_circle(dirt, int(dirt.get_rect().w/2), int(dirt.get_rect().h/2), 2, self.terrain.groundcolor)
        pygame.draw.rect(dirt, self.terrain.groundcolor, ((0, 0), (4, 4)))

        normalvec = self.terrain.normalmap[int(self.pos[0])]
        surfacevec = self.terrain.normalmap[int(self.pos[0])].getnormalvec()
        for i in range(int(self.blastradius * particlescaling)):
            direction = (normalvec * (random.randint(-50, 400)/10.0) + (random.randint(-80, 80)/10.0) * surfacevec).getuvec()
            velocity = random.randint(0, 1100)/100.0
            bouncyparticle(self.pos.copy(), self.terrain, dirt, 3.0, direction, velocity, self.particlelist, True, 2.0, None, 1000, 0.3)

        #explosion particle surface
        surface = pygame.Surface([self.blastradius*2+10, self.blastradius*2+10])
        surface.fill((0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        pygame.gfxdraw.filled_circle(surface, int(surface.get_rect().w/2), int(surface.get_rect().h/2), int(self.blastradius+2), pygame.color.THECOLORS["orange"])
        particle(self.pos, surface, 2.5, Vector2d(0.0, 0.0), 0.0, 0.0, self.particlelist, True, 0.3)

    #get distance from explosion center to all players and call hit function if hit
    def _playerhits(self):
        for i in self.playerlist:
            distance = self._distance(i.pos, self.pos)
            if distance < self.blastradius + i.width/2:
                i.hit(self.damage-self.damage*(distance/self.blastradius)*self.maxdamagedropoff, self.player)

    def _setplayersonground(self):
        for i in self.playerlist:
            i.setonground()
            i.updateTurret()

    #get the distance between two points
    def _distance(self, pos1, pos2):
        return Vector2d.getvectorfrompoints(pos2, pos1).length()

    def _distancesquared(self, pos1, pos2):
        return (pos2[0]-pos1[0])**2 + (pos2[1] - pos1[1])**2

    def _destroyterrain(self):
        rangex = range(int(max(self.pos[0] - self.blastradius, 0)),
                       int(min(self.pos[0] + self.blastradius, self.terrain.bounds[0])))
        rangey = range(int(max(self.pos[1] - self.blastradius, 0)),
                       int(min(self.pos[1] + self.blastradius, self.terrain.bounds[1] - self.terrain.bedrockheight)))

        for i in rangex:
            for j in rangey:
                if self._distancesquared([i, j], self.pos) < self.blastradiussquared:
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
