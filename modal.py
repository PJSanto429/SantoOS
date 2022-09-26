import pygame as pg

#!----------local imports---------
from variables import *
from errorHandler import handleError
from randomFuncts import *
from button import Button
from inputBox import InputBox

pg.init()

class Modal:
    instances = []
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title,
        #children: list = [],
        textColor = BLACK,
        textFont = defaultTextInputFont,
        backgroundColor = DARKGREY,
        parentApp = 'none',
        parent = False
    ):
        self.__class__.instances.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.textColor = textColor
        self.parentApp = parentApp
        self.parent = parent
        self.textFont = allFonts[textFont] if textFont in allFonts else defaultTextInputFont
        self.backgroundColor = backgroundColor
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect(topleft = (x, y))
        try:
            self.title = title
            self.textImage = self.textFont.render(self.title, True, self.textColor)
            self.textRect = self.textImage.get_rect(top = self.rect.top + 15, left = self.rect.left + 15)#, centerx = self.rect.centerx/2)
            #print('text rect ==> ', self.textRect.centerx)
            #print('--------------------')
            #print('modal center ==> ', self.rect.centerx)
            #print('text rect center x ==> ', self.textRect.centerx)
            #print('------------------------------')
            
            textSize = self.textFont.size(self.title)
            #print('center x ==> ', self.textRect.centerx)
            self.textRect.width = textSize[0]
            self.textRect.centerx = self.rect.width/2
            #print('center x ==> ', self.textRect.centerx)
            #print(self.textRect.width)
            
            try:
                self.image.fill(self.backgroundColor)
            except Exception as err:
                self.image.fill(RED)
                self.backgroundColor = RED
                handleError(err)
        except Exception as err:
            self.title = False
            handleError(err)
        #//self.children = children if type(children) == list else [children]
        self.active = False
        
    def update(self, screen):
        if self.active:
            self.textImage = self.textFont.render(self.title, True, self.textColor)
            self.textRect = self.textImage.get_rect(top = self.rect.top + 15, left = self.rect.left + 15)
            screen.blit(self.image, self.rect)
            screen.blit(self.textImage, self.textRect)
            for button in Button.instances:
                if button.parent:
                    if button.parent == self:
                        button.draw_button(screen)
            for inputBox in InputBox.instances:
                if inputBox.parent:
                    if inputBox.parent == self:
                        inputBox.update()
                        inputBox.draw(screen)
            for modal in Modal.instances:
                if modal.parent:
                    if modal.parent == self:
                        modal.update(screen)