class label:
    def __init__(self, text, font, pos, textcolor):
        #Button text
        self.pos = pos
        self.text = text
        self.textsurface = font.render(text, True, textcolor)
        self.textsurfacerect = self.textsurface.get_rect()

    def update(self):
        return

    def draw(self, screen):
        #draw text
        screen.blit(self.textsurface, (self.pos[0], self.pos[1]-self.textsurfacerect.h/2))

    def valuefromfile(self):
        return