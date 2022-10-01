#from modal import *
from modal import Modal
from variables import * 

class Loading():
    instances = []
    def __init__(
        self,
        x,
        y,
        width,
        height,
        time = 10,
        title = 'title',
        textColor = BLACK,
        textFont = defaultClockFont,
        backgroundColor = DARKGREY,
        loadedColor = GREEN,
        parentApp = 'none',
        parent = False
    ):
        self.__class__.instances.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.time = time
        self.setTime = 0
        self.title = title
        self.textColor = textColor
        self.textFont = textFont
        self.backgroundColor = backgroundColor
        self.loadedColor = loadedColor
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.image.fill(self.backgroundColor)
        self.offset = 20
        self.loadedImage = pg.Surface([0, height - self.offset])
        self.loadedRect = self.loadedImage.get_rect(topleft = (self.x + (self.offset / 2), self.y + self.offset / 2))
        self.loadedImage.fill(self.loadedColor)
        self.parentApp = parentApp
        self.parent = parent
        self.active = self.finished = False
        self.dist = (self.width - self.offset) / self.time
        
    def activate(self):
        self.setTime = 0
        self.finished = False
        self.activationTime = round(pg.time.get_ticks()/1000)
        self.active = True

    def update(self, screen):
        if self.active:
            if self.setTime < self.time:
                self.setTime = round(pg.time.get_ticks()/1000) - self.activationTime
                self.loadedImage = pg.Surface([self.setTime * self.dist, self.height - self.offset])
                self.loadedRect = self.loadedImage.get_rect(topleft = (self.x + (self.offset / 2), self.y + self.offset / 2))
            else:
                self.finished = True
            self.loadedImage.fill(self.loadedColor)
            screen.blit(self.image, self.rect)
            screen.blit(self.loadedImage, self.loadedRect)
        else:
            self.setTime = 0
        #! text stuff - not used yet
        #self.textImage = self.textFont.render(self.title, True, self.textColor)
        #self.textRect = self.textImage.get_rect(top = self.rect.top + 15, left = self.rect.left + 15)
        #screen.blit(self.textImage, self.textRect)