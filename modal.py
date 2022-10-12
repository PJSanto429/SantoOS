import pygame as pg

#!----------local imports---------
from variables import *
from errorHandler import handleError
from randomFuncts import *
from button import Button
from toggle import Toggle
from inputBox import InputBox
from loading import Loading

pg.init()

class Modal:
    instances = []
    topModal = False
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
            self.textRect = self.textImage.get_rect(top = self.rect.top + 15, left = self.rect.left + 15)
            try:
                self.image.fill(self.backgroundColor)
            except Exception as err:
                self.image.fill(RED)
                self.backgroundColor = RED
                handleError(err)
        except Exception as err:
            self.title = ''
            handleError(err)
        self.active = False
        
    def update(self, screen):
        if self.active:
            self.__class__.topModal = self
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
            for loading in Loading.instances:
                if loading.parent:
                    if loading.parent == self:
                        loading.update()
            for toggle in Toggle.instances:
                if toggle.parent:
                    if toggle.parent == self:
                        toggle.draw(screen)
            for modal in Modal.instances:
                if modal.parent:
                    if modal.parent == self:
                        modal.update(screen)