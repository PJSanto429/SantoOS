import pygame as pg

from variables import *

class Toggle:
    instances = []
    def __init__(
        self,
        x,
        y,
        width = 150,
        height = 75,
        onColor = GREEN,
        offColor = LIGHTGREY,
        bgColor = DARKGREY,
        text = False,
        textLocation = 'top',
        textColor = BLACK,
        textFont = defaultToggleFont,
        parent = False,
        parentApp = 'none',
    ):
        self.__class__.instances.append(self)
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect(topleft = (x, y))
        
        self.onColor = onColor
        self.offColor = offColor
        self.bgColor = bgColor
        
        self.text = text
        if self.text:
            self.textColor = textColor
            self.textFont = textFont
            allLocations = ['top', 'bottom', 'left', 'right']
            textLocation = textLocation.lower()
            self.textLocation = textLocation if textLocation in allLocations else 'top'
            self.textImage = self.textFont.render(self.text, True, self.textColor)
            self.getTextLocation()
        
        self.parent = parent
        self.parentApp = parentApp
        
        self.offset = 5
        self.toggleWidth = (self.rect.width - (self.offset * 3)) / 2
        self.toggleHeight = self.rect.height - (self.offset * 2)
        
        self.onImage = self.offImage = pg.Surface([self.toggleWidth, self.toggleHeight])
        self.offRect = self.onImage.get_rect(topleft = (x + self.offset, y + self.offset))
        self.onRect = self.onImage.get_rect(topleft = (x + self.offRect.width + (self.offset * 2), y + self.offset))
        self.image.fill(self.bgColor)
        self.onImage.fill(self.onColor)
        self.offImage.fill(self.offColor)
        self.on = False
        
    def getTextLocation(self):
        if self.textLocation == 'top':
            self.textRect = self.textImage.get_rect(centerx = self.rect.centerx, bottom = self.rect.top - 8)
        if self.textLocation == 'bottom':
            self.textRect = self.textImage.get_rect(centerx = self.rect.centerx, top = self.rect.bottom + 10)
        if self.textLocation == 'left':
            self.textRect = self.textImage.get_rect(centery = self.rect.centery, right = self.rect.left - 10)
        if self.textLocation == 'right':
            self.textRect = self.textImage.get_rect(centery = self.rect.centery, left = self.rect.right + 10)
        
    def onChangeEvent(self):
        if self.on:
            print('toggle turned on')
        else:
            print('toggle turned off')
        
    def checkClick(self, mouse, modals):
        parentOpen = True
        if self.parent:
            if not self.parent.active:
                parentOpen = False
        modalClick = False
        for modal in modals:
            if modal.active and modal.rect.collidepoint(mouse) and modal != self.parent:
                modalClick = True
        if self.rect.collidepoint(mouse):
            if parentOpen and not modalClick:
                if self.on:
                    self.offImage.fill(self.offColor)
                    self.on = False
                else:
                    self.onImage.fill(self.onColor)
                    self.on = True
                self.onChangeEvent()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.on:
            screen.blit(self.onImage, self.onRect)
        else:
            screen.blit(self.offImage, self.offRect)
        if self.text:
            self.textImage = self.textFont.render(self.text, True, self.textColor)
            self.getTextLocation()
            screen.blit(self.textImage, self.textRect)