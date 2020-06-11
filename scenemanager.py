import pygame
from settings import gamesettings
from scenes.mainmenuscene import mainmenuscene
from background import background

class scenemanager:
    #path for the settings
    def __init__(self, settingspath):
        self.settings = gamesettings(settingspath)

        # initialize pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        # screen
        if self.settings.gamevalues["Fullscreen"]:
            self.screen = pygame.display.set_mode(self.settings.gamevalues["Resolution"], pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.settings.gamevalues["Resolution"])

        self.background = background(self.settings.gamevalues["Resolution"], (19, 19, 39, 255))

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
