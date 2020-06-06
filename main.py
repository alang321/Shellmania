import pygame
from settings import gamesettings
from scenes.mainmenuscene import mainmenuscene
from background import background

class main:
    #path for the settings
    settingspath = "./settings.txt"

    def __init__(self):
        self.settings = gamesettings(self.settingspath)

        # initialize pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screensize = self.settings.gamevalues["Resolution"]

        # screen
        if self.settings.gamevalues["Fullscreen"]:
            self.screen = pygame.display.set_mode(self.screensize, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screensize)

        self.background = background(self.screensize, (19, 19, 39, 255), True)

        self.defaultscene = mainmenuscene

        self.currentscene = self.defaultscene



        self.sceneswitcher()


    def sceneswitcher(self):
        running = True

        #extra arguments that can be passed
        args = []

        while running:
            scene = self.currentscene(self.screen, self.background, self.settings, *args)

            #switch to next scene or quit if there is no next scene
            if scene.nextscene is None:
                self.currentscene = self.defaultscene
                args = []
            else:
                self.currentscene = scene.nextscene
                args = scene.arguments
        pygame.quit()
