import pygame
from player import player
from background import background
from terrain import terrain
import random
from wind import windforce

class scorchedearth:
    _playercolors = [pygame.color.THECOLORS["red"], pygame.color.THECOLORS["yellow"], pygame.color.THECOLORS["cyan"], pygame.color.THECOLORS["pink"], pygame.color.THECOLORS["grey"], pygame.color.THECOLORS["orange"]]
    _groundcolors = [(193, 68, 14, 255), (35, 141, 35, 255), (143, 143, 143, 255)]

    gamestates = {"round": 0, "draw": 1, "win": 2}

    lengthofturn = 15.0    #length of turn per player
    shotlimit = 1  # max shots per round per player

    quitbutton = pygame.K_ESCAPE # quit button
    continuebutton = pygame.K_RETURN # continue button

    def __init__(self, screensize, playernames, fullscreen=False):
        #initialize pygame
        pygame.init()
        pygame.font.init()

        #screen
        self.screensize = screensize
        if fullscreen:
            self.screen = pygame.display.set_mode(self.screensize, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screensize)

        # background
        self.background = background(self.screensize, (19, 19, 39, 255))

        self.playernames = playernames
        #set name to Player x if empty
        for i in range(len(self.playernames)):
            if self.playernames[i] == "":
                self.playernames[i] = "Player " + str(i+1)

        # players, missiles, particles
        self.entities = [[], [], []]
        self.aliveplayers = []

        #wind
        self.maxwind = 4.0
        self.wind = windforce(self.maxwind)

        #initilize fonts
        self.font = pygame.font.SysFont('Arial', 20)
        self.winnersubfont = pygame.font.SysFont('Arial', 25)
        self.winnerfont = pygame.font.SysFont('Arial', 50)

        #create terrain object
        self.gameTerrain = terrain(self.screensize)

        #create player objects with random colors
        random.shuffle(scorchedearth._playercolors)
        for i in range(len(playernames)):
            player(playernames[i], self.gameTerrain, self.wind, self.entities, self.aliveplayers, scorchedearth._playercolors[i % len(self._playercolors)])

        #reset all variables
        self.restart()

        #start the gameloop
        self.startgameloop()
        return

    #sets or reset all parameters to the start of a new round
    def restart(self):

        #regenerate the terrain
        self.gameTerrain.groundcolor = random.choice(scorchedearth._groundcolors)[:-1]
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

        #timer for how long current turn is
        self.currentturnstart = 0.0

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
        pygame.quit()

    #event handling
    def _eventhandling(self, eventlist):
        for event in eventlist:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == self.quitbutton:
                return False
            elif event.type == pygame.KEYDOWN and event.key == self.continuebutton:
                if self.gamestate != self.gamestates["round"]:
                    self.restart()
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == self.currentplayer.key_fire: # start shot
                if self.currentplayer.shotcounter < self.shotlimit:
                    self.currentplayer.firekeyevent(event.type, self.elapsedtime)
            elif event.type == pygame.KEYDOWN and event.key == self.currentplayer.key_left:
                self.currentplayer.left = True
            elif event.type == pygame.KEYDOWN and event.key == self.currentplayer.key_right:
                self.currentplayer.right = True
            elif event.type == pygame.KEYUP and event.key == self.currentplayer.key_left:
                self.currentplayer.left = False
            elif event.type == pygame.KEYUP and event.key == self.currentplayer.key_right:
                self.currentplayer.right = False
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
            text = self.currentplayer.name + "  -  " + str(round(max(self.lengthofturn - (self.elapsedtime - self.currentturnstart), 0.0), 1))
            textsurface = self.font.render(text, False, self.currentplayer.color)
            screen.blit(textsurface, (50, 50))

            #draw wind text
            if self.maxwind == 0:
                text = str(round(0.0, 1))
            else:
                text = str(abs(round((self.wind.force.x/self.maxwind)*10, 1)))
            textsurface = self.font.render(text, False, self.currentplayer.color)
            screen.blit(textsurface, (self.screensize[0]-50-textsurface.get_rect().w, 50))

            if self.wind.force.x < 0:
                pygame.draw.polygon(screen, self.currentplayer.color, ((self.screensize[0]-50-textsurface.get_rect().w-10, 50+3), (self.screensize[0]-50-textsurface.get_rect().w-10, 50+17), (self.screensize[0]-50-textsurface.get_rect().w-25, 50+20/2)))
            elif self.wind.force.x > 0:
                pygame.draw.polygon(screen, self.currentplayer.color, ((self.screensize[0]-50-textsurface.get_rect().w-25, 50+3), (self.screensize[0]-50-textsurface.get_rect().w-25, 50+17), (self.screensize[0]-50-textsurface.get_rect().w-10, 50+20/2)))

            #draw shotcharging bar
            if self.currentplayer.shotcharging:
                time = self.elapsedtime - self.currentplayer.shootingstarttime
            else:
                time = 0.0

            pygame.draw.rect(screen, self.currentplayer.color, ((0, 0), (self.screensize[0] * min(max(time/self.currentplayer.fullpowershottime, self.currentplayer.minshotpower), 1.0), 5)))
            return
        else:
            if self.gamestate == self.gamestates["draw"]:
                text = "Draw"
                textsurface = self.winnerfont.render(text, False, pygame.color.THECOLORS["white"])
            else:
                textsurface = pygame.Surface(self.screensize)
                textsurface.set_colorkey((0, 0, 0))

                text = "Winner: " + self.aliveplayers[0].name
                textsurface2 = self.winnerfont.render(text, False, self.aliveplayers[0].color)
                textsurface.blit(textsurface2, (textsurface.get_rect().w / 2 - textsurface2.get_rect().w / 2, (textsurface.get_rect().h / 2)-90))

                #pygame.draw.rect(textsurface, self.aliveplayers[0].color, ((textsurface.get_rect().w / 2 - textsurface2.get_rect().w / 2 - 20, (textsurface.get_rect().h / 2)-110), (textsurface2.get_rect().w + 40, 162)), 3)

                text = "Wins: " + str(self.aliveplayers[0].wins)
                textsurface3 = self.winnersubfont.render(text, False, self.aliveplayers[0].color)
                textsurface.blit(textsurface3, (textsurface.get_rect().w / 2 - textsurface3.get_rect().w / 2, (textsurface.get_rect().h / 2)-28))

                text = "Kills: " + str(self.aliveplayers[0].kills)
                textsurface4 = self.winnersubfont.render(text, False, self.aliveplayers[0].color)
                textsurface.blit(textsurface4, (textsurface.get_rect().w / 2 - textsurface4.get_rect().w / 2, (textsurface.get_rect().h / 2)+7))

            screen.blit(textsurface, (self.screensize[0] / 2 - textsurface.get_rect().w / 2, self.screensize[1] / 2 - textsurface.get_rect().h / 2))
