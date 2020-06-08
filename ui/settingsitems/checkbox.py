import pygame

class checkbox:
    def __init__(self, keydict, key, pos, dimension, color, bordercolor, bordercolorhovering, checkmarkcolor, valuechangedfunction):



        self.keydict = keydict
        #key for dict values
        self.key = key
        # checked
        self.checked = self.keydict[self.key]

        #button box
        self.pos = pos
        self.rect = pygame.Rect((0, 0), (dimension, dimension))
        self.rect.center = self.pos

        self.borderrect = pygame.Rect(self.pos, (dimension, dimension))
        self.borderrect.center = self.rect.center

        #checkmark
        checkmarkmargin = dimension*0.2
        self.checkmarkrect = pygame.Rect((0, 0), (dimension-2*checkmarkmargin, dimension-2*checkmarkmargin))
        self.checkmarkrect.center = self.rect.center

        #colors
        self.bordercolor = bordercolor
        self.bordercolorhovering = bordercolorhovering
        self.checkmarkcolor = checkmarkcolor
        self.color = color

        #function that is called when button is pressed
        self.valuechangedfunction = valuechangedfunction

        self.hovering = False
        #if the mousebutton down is pressed, calls function if mousebutton one is released still on button
        self.clicked = False

    def update(self):
        mousepos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #calls function if mousebutton is released
        if self.rect.collidepoint(mousepos):
            if not self.clicked:
                self.hovering = True

                if click[0] == 1:
                    self.clicked = True
            else:
                if click[0] == 0:
                    self.checked = not self.checked
                    self.valuechangedfunction(self)
                    self.clicked = False
        else:
            self.hovering = False
            self.clicked = False

    def draw(self, screen):
        #switch color to current state color, clicked before hoveringx
        if self.hovering:
            bordercolor = self.bordercolorhovering
        else:
            bordercolor = self.bordercolor

        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, bordercolor, self.borderrect, 2)

        if self.checked:
            #draw the checkmark
            pygame.draw.rect(screen, self.checkmarkcolor, self.checkmarkrect)

    def valuefromfile(self):
        self.checked = self.keydict[self.key]
        return