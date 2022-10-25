import pygame as pg
from math import floor

from variables import *

class Slider:
    instances = []
    def __init__(
        self,
        x,
        y,
        width,
        height,
        maxVal = 100,
        title = False, #['slider', 'top']
        showValue = False, #[True, 'right']
        backgroundColor = VERYDARKGREY,
        activeColor = BLUE,
        handleColor = GREEN,
        textColor = BLACK,
        textFont = defaultSliderFont,
        parentApp = 'none',
        parent = False,
    ):
        self.__class__.instances.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.maxVal = maxVal
        self.offset = 20
        self.value = 0
        
        self.backgroundColor = backgroundColor
        self.activeColor = activeColor
        self.handleColor = handleColor
        self.textColor = textColor
        self.textFont = textFont
        
        #main body stuff
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect(topleft = (x, y))
        self.image.fill(self.backgroundColor)
        
        #active body stuff
        self.activeImage = pg.Surface([0, height - self.offset])
        self.activeRect = self.image.get_rect(topleft = (x + (self.offset / 2), y + self.offset / 2))
        self.activeImage.fill(self.activeColor)
        
        #handle stuff
        self.handleImage = pg.Surface([20, height - (self.offset / 2)])
        self.handleRect = self.handleImage.get_rect(topleft = (x + (self.offset / 2), y + self.offset / 4))
        self.handleImage.fill(self.handleColor)
        
        self.parent = parent
        self.parentApp = parentApp
        
        self.title = title
        if self.title:
            self.title, self.titleLocation = self.title
            self.titleImage = self.textFont.render(self.title, True, self.textColor)
            self.getTitleLocation()
            
        self.showValue = showValue
        if self.showValue:
            self.showValue, self.valueLocation = self.showValue
            self.valueImage = self.textFont.render('0', True, self.textColor)
            self.getValueLocation()
            
    def getTitleLocation(self):
        if self.titleLocation == 'top':
            self.titleRect = self.titleImage.get_rect(centerx = self.rect.centerx, bottom = self.rect.top)
        elif self.titleLocation == 'bottom':
            self.titleRect = self.titleImage.get_rect(centerx = self.rect.centerx, top = self.rect.bottom + 10)
        elif self.titleLocation == 'left':
            self.titleRect = self.titleImage.get_rect(centery = self.rect.centery, right = self.rect.left - 10)
        elif self.titleLocation == 'right':
            self.titleRect = self.titleImage.get_rect(centery = self.rect.centery, left = self.rect.right + 10)
        else:
            self.title = False

    def getValueLocation(self):
        if self.valueLocation == 'top':
            self.valueRect = self.valueImage.get_rect(centerx = self.rect.centerx, bottom = self.rect.top - 8)
        elif self.valueLocation == 'bottom':
            self.valueRect = self.valueImage.get_rect(centerx = self.rect.centerx, top = self.rect.bottom + 10)
        elif self.valueLocation == 'left':
            self.valueRect = self.valueImage.get_rect(centery = self.rect.centery, right = self.rect.left - 10)
        elif self.valueLocation == 'right':
            self.valueRect = self.valueImage.get_rect(centery = self.rect.centery, left = self.rect.right + 8)
        else:
            self.showValue = False

    def moveHandle(self, pos):
        parentOpen = True
        if self.parent:
            if not self.parent.active:
                parentOpen = False
        # modalClick = False
        if self.rect.collidepoint(pos) and pg.mouse.get_pressed()[0] and parentOpen:
            self.handleRect.centerx = pos[0]
            if self.handleRect.left < self.rect.left + self.offset:
                self.handleRect.left = self.rect.left + self.offset / 2
            if self.handleRect.right > self.rect.right - self.offset:
                self.handleRect.right = self.rect.right - self.offset / 2

            try:
                distance = (self.handleRect.left - (self.rect.left + (self.offset / 2)))
                jumpDist = (self.rect.width - (self.offset * 2)) / self.maxVal
                self.value = round((distance / (self.rect.width - (self.offset * 2))) * self.maxVal)
                self.activeImage = pg.Surface([self.value * jumpDist, (self.height - self.offset)])
                self.activeImage.fill(self.activeColor)
                self.activeRect = self.activeImage.get_rect(centery = self.rect.centery, left = (self.rect.left + self.offset / 2))
                
                if self.showValue:
                    self.valueImage = self.textFont.render(f'{self.value}', True, self.textColor)
                    self.getValueLocation()
            except:
                pass
    
    def update(self, screen):
        if self.title:
            screen.blit(self.titleImage, self.titleRect)
        if self.showValue:
            screen.blit(self.valueImage, self.valueRect)
        screen.blit(self.image, self.rect)
        screen.blit(self.activeImage, self.activeRect)
        screen.blit(self.handleImage, self.handleRect)
            