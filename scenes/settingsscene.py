import pygame
from ui.button import button
from ui.settingsitems.settingstabs import settingstabs

class settingsscene:
    nextscene = None

    tabnames = ["Keys", "Player", "General", "Display"]
    #all settingsitems that are created, [dictindex, "text", "key", "type", specific]
    settingsitems = [[[0, "key", "Move left", "Left"], [0, "key", "Move right", "Right"], [0, "key", "Next item", "Next"], [0, "key", "Previous item", "Previous"], [0, "key", "Fire", "Fire"]],
                     [[1, "float", "Initial fuel in seconds", "Initial fuel", [0, 999]], [1, "float", "Maximum wind strength", "Wind strength", [0, 100]], [1, "float", "Maximum turret angle", "Max turret angle", [0, 180]], [1, "float", "Player speed", "Player speed", [0, 9999]], [1, "float", "Fullpower shot charging time", "Fullpower shot time", [0, 60]]],
                     [[1, "float", "Turn length", "Turn length", [3, 400]], [1, "int", "Turn shot limit", "Shot limit", [1, 999]], [1, "bool", "Enable fuel", "Enable fuel"], [1, "bool", "Reset fuel every round", "Reset fuel"]],
                     [[1, "dropdown", "Resolution (Restart)", "Resolution", [[1920, 1080], [1600, 900], [1280, 720], [960, 540]]], [1, "bool", "Fullscreen (Restart)", "Fullscreen"]]]

    def __init__(self, screen, background, settings):
        self.arguments = []
        self.screen = screen

        self.settings = settings

        self.running = True

        self.screensize = screen.get_size()

        self.font = pygame.font.SysFont(settings.design["Font type"], max(int(self.screensize[1]*0.042), 12))

        self.background = background

        # ui element height and width
        self.uiheight = self.screensize[1]*0.059
        self.uiwidth = self.screensize[0]*0.3
        self.backbuttonmargin = self.screensize[1]*0.05

        #buttons
        self.buttons = []

        self.settingspages = settingstabs([self.screensize[0]*0.15, self.screensize[1]*0.2], self.screensize[1]*0.059, self.screensize[0]*0.58, self.font, self.settingsitems, self.tabnames, self.settings)


        #button colors
        self.buttoncolor = settings.design["Button color"]
        self.hovercolor = settings.design["Button hover color"]
        self.pressedcolor = settings.design["Button pressed color"]
        self.inactivecolor = settings.design["Button inactive color"]
        self.bordercolor = settings.design["Textbox border color"]
        self.bordercolorhovering = self.hovercolor
        self.checkboxcolor = settings.design["Textbox active color"]

        #textboxcolors
        self.textboxactivecolor = settings.design["Textbox active color"]
        self.textboxinactivecolor = settings.design["Textbox inactive color"]
        self.textboxbordercolor = settings.design["Textbox border color"]

        self.textboxfont = pygame.font.SysFont(settings.design["Font type"], max(int(self.screensize[1]*0.033), 12))

        self.backkey = settings.playerkeys["Quit"]

        self._createbuttons()
        self._startloop()
        return

    def _createbuttons(self):
        backbutton = button("< Back", self.font, [self.backbuttonmargin+ self.uiwidth*0.3/2, self.backbuttonmargin+self.uiheight/2], self.uiwidth*0.3, self.uiheight,
                                self.buttoncolor, self.hovercolor,
                                self.pressedcolor, self.inactivecolor, self._goback)
        self.buttons.append(backbutton)

    def _intchanged(self, object):
        print(object.key, "        ", object.value)

    def _drawnoeventobjects(self):
        for i in self.settingspages.noeventobjects:
            i.update()
            i.draw(self.screen)

    def _drawbuttons(self):
        for i in self.buttons:
            i.update()
            i.draw(self.screen)

        for i in self.settingspages.buttons:
            i.update()
            i.draw(self.screen)

    def _draweventcaptureobjects(self):
        for i in self.settingspages.eventcaptureobjects:
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
                    else:
                        for i in self.settingspages.eventcaptureobjects:
                            i.eventhandler(event)
                    pass

                # draw
                self.background.draw(self.screen)
                self._drawbuttons()
                self._drawnoeventobjects()
                self._draweventcaptureobjects()

                # display screen surface
                pygame.display.flip()

    def _goback(self, object):
        self.nextscene = None
        self.running = False

    def _valuechanged(self, object):
        print(object.key, " value is now ", object.checked)

    def _keychanged(self, object):
        print(object.key, "changed key new key", object.keyvalue)

        object.keydict[object.key] = object.keyvalue
        self.settings.updatesettingsfile()

        print("updated settings for ", object.key)