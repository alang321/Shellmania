from ui.button import button
from ui.settingsitems.checkbox import checkbox
from ui.settingsitems.keycapture import keycapture
from ui.settingsitems.numbox import numbox
from ui.settingsitems.label import label


#not very pretty code, but really wanted to get done at this point
#creates settings tabs that can be switche by buttons from array values, format can be seen in settingscene .py [dictindex, "text", "key", "type", extra]
class settingstabs:

    def __init__(self, pos, itemheight, itemwidth, font, itemarray, tabnames, settings):
        self.typerefs = {"key":self._appendkeycapture, "int":self._appendnumboxint, "float":self._appendnumboxfloat, "bool":self._appendcheckbox, "dropdown":self._appenddropdown}
        self.buttons = []
        self.tabbuttons = []

        self.uiheight = itemheight
        self.uiwidth = itemwidth
        self.uimarginbetween = 0.2 * self.uiheight

        self.font = font

        self.pos = pos

        self.settings = settings

        self.index = 0


        #button colors
        self.buttoncolor = settings.design["Button color"]
        self.hovercolor = settings.design["Button hover color"]
        self.pressedcolor = settings.design["Button pressed color"]
        self.inactivecolor = settings.design["Button inactive color"]
        self.bordercolor = settings.design["Textbox border color"]
        self.bordercolorhovering = self.hovercolor
        self.checkboxcolor = settings.design["Textbox active color"]

        self.buttonwidth = self.uiwidth * 0.18
        self.inputfieldwidth = self.uiwidth * 0.18

        #textboxcolors
        self.textboxactivecolor = settings.design["Textbox active color"]
        self.textboxinactivecolor = settings.design["Textbox inactive color"]
        self.textboxbordercolor = settings.design["Textbox border color"]

        #labeltext
        self.labelcolor = settings.design["Label color"]
        self.itemarray = itemarray

        #recreate settings items
        self._recreateseetingsitems()

        #create tab switching buttons
        self._createbuttons(tabnames)
        return

    def _recreateseetingsitems(self):
        self.noeventobjectslist = []
        self.eventcaptureobjectslist = []

        #create the list with setting items
        for index, itemlist in enumerate(self.itemarray):
            self.noeventobjectslist.append([])
            self.eventcaptureobjectslist.append([])
            for j, item in enumerate(itemlist):
                ypos = self.pos[1] + self.uiheight + self.uimarginbetween + (self.uiheight+self.uimarginbetween)*j
                self.noeventobjectslist[index].append(label(item[2], self.font, [self.pos[0], ypos], self.labelcolor))
                self.typerefs[item[1]](ypos, item, index)

        self.noeventobjects = self.noeventobjectslist[self.index]
        self.eventcaptureobjects = self.eventcaptureobjectslist[self.index]

    #create buttons for each tab
    def _createbuttons(self, tabnames):
        #create tabb buttons
        for index, item in enumerate(tabnames):
            xpos = (self.buttonwidth + 3) * index
            tabbutton = button(item, self.font, [self.pos[0]+self.buttonwidth/2+xpos, self.pos[1]], self.buttonwidth, self.uiheight,
                                    self.buttoncolor, self.hovercolor,
                                    self.pressedcolor, self.labelcolor, self._switchtab, index)
            self.buttons.append(tabbutton)
            self.tabbuttons.append(tabbutton)
        self.tabbuttons[0].active = False

        #create reset button
        self.buttons.append(button("Reset", self.font, [self.pos[0] + self.uiwidth, self.pos[1]], self.buttonwidth,
               self.uiheight,
               self.buttoncolor, self.hovercolor,
               self.pressedcolor, self.labelcolor, self._resetsettings))

    def _switchtab(self, object):
        for i in self.tabbuttons:
            i.active = True
        self.index = object.passingvalue
        object.active = False
        self.noeventobjects = self.noeventobjectslist[self.index]
        self.eventcaptureobjects = self.eventcaptureobjectslist[self.index]

    def _resetsettings(self, object):
        self.settings.reset()
        self._recreateseetingsitems()

    #append key capture object to index
    def _appendkeycapture(self, ypos, item, index):
        self.eventcaptureobjectslist[index].append(keycapture(self.settings.values[item[0]], item[3], False, self.font, [self.pos[0]+self.uiwidth, ypos], self.inputfieldwidth,
                                  self.uiheight, self.textboxbordercolor, self.hovercolor, self.textboxactivecolor,
                                  self.textboxinactivecolor, None, self._keychanged))
        return

    def _keychanged(self, object):
        object.keydict[object.key] = object.keyvalue
        self.settings.updatesettingsfile()

    #append numbox
    def _appendnumboxint(self, ypos, item, index):
        self.eventcaptureobjectslist[index].append(numbox(self.settings.values[item[0]], item[3], True, False, self.font, [self.pos[0]+self.uiwidth, ypos], self.inputfieldwidth,
                              self.uiheight, self.textboxbordercolor, self.hovercolor, self.textboxactivecolor,
                              self.textboxinactivecolor, item[4][0], item[4][1], self._numboxchanged))
        return

    def _appendnumboxfloat(self, ypos, item, index):
        self.eventcaptureobjectslist[index].append(numbox(self.settings.values[item[0]], item[3], False, False, self.font, [self.pos[0]+self.uiwidth, ypos], self.inputfieldwidth,
                              self.uiheight, self.textboxbordercolor, self.hovercolor, self.textboxactivecolor,
                              self.textboxinactivecolor, item[4][0], item[4][1], self._numboxchanged))

    def _numboxchanged(self, object):
        object.keydict[object.key] = object.value
        self.settings.updatesettingsfile()

    #append checkbox
    def _appendcheckbox(self, ypos, item, index):
        self.noeventobjectslist[index].append(checkbox(self.settings.values[item[0]], item[3], [self.pos[0]+self.uiwidth, ypos], self.uiheight*0.6,
                                self.checkboxcolor, self.bordercolor,
                                self.bordercolorhovering, self.bordercolor, self._boolchanged))
        return

    def _boolchanged(self, object):
        object.keydict[object.key] = object.checked
        self.settings.updatesettingsfile()

    def _appenddropdown(self, ypos, item, index):
        return
