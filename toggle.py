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
        parent = False,
        parentApp = 'none',
    ):
        self.__class__.instances.append(self)
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect(topleft = (x, y))
        
        self.onColor = onColor
        self.offColor = offColor
        self.bgColor = bgColor
        
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