import pygame

class textbox:
    def __init__(self, hasfocus, text, font, pos, w, h, bordercolor, backgroundcoloractive, backgroundcolorinactive, textchangedfunction, lostfocusfunction, maxtextlength=11, key="default", textcolor=pygame.color.THECOLORS["black"]):
        #Button text
        self.text = text
        self.font = font
        self.textcolor = textcolor
        self.maxtextlength = maxtextlength

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
        self.textchangedfunction = textchangedfunction
        self.lostfocusfunction = lostfocusfunction

        self.delete = False

        self.hasfocus = hasfocus

        self.hovering = False
        #if the mousebutton down is pressed, calls function if mousebutton one is released still on button
        self.clicked = False

    def rendertext(self, text):
        self.textsurface = self.font.render(text, True, self.textcolor)
        self.textsurfacerect = self.textsurface.get_rect()

    #keydown event handler
    def eventhandler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.hasfocus = True
            else:
                self.hasfocus = False
                if self.lostfocusfunction != None:
                    self.lostfocusfunction(self)
            return True
        # if text box has foxus and
        if event.type == pygame.KEYDOWN and self.hasfocus:
            if event.key == pygame.K_RETURN:
                self.hasfocus = False
                if self.lostfocusfunction != None:
                    self.lostfocusfunction(self)
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                if self.textchangedfunction != None:
                    self.textchangedfunction(self)
            else:
                if len(self.text) < self.maxtextlength:
                    self.text += event.unicode
                    if self.textchangedfunction != None:
                        self.textchangedfunction(self)
            self.rendertext(self.text)
            return True
        return False

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
