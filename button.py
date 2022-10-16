import pygame as pg

#!-----local imports---
from variables import *
from errorHandler import handleError
from randomFuncts import *

pg.init()

class Button():
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
        showOutline = False,
        outlineColor = BLACK,
        parent = False,
        parentApp = 'none',
        picture = False,
        group = 'other',
        
    ):
        self.__class__.instances.append(self)
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect(topleft = (x, y))
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
            #handleError(err)
            self.image.fill(RED)
        self.text = text
        if self.text:
            self.textImage = self.textFont.render(self.text, True, self.textColor)
            self.textRect = self.textImage.get_rect(center = self.rect.center)
        self.showOutline = showOutline
        self.outlineColor = outlineColor
        self.outLineRect = pg.Rect(x, y, width, height)
        #* other various settings
        self.disabled = False
        self.group = group
        self.parentApp = parentApp
        self.parent = parent
        
    def onClickFunction(self):
        if self.group == 'other':
            print('hit button')
        else:
            if self.group[0] == 'calc':
                self.calculatorStuff()
                    
    def calculatorStuff(self):
        if self.group[1].eraseAll and self.text not in '-+/*=':
            self.group[1].eraseAll = False
            self.group[1].text = ''
        if self.text in '-+/*':
            if self.group[1].text != 'Enter Equation':
                self.group[1].eraseAll = False
                if len(self.group[1].text) > 0:
                    if self.group[1].text[-1] in '-+/*':
                        self.group[1].text = self.group[1].text[:-1]
                    self.group[1].text += self.text
        else:
            self.group[1].text += self.text

    def check_click(self, mouse, modals):
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
                if not self.disabled:
                    self.onClickFunction()
    
    def draw_button(self, screen):
        screen.blit(self.image, self.rect)
        if self.picture:
            screen.blit(self.picture, self.rect)
        if self.text:
            self.textImage = self.textFont.render(self.text, True, self.textColor)
            self.textRect = self.textImage.get_rect(center = self.rect.center)
            screen.blit(self.textImage, self.textRect)
        if self.showOutline:
            self.outLineRect = pg.Rect(self.rect)
            pg.draw.rect(screen, self.outlineColor, self.outLineRect, 2)