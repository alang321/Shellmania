from Vector import Vector2d
import numpy as np

class particle:
    _enabled = True
    g = 9.80665

    def __init__(self, pos, surface, duration, dir, velocity, slowdown, particles, fadeout=True, fadeoutstart=0.0, wind=None, m=1.0):
        if particle._enabled:
            #entitiy list
            particles.append(self)
            self.delete = False

            # pos vel, vel is a vector2d
            self.pos = pos
            self.velocity = velocity * dir

            #forces
            self.wind = wind
            self.m = m
            if self.wind != None:
                self.windeffect = True
            else:
                self.windeffect = False

            #if particle shouild fade out linearly
            self.fadeout = fadeout
            #when the fadeout starts in seconds
            self.fadeoutstart = fadeoutstart
            #how long the partile lives
            self.duration = float(duration)
            #loose this percentage of velocity each second
            self.slowdown = slowdown

            #time to lkeep track of how long particle has been alive
            self.timer = 0.0

            #surface
            self.surface = surface
            self.rect = self.surface.get_rect()

#draw the particle
    def draw(self, screen):
        screen.blit(self.surface, (self.pos[0] - self.surface.get_rect().w/2, self.pos[1] - self.surface.get_rect().h/2))

#update the particle
    def update(self, dt):
        self.timer += dt

        # if particle hasnt exceeded its predesignated life duration
        if self.timer < self.duration:
            #percentage of the total particel life

            forces = []
            if self.windeffect:
                forces.append(self.wind.force)

            #change pos
            for i in range(2):
                self.velocity[i] += (sum([j[i] for j in forces]) / self.m) * dt
                self.pos[i] += 20.0 * self.velocity[i] * dt

            # if fadeout set opacity linearly from 100%-0% from start to end
            if self.fadeout:
                percentage = (self.timer - self.fadeoutstart)/(self.duration-self.fadeoutstart)
                self.surface.set_alpha(255 - 255 * percentage)

            #adjust velocity
            for i in range(len(self.velocity)):
                self.velocity[i] *= 1.0 - self.slowdown * dt
        else:
            self.delete = True

    # calculates the force of gravity in x and y direction
    def _forcegravity(self):
        return Vector2d(0, (self.g * self.m))


class bouncyparticle:
    g = 9.80665

    _enabled = True

    def __init__(self, pos, terrain, surface, duration, dir, velocity, particles, fadeout=True, fadeoutstart=0.0, wind=None, m=1.0, coeffrest=0.6):
        if bouncyparticle._enabled:
            #entitiy list
            particles.append(self)
            self.delete = False

            #bouncing
            self.terrain = terrain
            self.coeffrest = coeffrest
            #more efficienct
            self.atrest = False
            self.minspeed = 0.1

            # pos vel, vel is a vector2d
            self.pos = pos
            self.velocity = velocity * dir

            #forces
            self.wind = wind
            self.m = m
            if self.wind != None:
                self.windeffect = True
            else:
                self.windeffect = False

            #if particle shouild fade out linearly
            self.fadeout = fadeout
            #when the fadeout starts in seconds
            self.fadeoutstart = fadeoutstart
            #how long the partile lives
            self.duration = float(duration)

            #time to lkeep track of how long particle has been alive
            self.timer = 0.0

            #surface
            self.surface = surface
            self.rect = self.surface.get_rect()

#draw the particle
    def draw(self, screen):
        screen.blit(self.surface, (self.pos[0] - self.surface.get_rect().w/2, self.pos[1] - self.surface.get_rect().h/2))

#update the particle
    def update(self, dt):
        self.timer += dt

        # if particle hasnt exceeded its predesignated life duration
        if self.timer < self.duration:

            forces = [self._forcegravity()]
            if self.windeffect:
                forces.append(self.wind.force)
            for i in range(2):
                self.velocity[i] += (sum([j[i] for j in forces]) / self.m) * dt
                self.pos[i] += 20.0 * self.velocity[i] * dt

            # if fadeout set opacity linearly from 100%-0% from start to end
            if self.fadeout:
                percentage = (self.timer - self.fadeoutstart)/(self.duration-self.fadeoutstart)
                self.surface.set_alpha(255 - 255 * percentage)

            if 0 < self.pos[0] < self.terrain.bounds[0]-1: # check if in bounds to avoid out of bounds array call in next line
                if self.pos[1] >= self.terrain.heightmap[int(self.pos[0])]: # check if at groundlevel
                    # vector in the opposite direction of the curren velocity
                    opposite = -1 * self.velocity

                    newposset = False

                    steps = 5
                    for i in range(1, steps + 1):
                        # go back in a certain number of steps
                        vec = opposite * (i / float(steps)) * 20.0 * dt
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
                self.delete = True
        else:
            self.delete = True

    # calculates the force of gravity in x and y direction
    def _forcegravity(self):
        return Vector2d(0, (self.g * self.m))