import pygame
import os.path

class gamesettings:
    _playerkeys = {'Left': pygame.K_a, 'Right': pygame.K_d, 'Next': pygame.K_e, 'Previous': pygame.K_q, 'Fire': pygame.K_SPACE}
    _gamekeys = {'Quit':pygame.K_ESCAPE, 'Newround':pygame.K_RETURN}
    _gamevalues = {'Resolution':[1280, 720], 'Fullscreen':False, 'Wind strength':3.0, 'Turret Angle Limit':90, 'Turn length':25.0,'Shot Limit':1}

    _sections = {'playerkeys': 0, 'gamekeys': 1, 'values': 2}

    _values = [_playerkeys,
               _gamekeys,
               _gamevalues]

    def __init__(self, path):
        self.path = path
        #if folder doesnt exist create
        # if path is empty regenerate

        #try to read path
        #if path dont work regenerate

        #key dictionary

        playerkeys = pygame.K_a, pygame.K_e, pygame.K_SPACE, pygame.K_q, pygame.K_e
        controlkeys = pygame.K_ESCAPE, pygame.K_RETURN
        #list with all other values, maybe a dictionary

        self.sections = []



    def reset(self):
        self.values = self._values.copy()
        self.generatesettingsfile(self.path)
        return

    #returns true if
    def getsettingsfromfile(self, path):
        return

    def generatesettingsfile(self, filepath):
        f = open(filepath, "w+")
        for sectionkey in gamesettings._sections:
            f.write("["+sectionkey+"]\n")
            values = self.values[gamesettings._sections[sectionkey]]
            for key in values:
                f.write(key+":"+str(values[key])+"\n")
        f.close()


#key player

#keys contiune

#resolution

#wind strength

#max turret angle

#length of turn

#shot limit

#battlefire
#company of iron
#spaceforce