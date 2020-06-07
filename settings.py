import pygame

class gamesettings:
    #default values
    _playerkeys = {'Left': pygame.K_a, 'Right': pygame.K_d, 'Next': pygame.K_e, 'Previous': pygame.K_q, 'Fire': pygame.K_SPACE}
    _gamekeys = {'Quit':pygame.K_ESCAPE, 'Newround':pygame.K_RETURN}
    _gamevalues = {'Resolution':[1280, 720], 'Fullscreen':False, 'Wind strength':3.0, 'Turn length':25.0,'Shot limit':1, 'Enable fuel': False, 'Reset fuel':True, 'Initial fuel':10.0, 'Max turret angle':85.0, 'Player speed':45.0}
    _design = {'Button color':[210,206,194,255], 'Button hover color':[242,190,28,255], 'Button pressed color':list(pygame.color.THECOLORS["orange"]), 'Button inactive color':list(pygame.color.THECOLORS["red"]), 'Textbox active color':list(pygame.color.THECOLORS["white"]), 'Textbox inactive color':[130,130,130], 'Textbox border color':list(pygame.color.THECOLORS["black"]), 'Title color':[242,190,28,255], 'Font type':'Calibri'}
    _misc = {'Game title': "Tiny Tank"}


    _sections = {'playerkeys': 0, 'gamekeys': 1, 'values': 2, 'design':3, 'misc':4}

    _values = [_playerkeys,
               _gamekeys,
               _gamevalues,
               _design,
               _misc]

    #seperator for save lines
    _seperator = ':'

    #parse function dictionary, kind fo ugly but works
    _parsefunctions = {'int': "_parseint", 'float': "_parsefloat", 'bool': "_parsebool", 'list': "_parselist", 'str':"_parsestring"}

    def __init__(self, path):
        self.path = path
        self.reset()
        self.values = self.readsettingsfromfile()

        #for easier access
        self.playerkeys = self.values[0]
        self.gamekeys = self.values[1]
        self.gamevalues = self.values[2]
        self.design = self.values[3]
        self.misc = self.values[4]

    #resets the savefile with default values
    def reset(self):
        self._writesettingsfile(self._values)
        return

    #updates the settings file to include current values
    def updatesettingsfile(self):
        self._writesettingsfile(self.values)

    def _writesettingsfile(self, valuelist):
        textfile = open(self.path, "w+")
        for sectionkey in gamesettings._sections:
            textfile.write("["+sectionkey+"]\n")
            values = valuelist[gamesettings._sections[sectionkey]]
            for key in values:
                textfile.write(key+gamesettings._seperator+str(type(values[key]))+str(values[key])+"\n")
        textfile.close()

    #creates setting file if settings file doesnt exist or error while reading
    def readsettingsfromfile(self):
        values = []

        #try to open the file
        try:
            textfile = open(self.path)
        except:
            self.reset()
            textfile = open(self.path)

        #split the lines without newline symbols
        lines = textfile.read().splitlines()

        #try reading the file, if exception occurs file is reset and reading is attempted again
        try:
            counter = 0
            for sectionkey in gamesettings._sections:
                dictionary = {}
                values.append(dictionary)

                if gamesettings._textbetweensymbols(lines[counter].strip(), '[', ']') != sectionkey:
                    raise Exception("sectionkey doesnt equal file sectionkey  ", sectionkey, " != ", lines[counter])

                for refkey in gamesettings._values[gamesettings._sections[sectionkey]]:
                    counter += 1
                    #line to be analysed
                    line = lines[counter]

                    key = self._readkey(line)
                    if key == refkey:
                        dictionary[key] = gamesettings._parsevalue(line)
                    else:
                        raise Exception("refkey doesnt equal file key")
                counter += 1
        except Exception as ex:
            print(ex)
            self.reset()
            values = self.readsettingsfromfile()

        #close file
        textfile.close()

        return values

    @staticmethod
    def _parsevalue(line):
        #split at double dot
        line = line.split(gamesettings._seperator)[1]

        # split at >
        line = line.split('>')
        key = gamesettings._textbetweensymbols(line[0], '\'', '\'')
        value = line[1]

        return getattr(gamesettings, gamesettings._parsefunctions[key])(value)

    @staticmethod
    def _readkey(line):
        return line.split(gamesettings._seperator)[0]

    @staticmethod
    def _parseint(value):
        return int(value)

    @staticmethod
    def _parsefloat(value):
        return float(value)

    @staticmethod
    def _parsebool(value):
        if value == "True":
            return True
        else:
            return False

    @staticmethod
    def _parselist(value):
        values = gamesettings._textbetweensymbols(value, '[', ']')

        list = [int(i) for i in values.split(", ")]
        return list

    @staticmethod
    def _parsestring(value):
        return value

    @staticmethod
    #read text between to symbols
    def _textbetweensymbols(line, sy1, sy2):
        return line.split(sy1)[1].split(sy2)[0]