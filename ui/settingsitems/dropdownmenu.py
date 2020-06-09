import pygame
from ui.button import button

class dropdownmenu:
    def __init__(self, keydict, key, items, font, pos, w, h, color, hoveringcolor, clickedcolor, inactivecolor, newvaluefunction, textcolor=pygame.color.THECOLORS["black"]):
        self.keydict = keydict
        self.key = key
        self.items = items

        self.item = self.keydict[self.key]

        self.font = font

        self.w = w
        self.h = h

        try:
            self.index = self.items.index(self.item)
        except:
            self.index = -1

        #Button text
        self.textcolor = textcolor
        self.text = self._itemtotext(self.item)
        self.textsurface = font.render(self.text, True, self.textcolor)
        self.textsurfacerect = self.textsurface.get_rect()

        #button box
        self.pos = pos
        self.buttonbox = pygame.Surface((w, h))
        self.rect = self.buttonbox.get_rect()
        self.rect.center = self.pos

        #the rect of the current object,  if extended it gets bigger
        self.activerect = self.rect

        #colors
        self.hovercolor = hoveringcolor
        self.clickedcolor = clickedcolor
        self.inactivecolor = inactivecolor
        self.color = color

        #function that is called when button is pressed
        self.newvaluefunction = newvaluefunction

        #whether the dropdown menu is extended
        self.extended = False
        self.buttons = []

        self.hovering = False
        #if the mousebutton down is pressed, calls function if mousebutton one is released still on button
        self.clicked = False

    def _createbuttons(self):
        # key as passing value
        for j, item in enumerate(self.items):
            dropdownitem = button(self._itemtotext(item), self.font, [self.pos[0], self.pos[1]+(self.h-1)*(j+1)], self.w, self.h,
                                    self.color, self.hovercolor,
                                    self.clickedcolor, self.hovercolor, self._dropbuttonspressed, j)
            self.buttons.append(dropdownitem)

            self.activerect = self.activerect.union(dropdownitem.rect)

        self._changeactive()

    def _dropbuttonspressed(self, object):
        self._switchitem(object.passingvalue)

    def _switchitem(self, index):
        self.index = index
        self.item = self.items[self.index]

        self.text = self._itemtotext(self.items[index])

        self._changeactive()
        self._rendertext()

        if self.newvaluefunction != None:
            self.newvaluefunction(self)

    #make an item to text
    def _itemtotext(self, item):
        return str(item[0]) + "x" + str(item[1])

    #render the current text
    def _rendertext(self):
        self.textsurface = self.font.render(self.text, True, self.textcolor)
        self.textsurfacerect = self.textsurface.get_rect()

    #change the active
    def _changeactive(self):
        for i in self.buttons:
            i.active = True

        # if minus 1 no buttons is set to active
        if self.index >= 0:
            self.buttons[self.index].active = False


    def update(self):
        for i in self.buttons:
            i.update()

        mousepos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #calls function if mousebutton is released
        if self.activerect.collidepoint(mousepos):
            if self.rect.collidepoint(mousepos):
                if not self.clicked:
                    self.hovering = True

                    if click[0] == 1:
                        self.clicked = True
                else:
                    if click[0] == 0:
                        self.clicked = False
                        self._changeextended(not self.extended)
            else:
                self.hovering = False
                self.clicked = False
        else:
            self.hovering = False
            self.clicked = False
            self._changeextended(False)

    def _changeextended(self, extended):
        if self.extended != extended:
            self.extended = extended

            if self.extended:
                self._createbuttons()
            else:
                self.buttons = []
                self.activerect = self.rect


    def draw(self, screen):
        #switch color to current state color, clicked before hovering
        if self.clicked:
            color = self.clickedcolor
        elif self.hovering:
            color = self.hovercolor
        else:
            color = self.color


        #draw button rect
        self.buttonbox.fill(color)
        screen.blit(self.buttonbox, (self.pos[0]-self.rect.w/2, self.pos[1]-self.rect.h/2))

        #draw text
        screen.blit(self.textsurface, (self.pos[0]-self.textsurfacerect.w/2, self.pos[1]-self.textsurfacerect.h/2))

        for i in self.buttons:
            i.draw(screen)
