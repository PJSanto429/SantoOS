import pygame as pg

#!-----local imports---
from variables import *
from errorHandler import handleError
from randomFuncts import *

pg.init()

def buttonFunct():
    print('hit button')
class Button(pg.sprite.Sprite):
    instances = []
    #user = None
    def __init__(self, x, y, width, height, color = RED, text = False, textColor = BLACK, textFont = defaultButtonFont, parent = False):
        self.__class__.instances.append(self)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect(topleft = (x, y))
        self.onClickFunction = buttonFunct
        self.color = color
        self.textColor = textColor
        self.textFont = allFonts[textFont] if textFont in allFonts else defaultButtonFont
        try:
            self.image.fill(self.color)
        except Exception as err:
            handleError(err)
            self.image.fill(RED)
        self.text = text
        if self.text:
            self.textImage = self.textFont.render(self.text, True, self.textColor)
            self.textRect = self.textImage.get_rect(center = self.rect.center)
        #* other various settings
        self.disabled = False
        self.active = False
        self.parent = parent #Modal
        childToParent(self, self.parent)
        
    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            if not self.disabled:
                if self.parent:
                    if self.parent.active:
                        self.onClickFunction()
                else:
                    self.onClickFunction()
    
    def draw_button(self, screen):
        screen.blit(self.image, self.rect)
        if self.text:
            self.textImage = self.textFont.render(self.text, True, self.textColor)
            self.textRect = self.textImage.get_rect(center = self.rect.center)
            screen.blit(self.textImage, self.textRect)