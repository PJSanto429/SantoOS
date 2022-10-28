#from modal import *
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
        loadingTitle = 'loading...',
        loadedTitle = 'done!',
        backgroundColor = VERYDARKGREY,
        loadedColor = GREEN,
        textColor = BLACK,
        textFont = defaultLoaderFont,
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
        self.title = ''
        self.loadingTitle = loadingTitle
        self.loadedTitle = loadedTitle
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
        self.active = False
        self.finished = False
        self.dist = (self.width - self.offset) / self.time
        self.activationTime = 0
        self.doneloadingFunctDone = False
        
    def activate(self):
        self.setTime = 0
        self.doneloadingFunctDone = self.finished = False
        self.activationTime = round(pg.time.get_ticks()/1000)
        self.active = True
    
    def deactivate(self):
        self.active = False
        self.activationTime = round(pg.time.get_ticks()/1000)
        self.setTime = 0
        
    def doneLoadingFunct(self):
        print('done loading')
    
    def loadingDone(self):
        if not self.doneloadingFunctDone:
            self.doneloadingFunctDone = True
            self.doneLoadingFunct()

    def update(self, screen):
        if self.active:
            self.title = self.loadingTitle if not self.finished else self.loadedTitle
            if self.setTime < self.time:
                self.setTime = (pg.time.get_ticks() / 1000) - self.activationTime
                try:
                    self.loadedImage = pg.Surface([(self.setTime * self.dist), self.height - self.offset])
                except:
                    pass
                self.loadedRect = self.loadedImage.get_rect(topleft = (self.x + (self.offset / 2), self.y + self.offset / 2))
            else:
                self.finished = True
                self.loadingDone()
            self.loadedImage.fill(self.loadedColor)
            self.textImage = self.textFont.render(self.title, True, self.textColor)
            self.textRect = self.textImage.get_rect(bottom = self.rect.top - 5, centerx = self.rect.centerx)
            screen.blit(self.image, self.rect)
            screen.blit(self.loadedImage, self.loadedRect)
            screen.blit(self.textImage, self.textRect)
        else:
            try:
                self.loadedImage = pg.Surface([(self.setTime * self.dist), self.height - self.offset])
            except:
                pass
            self.loadedRect = self.loadedImage.get_rect(topleft = (self.x + (self.offset / 2), self.y + self.offset / 2))