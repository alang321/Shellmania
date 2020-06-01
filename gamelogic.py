import pygame
from player import tank
from terrain import terrain
import random

class scorchedearth:
    _playercolors = [pygame.color.THECOLORS["red"], pygame.color.THECOLORS["yellow"], pygame.color.THECOLORS["cyan"],pygame.color.THECOLORS["pink"], pygame.color.THECOLORS["blue"], pygame.color.THECOLORS["grey"],pygame.color.THECOLORS["orange"]]

    #length of turn per player
    lengthofturn = 15.0
    # max shots per round per player
    shotlimit = 1
    # time to charge full power shot in seconds
    fullpowershottime = 1.5

    def __init__(self, screensize, playernames, fullscreen=False):
        #initialize pygame
        pygame.init()
        pygame.font.init()

        #passed parameters assignment
        self.screensize = screensize
        if fullscreen:
            self.screen = pygame.display.set_mode(self.screensize, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screensize)
        self.playernames = playernames
        #set name to Player x if empty
        for i in range(len(self.playernames)):
            if self.playernames[i] == "":
                self.playernames[i] = "Player " + str(i+1)

        # players, missiles, particles
        self.entities = [[], [], []]

        #create terrain object
        self.gameTerrain = terrain(self.screensize)
        #create player objects
        self._initPlayers(self.playernames)

        #reset all variables
        self.restart()

        #start the game
        self.start()
        return

    def restart(self):
        random.shuffle(scorchedearth._playercolors)

        #regenerate the terrain
        self.gameTerrain.generateTerrain()

        #respawn players
        random.shuffle(self.entities[0])
        for i in range(len(self.entities[0])):
            xpos = (self.gameTerrain.bounds[0] / len(self.entities[0])) * ((i+1)-0.5) + random.randint(int(-(self.gameTerrain.bounds[0] / len(self.entities[0])) * 0.1), int((self.gameTerrain.bounds[0] / len(self.entities[0]))*0.5))
            self.entities[0][i].respawn(xpos)

        #delete missiles and particles
        self.entities[1] = []
        self.entities[2] = []

        self.gameended = False

        #initilize fonts
        self.font = pygame.font.SysFont('Arial', 20)
        self.winnerfont = pygame.font.SysFont('Arial', 50)

        #variable to keep track of how many shots a player fired in the current turn
        self.shotcounter = 0
        #if shot is charing shootingtimer starts to see how long shot buttin is pressed
        self.shotcharging = False
        self.shootingtimer = 0.0

        #timer for how long current turn is
        self.currentturnlength = 0.0

        #random player starts
        self.currentplayer = random.randint(0, len(self.playernames)-1)
        self.entities[0][self.currentplayer].controlActive = True

    #add tank objects to player array
    def _initPlayers(self, playernames):
        for i in range(len(playernames)):
            #evenly distribute players over screen
            tank(playernames[i], self.gameTerrain, self.entities, scorchedearth._playercolors[i])

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

    def turnlogic(self):
        playersalive = len(self.entities[0])
        for i in self.entities[0]:
            if i.destroyed:
                playersalive -= 1

        if playersalive <= 1:
            self.gameended = True
            if playersalive == 1:
                while self.entities[0][self.currentplayer].destroyed:
                    if self.currentplayer >= len(self.entities[0]) - 1:
                        self.currentplayer = 0
                        continue
                    self.currentplayer += 1
                self.entities[0][self.currentplayer].wins += 1
                text = "Winner: " + self.entities[0][self.currentplayer].name
                textsurface = self.winnerfont.render(text, False, self.entities[0][self.currentplayer].color)
                self.screen.blit(textsurface, (self.screensize[0]/2 - textsurface.get_rect().w/2, self.screensize[1]/2 - textsurface.get_rect().h/2))
            else:
                text = "Draw"
                textsurface = self.winnerfont.render(text, False, pygame.color.THECOLORS["white"])
                self.screen.blit(textsurface, (self.screensize[0]/2 - textsurface.get_rect().w/2, self.screensize[1]/2 - textsurface.get_rect().h/2))
            return


        text = "Time left: " + str(round(abs(self.lengthofturn - self.currentturnlength), 1))
        textsurface = self.font.render(text, False, self.entities[0][self.currentplayer].color)
        self.screen.blit(textsurface, (50, 50))


        pygame.draw.rect(self.screen, self.entities[0][self.currentplayer].color, ((0, 0), (self.screensize[0] * min(max(self.shootingtimer/self.fullpowershottime, 0.1), 1.0), 5)))

        if self.shotcounter >= self.shotlimit:
            self.entities[0][self.currentplayer].controlActive = False
            self.currentturnlength = self.lengthofturn
            if len(self.entities[1]) > 0:
                return
            self.shotcounter = 0

        if self.currentturnlength > self.lengthofturn or self.entities[0][self.currentplayer].destroyed:
            self.shotcharging = False
            self.shootingtimer = 0.0
            self.entities[0][self.currentplayer].controlActive = False
            self.currentplayer += 1

            if self.currentplayer >= len(self.entities[0]):
                self.currentplayer = 0

            while self.entities[0][self.currentplayer].destroyed:
                if self.currentplayer >= len(self.entities[0])-1:
                    self.currentplayer = 0
                    continue
                self.currentplayer += 1

            self.entities[0][self.currentplayer].controlActive = True
            self.currentturnlength = 0.0
            self.shotcounter = 0

    def start(self):
        t0 = 0.001 * pygame.time.get_ticks()
        maxdt = 0.5

        running = True
        left = False
        right = False

        while running:
            t = 0.001 * pygame.time.get_ticks()
            dt = min(t - t0, maxdt)
            if dt > 0.:
                t0 = t
                # event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if self.gameended:
                            self.restart()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == self.entities[0][self.currentplayer].key_fire:
                        if self.shotcounter < self.shotlimit:
                            self.shotcharging = True
                    elif event.type == pygame.KEYUP and event.key == self.entities[0][self.currentplayer].key_fire:
                        if self.shotcharging:
                            self.shotcharging = False
                            if self.shotcounter < self.shotlimit:
                                self.shotcounter += 1
                                self.entities[0][self.currentplayer].fire(min(max(self.shootingtimer/self.fullpowershottime, 0.1), 1.0))
                                self.shootingtimer = 0.0
                    elif event.type == pygame.KEYDOWN and event.key == self.entities[0][self.currentplayer].key_left:
                        left = True
                    elif event.type == pygame.KEYDOWN and event.key == self.entities[0][self.currentplayer].key_right:
                        right = True
                    elif event.type == pygame.KEYUP and event.key == self.entities[0][self.currentplayer].key_left:
                        left = False
                    elif event.type == pygame.KEYUP and event.key == self.entities[0][self.currentplayer].key_right:
                        right = False
                    pass

                if self.shotcharging:
                    self.shootingtimer += dt

                if left:
                    self.entities[0][self.currentplayer].move(-1.0, dt)
                elif right:
                    self.entities[0][self.currentplayer].move(1.0, dt)

                self.gameTerrain.draw(self.screen)

                self.currentturnlength += dt
                self.turnlogic()

                self._drawEntities(self.screen, self.entities, dt)
                pygame.display.flip()
        pygame.quit()


