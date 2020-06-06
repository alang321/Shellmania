import pygame
from settings import gamesettings
from scenes.mainmenuscene import mainmenuscene

class main:
    #path for the settings
    settingspath = "./settings.txt"

    def __init__(self):
        self.settings = gamesettings(self.settingspath)

        # initialize pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        # screen
        if self.settings.gamevalues["Fullscreen"]:
            self.screen = pygame.display.set_mode(self.settings.gamevalues["Resolution"], pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.settings.gamevalues["Resolution"])

        self.currentscene = mainmenuscene

        self.sceneswitcher()


    def sceneswitcher(self):
        running = True

        #extra arguments that can be passed
        args = ()

        while running:
            scene = self.currentscene(self.screen, self.settings, *args)

            #switch to next scene or quit if there is no next scene
            if scene.nextscene is None:
                running = False
            else:
                self.currentscene = scene.nextscene
                args = scene.arguments
        pygame.quit()
