import pygame
from ui.button import button

class settingsscene:
    nextscene = None

    # TODO: implement this class, probably settings tabs

    def __init__(self, screen, background, settings):
        self.arguments = []
        self.screen = screen

        self.running = True

        self.font = pygame.font.SysFont(settings.design["Font type"], 30)

        self.screensize = settings.gamevalues["Resolution"]

        self.background = background

        self.buttonlist = []

        # ui element height and width
        self.uiheight = self.screensize[1]/18
        self.uiwidth = self.screensize[0]/4.3

        #button colors
        self.buttoncolor = settings.design["Button color"]
        self.hovercolor = settings.design["Button hover color"]
        self.pressedcolor = settings.design["Button pressed color"]
        self.inactivecolor = settings.design["Button inactive color"]

        self.backkey = settings.gamekeys["Quit"]

        self._createbuttons()
        self._startloop()
        return

    def _createbuttons(self):
        settingsbutton = button("Back", self.font, [self.screensize[0] / 2, self.screensize[1] / 2], self.uiwidth, self.uiheight,
                                self.buttoncolor, self.hovercolor,
                                self.pressedcolor, self.inactivecolor, self._goback)
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
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYUP and event.key == self.backkey:
                        self._goback(None)
                    pass

                # draw
                self.background.draw(self.screen)
                self._drawbuttons()

                # display screen surface
                pygame.display.flip()

    def _goback(self, object):
        self.nextscene = None
        self.running = False