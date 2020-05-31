import pygame

class particle:
    def __init__(self, pos, surface, duration, dir, velocity, slowdown, particles, fadeout=True, scale=1.0):
        self.delete = False
        self.pos = pos
        self.velocity = [dir[0] * velocity, dir[1] * velocity]

        self.fadeout = fadeout

        self.surface = surface
        self.rect = self.surface.get_rect()

        self.scale = scale

        self.duration = float(duration)

        self.timer = 0.0

        #loose this percentage of velocity each second
        self.slowdown = slowdown

        particles.append(self)

    def draw(self, screen):
        screen.blit(self.surface, (self.pos[0] - self.surface.get_rect().w/2, self.pos[1] - self.surface.get_rect().h/2))


    def update(self, dt):
        self.timer += dt

        if self.timer < self.duration:
            percentage = (self.timer/self.duration)
            for i in range(2):
                self.pos[i] += self.velocity[i] * dt

            if self.fadeout:
                self.surface.set_alpha(255 - 255 * percentage)



            #self.surface = pygame.transform.scale(self.surface, (int(self.rect.w + self.rect.w * (self.scale-1) * percentage), int(self.rect.h + self.rect.h * (self.scale-1) * percentage)))

            self.velocity = [i - i * self.slowdown * dt for i in self.velocity]
        else:
            self.delete = True