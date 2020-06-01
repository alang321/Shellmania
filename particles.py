class particle:
    def __init__(self, pos, surface, duration, dir, velocity, slowdown, particles, fadeout=True):
        #entitiy list
        particles.append(self)
        self.delete = False

        # pos vel, vel is a vector2d
        self.pos = pos
        self.velocity = velocity * dir

        #if particle shouild fade out linearly
        self.fadeout = fadeout
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
            percentage = (self.timer/self.duration)

            #change pos
            for i in range(2):
                self.pos[i] += self.velocity[i] * dt

            # if fadeout set opacity linearly from 100%-0% from start to end
            if self.fadeout:
                self.surface.set_alpha(255 - 255 * percentage)

            #adjust velocity
            for i in range(len(self.velocity)):
                self.velocity[i] *= 1.0 - self.slowdown * dt
        else:
            self.delete = True