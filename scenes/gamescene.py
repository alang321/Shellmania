import pygame
from player import player
from background import background as generatebackground
from terrain import terrain
import random
from wind import windforce

class gamescene:
    _playercolors = [pygame.color.THECOLORS["red"], pygame.color.THECOLORS["yellow"], pygame.color.THECOLORS["cyan"], pygame.color.THECOLORS["pink"], pygame.color.THECOLORS["purple"], pygame.color.THECOLORS["green"]]
    _groundcolors = [(193, 68, 14, 255), (35, 141, 35, 255), (143, 143, 143, 255)]

    gamestates = {"round": 0, "draw": 1, "win": 2}

    nextscene = None

    def __init__(self, screen, background, settings, playernames):
        self.arguments = []
        #settingsfile
        self.settings = settings

        #screen
        self.screen = screen
        self.screensize = self.settings.gamevalues["Resolution"]

        # background
        self.background = generatebackground(self.screensize, (19, 19, 39, 255))

        self.playernames = playernames
        #set name to Player x if empty
        for i in range(len(self.playernames)):
            if self.playernames[i] == "":
                self.playernames[i] = "Player " + str(i+1)

        # players, missiles, particles
        self.entities = [[], [], []]
        self.aliveplayers = []

        #wind
        self.maxwind = 3.0
        self.wind = windforce(self.settings.gamevalues["Wind strength"])

        #turn length limits
        self.lengthofturn = self.settings.gamevalues["Turn length"]    #length of turn per player
        self.shotlimit = self.settings.gamevalues["Shot limit"]   # max shots per round per player

        #initilize fonts
        self.font = pygame.font.SysFont('Calibri', max(int(self.screensize[1]*0.028), 12))
        self.winnersubfont = pygame.font.SysFont('Arial', max(int(self.screensize[1]*0.05), 20))
        self.winnerfont = pygame.font.SysFont('Arial', max(int(self.screensize[1]*0.0695), 25))

        #sizes and margins
        self.margintop = self.screensize[1] * 0.0694
        self.marginside = self.screensize[1] * 0.055
        self.shotbarheight = self.screensize[1] * 0.00694
        self.arrowheight = self.screensize[1] * 0.02
        self.arrowwidth = self.screensize[1] * 0.02
        self.arrowmargin = 5
        self.offsetfromcenter = self.screensize[1]*0.2
        self.boxmargin =self.screensize[1]*0.05
        self.subtextmargin = 0.02 * self.screensize[1]

        #create terrain object
        self.gameTerrain = terrain(self.screensize)

        #create player objects with random colors
        random.shuffle(gamescene._playercolors)
        for i in range(len(playernames)):
            player(settings, playernames[i], self.gameTerrain, self.wind, self.entities, self.aliveplayers, gamescene._playercolors[i % len(self._playercolors)])

        #reset all variables
        self.restart()

        #start the gameloop
        self.startgameloop()
        return

    #sets or reset all parameters to the start of a new round
    def restart(self):

        #regenerate the terrain
        self.gameTerrain.groundcolor = random.choice(gamescene._groundcolors)[:-1]
        self.gameTerrain.generateTerrain()

        #random spawn order
        random.shuffle(self.entities[0])

        self.aliveplayers.clear()
        #respawn players
        for i in range(len(self.entities[0])):
            xpos = (self.gameTerrain.bounds[0] / len(self.entities[0])) * ((i+1)-0.5) + random.randint(int(-(self.gameTerrain.bounds[0] / len(self.entities[0])) * 0.05), int((self.gameTerrain.bounds[0] / len(self.entities[0]))*0.4))
            self.entities[0][i].respawn(xpos)
            self.aliveplayers.append(self.entities[0][i])

        #random control order
        random.shuffle(self.aliveplayers)

        #delete missiles and particles
        self.entities[1].clear()
        self.entities[2].clear()

        self.gamestate = self.gamestates["round"]

        #timer for when the current turn started
        self.currentturnstart = 0.001 * pygame.time.get_ticks()

        #random player starts
        self.currentindex = random.randint(0, len(self.playernames)-1)
        self.currentplayer = self.aliveplayers[self.currentindex]
        self.currentplayer.controlActive = True

        #wind
        self.wind.newWind()

    #game loop function
    def startgameloop(self):
        t0 = 0.001 * pygame.time.get_ticks()
        maxdt = 0.5

        running = True

        while running:
            self.elapsedtime = 0.001 * pygame.time.get_ticks()
            dt = min(self.elapsedtime - t0, maxdt)
            if dt > 0.:
                t0 = self.elapsedtime

                # event handling
                running = self._eventhandling(pygame.event.get())

                #update turn and win loose stuff
                self._turnlogic()

                #draw
                self.background.draw(self.screen)
                self.gameTerrain.draw(self.screen)
                self._drawEntities(self.screen, self.entities, dt)
                self._drawText(self.screen)

                #display screen surface
                pygame.display.flip()

    #event handling
    def _eventhandling(self, eventlist):
        for event in eventlist:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == self.settings.gamekeys["Quit"]:
                return False
            elif event.type == pygame.KEYDOWN and event.key == self.settings.gamekeys["Newround"]:
                if self.gamestate != self.gamestates["round"]:
                    self.restart()
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == self.settings.playerkeys["Fire"]: # start shot
                if self.currentplayer.shotcounter < self.shotlimit:
                    self.currentplayer.firekeyevent(event.type, self.elapsedtime)
            elif event.type == pygame.KEYDOWN and event.key == self.settings.playerkeys["Left"]:
                self.currentplayer.left = True
            elif event.type == pygame.KEYDOWN and event.key == self.settings.playerkeys["Right"]:
                self.currentplayer.right = True
            elif event.type == pygame.KEYUP and event.key == self.settings.playerkeys["Left"]:
                self.currentplayer.left = False
            elif event.type == pygame.KEYUP and event.key == self.settings.playerkeys["Right"]:
                self.currentplayer.right = False
            elif event.type == pygame.KEYUP and event.key == self.settings.playerkeys["Next"]:
                self.currentplayer.nextitem()
            elif event.type == pygame.KEYUP and event.key == self.settings.playerkeys["Previous"]:
                self.currentplayer.previousitem()
            pass
        return True

    def _turnlogic(self):
        if self.gamestate != self.gamestates["round"]: # if gamestate win or draw return
            return

        elif len(self.aliveplayers) <= 1: #switch gamestate and add win if playersalive is less or equal than 1
            if len(self.aliveplayers) == 1:
                self.gamestate = self.gamestates["win"]
                self.aliveplayers[0].controlActive = False
                self.aliveplayers[0].wins += 1
            if len(self.aliveplayers) == 0:
                self.gamestate = self.gamestates["draw"]

        elif self.currentplayer.destroyed: #switch to next alive player if current is destroyed
            newindex = (self.currentindex) % len(self.aliveplayers)
            if self._switchplayer(self.currentplayer, self.aliveplayers[newindex]):
                self.currentindex = newindex

        elif self.lengthofturn < (self.elapsedtime - self.currentturnstart) or self.currentplayer.shotcounter >= self.shotlimit: # if turnlength or shotlimit is exceeded switch player
            self.currentplayer.controlActive = False
            newindex = (self.currentindex + 1) % len(self.aliveplayers)
            if self._switchplayer(self.currentplayer, self.aliveplayers[newindex]):
                self.currentindex = newindex

    def _switchplayer(self, oldplayer, newplayer):
        #only switch if htere are no more missiles flying
        if len(self.entities[1]) == 0:
            if self.settings.gamevalues['Reset fuel']:
                oldplayer.fuel = oldplayer.initialfuel
            #wind
            self.wind.newWind()
            #oldplayer deativate control
            oldplayer.shotcharging = False
            oldplayer.controlActive = False
            oldplayer.shotcounter = 0
            self.currentplayer.left = False
            self.currentplayer.right = False
            #newplayer activate control
            self.currentplayer = newplayer
            newplayer.controlActive = True
            self.currentturnstart = self.elapsedtime
            return True
        else:
            return False

    def _drawEntities(self, screen, entities, dt):
        for entitylist in entities:
            delete = []
            for j in range(len(entitylist)):
                entitylist[j].update(dt)
                if entitylist[j].delete:
                    delete.append(j)

            for i in sorted(delete, reverse=True):
                del entitylist[i]

            for i in entitylist:
                i.draw(screen)

    def _drawText(self, screen):
        if self.gamestate == self.gamestates["round"]:
            #draw remaining time
            text = self.currentplayer.name + "  -  " + str(round(max(self.lengthofturn - (self.elapsedtime - self.currentturnstart), 0.0), 1)) + "  -  " + str(self.shotlimit - self.currentplayer.shotcounter)
            textsurface = self.font.render(text, False, self.currentplayer.color)
            screen.blit(textsurface, (self.marginside, self.margintop))

            #draw wind text
            if self.maxwind == 0:
                text = str(round(0.0, 1))
            else:
                text = str(abs(round((self.wind.force.x/self.maxwind)*10, 1)))
            textsurface = self.font.render(text, False, self.currentplayer.color)
            screen.blit(textsurface, (self.screensize[0]-self.marginside-textsurface.get_rect().w, self.margintop))

            #ddraw wind direction indicator
            if self.wind.force.x > 0:
                arrowpoint = (self.screensize[0]-self.marginside-textsurface.get_rect().w-self.arrowmargin ,self.margintop + self.arrowheight/2)
                arrowsidex = self.screensize[0]-self.marginside-textsurface.get_rect().w-self.arrowmargin- self.arrowwidth
                pygame.draw.polygon(screen, self.currentplayer.color, (arrowpoint, (arrowsidex, self.margintop+self.arrowheight), (arrowsidex, self.margintop)))
            elif self.wind.force.x < 0:
                arrowpoint = (self.screensize[0]-self.marginside-textsurface.get_rect().w-self.arrowmargin- self.arrowwidth ,self.margintop + self.arrowheight/2)
                arrowsidex = self.screensize[0] - self.marginside - textsurface.get_rect().w - self.arrowmargin
                pygame.draw.polygon(screen, self.currentplayer.color, (arrowpoint, (arrowsidex, self.margintop+self.arrowheight), (arrowsidex, self.margintop)))

            #draw shotcharging bar
            if self.currentplayer.shotcharging:
                time = self.elapsedtime - self.currentplayer.shootingstarttime
            else:
                time = 0.0
            pygame.draw.rect(screen, self.currentplayer.color, ((0, 0), (
            self.screensize[0] * min(max(time / self.currentplayer.fullpowershottime, self.currentplayer.minshotpower),
                                     1.0), self.shotbarheight)))

            #draw currently equipped weapon name
            amount = self.currentplayer.inventory.getcurrentamount()
            if amount < 0:
                text = self.currentplayer.inventory.getcurrentitem()._name + "  -  " + "∞"
            else:
                text = self.currentplayer.inventory.getcurrentitem()._name + "  -  " + str(amount)

            textsurface = self.font.render(text, False, self.currentplayer.color)
            screen.blit(textsurface, (self.screensize[0]/2-textsurface.get_rect().w/2, self.margintop))

            return
        else:
            if self.gamestate == self.gamestates["draw"]:
                text = "Draw"
                textsurface = self.winnerfont.render(text, False, pygame.color.THECOLORS["white"])
                y1 = self.screensize[1]/2-self.offsetfromcenter
                screen.blit(textsurface, (self.screensize[0]/2-textsurface.get_rect().w/2, y1))
                pygame.draw.rect(screen, pygame.color.THECOLORS["white"], (
                (self.screensize[0] / 2 - textsurface.get_rect().w / 2 - self.boxmargin, y1 - self.boxmargin),
                (textsurface.get_rect().w + self.boxmargin * 2,
                 textsurface.get_rect().h + self.boxmargin * 2)), 3)

            else:
                text = "Winner: " + self.aliveplayers[0].name
                textsurface = self.winnerfont.render(text, False, self.aliveplayers[0].color)
                y1 = self.screensize[1]/2-self.offsetfromcenter
                screen.blit(textsurface, (self.screensize[0]/2-textsurface.get_rect().w/2, y1))

                text = "Wins: " + str(self.aliveplayers[0].wins)
                textsurface2 = self.winnersubfont.render(text, False, self.aliveplayers[0].color)
                y2 = y1 + textsurface.get_rect().h+self.subtextmargin
                screen.blit(textsurface2, (self.screensize[0]/2-textsurface2.get_rect().w/2, y2))

                text = "Kills: " + str(self.aliveplayers[0].kills)
                textsurface3 = self.winnersubfont.render(text, False, self.aliveplayers[0].color)
                y3 = y2 + textsurface2.get_rect().h+self.subtextmargin
                screen.blit(textsurface3, (self.screensize[0]/2-textsurface3.get_rect().w/2, y3))

                pygame.draw.rect(screen, self.aliveplayers[0].color, ((self.screensize[0]/ 2 - textsurface.get_rect().w / 2 - self.boxmargin, y1 - self.boxmargin),
                (textsurface.get_rect().w + self.boxmargin * 2, y3 - y1 + textsurface3.get_rect().h + self.boxmargin*2)), 3)

