from scenes.settingsscene import settingsscene
from scenes.playercreationscene import playercreationscene
import pygame
from ui.button import button

class mainmenuscene:
    nextscene = settingsscene

    def __init__(self, screen, background, settings):
        self.arguments = []
        self.screen = screen

        self.running = True

        self.screensize = settings.gamevalues["Resolution"]

        self.buttonfont = pygame.font.SysFont(settings.design["Font type"], max(int(self.screensize[1]*0.042), 12))

        self.background = background

        self.buttonlist = []

        #button colors
        self.buttoncolor = settings.design["Button color"]
        self.hovercolor = settings.design["Button hover color"]
        self.pressedcolor = settings.design["Button pressed color"]
        self.inactivecolor = settings.design["Button inactive color"]

        #gamename
        self.titlefont = pygame.font.SysFont(settings.design["Font type title"], max(int(self.screensize[1]*0.2), 30))
        self.titletext = self.titlefont.render(settings.misc["Game title"], True, settings.design["Title color"])
        self.titlepos = [self.screensize[0]/2-self.titletext.get_rect().w/2, self.screensize[1]*0.285-self.titletext.get_rect().h/2]


        self._createbuttons()
        self._startloop()
        return

    def _createbuttons(self):
        offsetcenter = self.screensize[1]*0.07
        height = self.screensize[1]*0.059
        width = self.screensize[0]*0.3
        marginbetween = height * 0.2

        startbutton = button("Start", self.buttonfont, [self.screensize[0]/2, self.screensize[1]/2+offsetcenter], width, height,
                                self.buttoncolor, self.hovercolor,
                                self.pressedcolor, self.inactivecolor, self._switchtoplayercreation)
        self.buttonlist.append(startbutton)

        settingsbutton = button("Settings", self.buttonfont, [self.screensize[0] / 2, self.screensize[1] / 2+offsetcenter+height+marginbetween], width, height,
                                self.buttoncolor, self.hovercolor,
                                self.pressedcolor, self.inactivecolor, self._switchtosettings)
        self.buttonlist.append(settingsbutton)

        quitbutton = button("Quit", self.buttonfont, [self.screensize[0] / 2, self.screensize[1] / 2+offsetcenter+2 * height+ 2*marginbetween], width, height,
                                self.buttoncolor, self.hovercolor,
                                self.pressedcolor, self.inactivecolor, self._quit)
        self.buttonlist.append(quitbutton)

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
                        pygame.quit()
                        exit()
                    pass

                #draw
                self.background.draw(self.screen)
                self._drawbuttons()
                self.screen.blit(self.titletext, self.titlepos)

                #display screen surface
                pygame.display.flip()

    def _switchtosettings(self, object):
        self.nextscene = settingsscene
        self.running = False

    def _switchtoplayercreation(self, object):
        self.nextscene = playercreationscene
        self.running = False

    def _quit(self, object):
        pygame.quit()
        exit()