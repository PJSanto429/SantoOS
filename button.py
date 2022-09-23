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
    def __init__(
        self,
        x,
        y,
        width,
        height,
        color = RED,
        text = False,
        textColor = BLACK,
        textFont = defaultButtonFont,
        parent = False,
        parentApp = 'none',
        picture = False,
        
    ):
        self.__class__.instances.append(self)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect(topleft = (x, y))
        self.onClickFunction = buttonFunct
        self.color = color
        self.picture = picture
        if self.picture:
            try:
                self.picture = pg.image.load(self.picture).convert_alpha()
                self.picture = pg.transform.scale(self.picture, (width, height))
            except Exception as err:
                handleError(err)
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
        self.parentApp = parentApp
        self.parent = parent #Modal
        #if self.parent:
        #    childToParent(self, parent)
        
    def check_click(self, mouse):
        if self.parent:
            if self.parent.active:
                parentActive = True
        else:
            parentActive = True
        if self.rect.collidepoint(mouse):
            if not self.disabled and parentActive:
                if self.parent:
                    if self.parent.active:
                        self.onClickFunction()
                else:
                    self.onClickFunction()
    
    def draw_button(self, screen):
        #if self.parent:
        #    if self.parent.active:
        screen.blit(self.image, self.rect)
        if self.picture:
            screen.blit(self.picture, self.rect)
        if self.text:
            self.textImage = self.textFont.render(self.text, True, self.textColor)
            self.textRect = self.textImage.get_rect(center = self.rect.center)
            screen.blit(self.textImage, self.textRect)