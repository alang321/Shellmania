import pygame
from Vector import Vector2d
from particles import particle

class teleportermissile:
    _name = "Teleporter"

    width = 9
    height = 9

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
        #main sprite
        self.sprite = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.sprite.get_rect()
        pygame.draw.circle(self.sprite, pygame.color.THECOLORS["white"], [int(self.rect.w / 2.0), int(self.rect.h / 2.0)], 4)
        return

    def draw(self, screen):
        screen.blit(self.sprite, [self.pos[0] - (self.rect.w / 2), self.pos[1] - self.rect.h/2])

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
                #set player x position to own x position
                self.player.pos[0] = self.pos[0]

                #set player on ground and update turret
                self.player.setonground()
                self.player.updateTurret()

                #white explosion particle at player position
                radius = 23
                surface = pygame.Surface([radius * 2 + 5, radius * 2 + 5])
                surface.fill((0, 0, 0))
                surface.set_colorkey((0, 0, 0))
                pygame.draw.circle(surface, pygame.color.THECOLORS["white"], (int(surface.get_rect().w / 2), int(surface.get_rect().h / 2)), radius)
                particle(self.player.pos, surface, 2.5, Vector2d(0.0, 0.0), 0.0, 0.0, self.entities[2], True, 0.3)

                #delete missile
                self.delete = True
        else:
            self.delete = True


    def _forcedrag(self):
        dragtotal = self.Cd * self.S * 0.5 * self.rho * self.velocity.length() ** 2
        return self.velocity.getuvec() * dragtotal

    # calculates the force of gravity in x and y direction
    def _forcegravity(self):
        return Vector2d(0, (self.g * self.m))