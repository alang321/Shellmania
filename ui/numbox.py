import pygame

# todo : implement

class numbox:
    def __init__(self, isint, hasfocus, initialval, font, pos, w, h, bordercolor, backgroundcoloractive, backgroundcolorinactive, minvalue, maxvalue, lostfocusfunction, key="default", textcolor=pygame.color.THECOLORS["black"], maxtextlength=6):
        #Button text
        self.text = str(initialval)


        self.value = initialval

        self.font = font
        self.textcolor = textcolor

        self.maxtextlength = maxtextlength

        self.isint = isint
        if self.isint:
            self.convert = int
        else:
            self.convert = float

        self.minval = self.convert(minvalue)
        self.maxval = self.convert(maxvalue)

        self.rendertext(self.text)

        self.key = key

        #text box
        self.pos = pos
        self.textbox = pygame.Surface((w, h))
        self.rect = self.textbox.get_rect()
        self.rect.center = self.pos

        self.borderrect = pygame.Rect((0, 0), (w-1, h-1))

        #colors
        self.bordercolor = bordercolor
        self.inactivecolorbackground = backgroundcolorinactive
        self.activecolorbackground = backgroundcoloractive

        #function that is called when button is pressed
        self.lostfocusfunction = lostfocusfunction

        self.delete = False

        self.hasfocus = hasfocus

        self.hovering = False
        #if the mousebutton down is pressed, calls function if mousebutton one is released still on button
        self.clicked = False

    def rendertext(self, text):
        self.textsurface = self.font.render(text, True, self.textcolor)
        self.textsurfacerect = self.textsurface.get_rect()

    def _converttext(self, text):
        try:
            value = self.convert(text)

            if value <= self.maxval:
                self.value = value
                return True
            else:
                return False
        except:
            return False

    def _changefocus(self, value):
        if self.hasfocus != value:
            self.hasfocus = value

            if not self.hasfocus:
                if not self.minval <= self.value <= self.maxval:
                    self.value = self.minval
                    self.text = str(self.value)

                self.rendertext(self.text)
                if self.lostfocusfunction != None:
                    self.lostfocusfunction(self)

    #keydown event handler
    def eventhandler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._changefocus(self.rect.collidepoint(event.pos))
        # if text box has foxus and
        if event.type == pygame.KEYDOWN and self.hasfocus:
            if event.key == pygame.K_RETURN:
                self._changefocus(False)
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self._converttext(self.text)
            else:
                if len(self.text) < self.maxtextlength:
                    text = self.text
                    text += event.unicode
                    if self._converttext(text):
                        self.text += event.unicode
            self.rendertext(self.text)

    def update(self):
        #everything handled in eventhandler
        return

    def draw(self, screen):
        #switch color to current state color, clicked before hovering
        if self.hasfocus:
            color = self.activecolorbackground
        else:
            color = self.inactivecolorbackground

        #draw button rect
        self.textbox.fill(color)
        pygame.draw.rect(self.textbox, self.bordercolor, self.borderrect, 2)
        screen.blit(self.textbox, (self.pos[0]-self.rect.w/2, self.pos[1]-self.rect.h/2))

        #draw text
        screen.blit(self.textsurface, (self.pos[0]-self.textsurfacerect.w/2, self.pos[1]-self.textsurfacerect.h/2))
