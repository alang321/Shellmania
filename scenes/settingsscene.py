import pygame
from ui.button import button
from ui.checkbox import checkbox

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
        self.uiheight = self.screensize[1]*0.059
        self.uiwidth = self.screensize[0]*0.3

        #button colors
        self.buttoncolor = settings.design["Button color"]
        self.hovercolor = settings.design["Button hover color"]
        self.pressedcolor = settings.design["Button pressed color"]
        self.inactivecolor = settings.design["Button inactive color"]
        self.bordercolor = settings.design["Textbox border color"]
        self.bordercolorhovering = self.hovercolor
        self.checkboxcolor = settings.design["Textbox active color"]

        self.backkey = settings.gamekeys["Quit"]

        self._createbuttons()
        self._startloop()
        return

    def _createbuttons(self):
        backbutton = button("Back", self.font, [self.screensize[0] / 2, self.screensize[1] / 2], self.uiwidth, self.uiheight,
                                self.buttoncolor, self.hovercolor,
                                self.pressedcolor, self.inactivecolor, self._goback)
        self.buttonlist.append(backbutton)

        checkbox1 = checkbox(False, self.font, [self.screensize[0] / 2, self.screensize[1] / 2+80], self.uiheight*0.8,
                                self.checkboxcolor, self.bordercolor,
                                self.bordercolorhovering, self.bordercolor, self._valuechanged)
        self.buttonlist.append(checkbox1)

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

    def _valuechanged(self, object):
        print(object.key, " value is now ", object.checked)