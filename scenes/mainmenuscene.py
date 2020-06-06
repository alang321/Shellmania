from scenes.settingsscene import settingsscene
from scenes.playercreationscene import playercreationscene
import pygame
from button import button
from background import background

class mainmenuscene:
    nextscene = settingsscene
    arguments = []

    def __init__(self, screen, settings):
        self.screen = screen

        self.running = True

        self.font = pygame.font.SysFont('Calibri', 30)

        self.screensize = settings.gamevalues["Resolution"]

        self.buttonlist = []

        self.background = background(self.screensize, (19, 19, 39, 255))

        self._createbuttons()
        self._startloop()
        return

    def _createbuttons(self):
        settingsbutton = button("Settings", self.font, [self.screensize[0]/2, self.screensize[1]/2], 300, 60, pygame.color.THECOLORS["red"], pygame.color.THECOLORS["orange"], pygame.color.THECOLORS["yellow"], self._switchtosettings)
        self.buttonlist.append(settingsbutton)

    def _drawbuttons(self):
        for i in self.buttonlist:
            i.update()
            i.draw(self.screen)

    def _startloop(self):
        t0 = 0.001 * pygame.time.get_ticks()
        maxdt = 0.5

        while self.running:
            t = 0.001 * pygame.time.get_ticks()
            dt = min(t - t0, maxdt)
            if dt > 0.:
                t0 = t

                # event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._exitpressed()
                    pass

                #draw
                self.background.draw(self.screen)
                self._drawbuttons()

                #display screen surface
                pygame.display.flip()

    def _switchtosettings(self):
        # todo: remove gamescene here
        self.nextscene = settingsscene
        self.running = False

    def _switchtoplayercreation(self):
        self.nextscene = playercreationscene
        self.running = False

    def _exitpressed(self):
        self.nextscene = None
        self.running = False