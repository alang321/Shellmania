import pygame

class button:
    def __init__(self, text, font, pos, w, h, color, hoveringcolor, clickedcolor, inactivecolor, function, active=True, textcolor=pygame.color.THECOLORS["white"]):
        #Button text
        self.text = text
        self.textsurface = font.render(text, False, textcolor)
        self.textsurfacerect = self.textsurface.get_rect()

        #if button is active
        self.active = active

        #button box
        self.pos = pos
        self.buttonbox = pygame.Surface((w, h))
        self.rect = self.buttonbox.get_rect()
        self.rect.center = self.pos

        #colors
        self.hoveringcolor = hoveringcolor
        self.clickedcolor = clickedcolor
        self.inactivecolor = inactivecolor
        self.color = color

        #function that is called when button is pressed
        self.function = function


        self.hovering = False
        #if the mousebutton down is pressed, calls function if mousebutton one is released still on button
        self.clicked = False

    def update(self):
        mousepos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #calls function if mousebutton is released
        if self.rect.collidepoint(mousepos) and self.active:
            if not self.clicked:
                self.hovering = True

                if click[0] == 1:
                    self.clicked = True
            else:
                if click[0] == 0:
                    self.function(self)
                    self.clicked = False
        else:
            self.hovering = False
            self.clicked = False

    def draw(self, screen):
        #switch color to current state color, clicked before hovering
        if not self.active:
            color = self.inactivecolor
        elif self.clicked:
            color = self.clickedcolor
        elif self.hovering:
            color = self.hoveringcolor
        else:
            color = self.color

        #draw button rect
        self.buttonbox.fill(color)
        screen.blit(self.buttonbox, (self.pos[0]-self.rect.w/2, self.pos[1]-self.rect.h/2))

        #draw text
        screen.blit(self.textsurface, (self.pos[0]-self.textsurfacerect.w/2, self.pos[1]-self.textsurfacerect.h/2))
