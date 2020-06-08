from ui.keycapture import keycapture

class getkeyitem:
    #text
    #excludevalues
    #key
    #settingsclass
    def __init__(self, pos, w, h, text, font, excludevalues, key, settings):
        self.width = w
        self.height = h
        self.pos = pos
        self.settings = settings
        self.font = font

        self.textsurface
        self.keycapture = keycapture(True, self.settings.playerkeys["Left"], excludevalues, font, [w*0.8, 0], self.width*0.2,
                              self.height*0.8, self.textboxbordercolor, self.textboxactivecolor,
                              self.textboxinactivecolor, self._keychanged, None)
        return

    def eventpasser(self):

    def update

    def draw
