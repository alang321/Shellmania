import pygame
from ui.button import button
from ui.textbox import textbox
from scenes.gamescene import gamescene

class playercreationscene:
    nextscene = gamescene

    def __init__(self, screen, background, settings):
        self.arguments = []
        self.screen = screen

        self.running = True
        self.screensize = settings.gamevalues["Resolution"]

        self.font = pygame.font.SysFont(settings.design["Font type"], max(int(self.screensize[1]/24), 12))
        self.textboxfont = pygame.font.SysFont(settings.design["Font type"], max(int(self.screensize[1]/30), 12))


        self.background = background

        self.buttonlist = []
        self.textboxlist = []

        #button colors
        self.buttoncolor = settings.design["Button color"]
        self.hovercolor = settings.design["Button hover color"]
        self.pressedcolor = settings.design["Button pressed color"]
        self.inactivecolor = settings.design["Button inactive color"]

        #textboxcolors
        self.textboxactivecolor = settings.design["Textbox active color"]
        self.textboxinactivecolor = settings.design["Textbox inactive color"]
        self.textboxbordercolor = settings.design["Textbox border color"]

        # ui element height and width
        self.uiheight = self.screensize[1]/18
        self.uiwidth = self.screensize[0]/4.3

        #textbox height
        self.textboxheight = self.screensize[1]/20
        self.textboxwidth = self.uiwidth
        self.textboxmargin = self.screensize[0]/30
        self.textboxxpos = self.screensize[0] * 0.8
        self.textboxypos = self.screensize[1] * 0.1

        self.backkey = settings.gamekeys["Quit"]

        #playerlimits
        self.maxplayers = 8
        self.minplayers = 2

        self._addtextbox(self.minplayers)
        self._createbuttons()
        self._startloop()
        return

    # creates buttons
    def _createbuttons(self):
        self.addplayerbutton = button("Add", self.font, [self.screensize[0] / 2, self.screensize[1] / 2], self.uiwidth, self.uiheight,
                                self.buttoncolor, self.hovercolor,
                                self.pressedcolor, self.inactivecolor, self._addplayer)
        self.buttonlist.append(self.addplayerbutton)

        self.removeplayerbutton = button("Remove", self.font, [self.screensize[0] / 2, self.screensize[1] / 2+70], self.uiwidth, self.uiheight,
                                self.buttoncolor, self.hovercolor,
                                self.pressedcolor, self.inactivecolor, self._removeplayer)
        self.buttonlist.append(self.removeplayerbutton)

        startbutton = button("Start", self.font, [self.screensize[0] / 2- 500, self.screensize[1] / 2+70], self.uiwidth, self.uiheight,
                                self.buttoncolor, self.hovercolor,
                                self.pressedcolor, self.inactivecolor, self._start)
        self.buttonlist.append(startbutton)

        self._activatedeactivatebuttons()

    #add a certain amount of text boxes
    def _addtextbox(self, amount):

        for i in range(amount):
            #take either the starting or the lowest ypos
            if len(self.textboxlist) == 0:
                ypos = self.textboxypos
            else:
                ypos = self.textboxlist[-1].pos[1]+self.textboxmargin+self.textboxheight
            nametextbox = textbox(True, "", self.textboxfont, [self.textboxxpos, ypos], self.textboxwidth, self.textboxheight, self.textboxbordercolor, self.textboxactivecolor, self.inactivecolor, None, None)
            self.textboxlist.append(nametextbox)


    #remove text boxes
    def _removetextbox(self):
        self.textboxlist.pop()
        return

    # updates and draw buttons
    def _drawbuttons(self):
        for i in self.buttonlist:
            i.update()
            i.draw(self.screen)

    #updates and draw text boxes
    def _drawtextboxes(self):
        for i in self.textboxlist:
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
                    elif event.type == pygame.KEYUP and event.key == self.backkey:
                        self._goback()
                    else:
                        for i in self.textboxlist:
                            i.eventhandler(event)
                    pass

                # draw
                self.background.draw(self.screen)
                self._drawbuttons()
                self._drawtextboxes()

                # display screen surface
                pygame.display.flip()

    def _goback(self):
        self.nextscene = None
        self.running = False

    def _addplayer(self, object):
        self._addtextbox(1)

        self._activatedeactivatebuttons()
        return

    def _removeplayer(self, object):
        self._removetextbox()

        self._activatedeactivatebuttons()
        return

    def _activatedeactivatebuttons(self):
        if self.maxplayers == len(self.textboxlist):
            self.addplayerbutton.active = False
        else:
            self.addplayerbutton.active = True

        if self.minplayers == len(self.textboxlist):
            self.removeplayerbutton.active = False
        else:
            self.removeplayerbutton.active = True

    def _start(self, object):
        playerlist = []
        for i in self.textboxlist:
            playerlist.append(i.text)
        self.arguments.append(playerlist)
        self.running = False