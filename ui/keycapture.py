import pygame

#gets a keyinput if it has focus, doesnt set it just gets it
class keycapture:
    def __init__(self, hasfocus, keydict, key, font, pos, w, h, bordercolor, bordercolorhover, backgroundcoloractive, backgroundcolorinactive, keychangedfunction, lostfocusfunction, textcolor=pygame.color.THECOLORS["black"]):
        self.font = font
        self.textcolor = textcolor
        self.maxtextlength = 1

        self.keydict = keydict

        #key for dict values
        self.key = key
        #int value of the current key
        self.keyvalue = self.keydict[self.key]

        self.text = ""
        self.settext()

        #text box
        self.pos = pos
        self.textbox = pygame.Surface((w, h))
        self.rect = self.textbox.get_rect()
        self.rect.center = self.pos

        self.borderrect = pygame.Rect((0, 0), (w-1, h-1))

        #colors
        self.bordercolor = bordercolor
        self.bordercolordefualt = bordercolor
        self.bordercolorhover = bordercolorhover
        self.inactivecolorbackground = backgroundcolorinactive
        self.activecolorbackground = backgroundcoloractive

        #function that is called when button is pressed
        self.keychangedfunction = keychangedfunction
        self.lostfocusfunction = lostfocusfunction

        self.delete = False

        #whether the last input was wrong, as in exluded or self
        self.lastinputerror = False

        self.hasfocus = hasfocus

        self.hovering = False
        #if the mousebutton down is pressed, calls function if mousebutton one is released still on button
        self.clicked = False

    def settext(self):
        if self.keyvalue != None:
            self.text = pygame.key.name(self.keyvalue)
        else:
            self.text = ""

        self.rendertext(self.text)

    def rendertext(self, text):
        self.textsurface = self.font.render(text, True, self.textcolor)
        self.textsurfacerect = self.textsurface.get_rect()

    def _changefocus(self, value):
        if self.hasfocus != value:
            self.hasfocus = value

            if not self.hasfocus:
                if self.lostfocusfunction != None:
                    self.lostfocusfunction(self)

    #keydown event handler
    def eventhandler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._changefocus(self.rect.collidepoint(event.pos))
            return True
        # if text box has foxus and
        if event.type == pygame.KEYDOWN and self.hasfocus:
            if event.key == pygame.K_RETURN:
                self._changefocus(False)
            elif not event.key in self.keydict.values() and event.key != self.keyvalue:
                self.keyvalue = event.key
                self.settext()
                if self.keychangedfunction != None:
                    self.keychangedfunction(self)
                self.lastinputerror = False
            else:
                self.lastinputerror = True
            self.rendertext(self.text)

    def update(self):
        mousepos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mousepos):
            self.bordercolor = self.bordercolorhover
        else:
            self.bordercolor = self.bordercolordefualt
        return

    def draw(self, screen):

        if self.lastinputerror and self.hasfocus:
            bordercolor = pygame.color.THECOLORS["red"]
        else:
            self.lastinputerror = False
            bordercolor = self.bordercolor

        if self.hasfocus:
            color = self.activecolorbackground
        else:
            color = self.inactivecolorbackground

        #draw button rect
        self.textbox.fill(color)
        pygame.draw.rect(self.textbox, bordercolor, self.borderrect, 2)
        screen.blit(self.textbox, (self.pos[0]-self.rect.w/2, self.pos[1]-self.rect.h/2))

        #draw text
        screen.blit(self.textsurface, (self.pos[0]-self.textsurfacerect.w/2, self.pos[1]-self.textsurfacerect.h/2))
