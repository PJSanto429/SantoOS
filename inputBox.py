import pygame as pg
import textwrap
from math import floor

#!------local imports------
from errorHandler import handleError
from randomFuncts import *
from variables import *

pg.init()

class InputBox:
    instances = []
    def __init__ (
        self,
        x,
        y,
        width,
        height,
        text = '',
        textFont = defaultTextInputFont,
        changeable = True,
        activeColor = BLACK,
        inactiveColor = LIGHTGREY,
        parent = False,
        parentApp = 'none',
        maxChars = 1000,
        allowedChars = 'all',
        group = 'input box',
        center = False,
        allowWrap = False,
        showRect = True,
        useDate = False,
        useTime = False
    ):
        self.__class__.instances.append(self)
        self.rect = pg.Rect(x, y, width, height)
        self.color = inactiveColor
        self.activeColor = activeColor
        self.inactiveColor = inactiveColor
        self.text = text
        self.maxChars = maxChars
        self.allowedChars = allowedChars
        self.allowWrap = allowWrap
        self.showRect = showRect
        self.textFont = allFonts[textFont] if textFont in allFonts else defaultTextInputFont
        self.txt_surface = self.textFont.render(self.text, True, self.color)
        self.active = False
        self.changable = changeable
        self.static = False
        self.edited = False
        self.useCursor = True
        self.cursor = False
        self.full = False
        self.onChange = False
        self.parentApp = parentApp
        self.parent = parent #Modal
        self.center = center
        if self.center:
            self.centerText()
        self.group = group
        self.useDate = useDate
        self.useTime = useTime
        
    def isActive(self):
        parentActive = False
        if self.parent:
            if self.parent.active:
                parentActive = True
        else:
            parentActive = True
        return parentActive
    
    def onChange(self):
        pass
    
    def enterEvent(self):
        pass
    
    def charCheck(self, character):
        charAllowed = True
        if self.allowedChars == 'int':
            if not character.isdigit:
                charAllowed = False
        
        return charAllowed
    
    def validate(self, character):
        if len(self.text) < self.maxChars and self.charCheck(character):
            return True
        return False
    
    def handle_event(self, event):
        try:
            maxChars = floor(self.rect.width / (self.textFont.size(' ')[0]))
            if checkMouseClick(event)[0]:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active if self.changable else self.active
                    if len(self.text) > 0:
                        if not self.active and self.text[-1] == '|':
                            self.text = self.text[:-1]
                else:
                    self.active = False
                    if len(self.text) > 0:
                        self.text = self.text[:-1] if self.text[-1] == '|' else self.text
                self.color = self.activeColor if self.active else self.inactiveColor
            
            if event.type == pg.KEYDOWN:
                if self.active and self.changable:
                    if not self.edited:
                        self.edited = True
                        self.text = ''
                    if event.key == pg.K_BACKSPACE:
                        if self.useCursor:
                            if len(self.text) > 1:
                                self.text = self.text[:-1] if self.text[-1] != '|' else self.text[:-2]
                            elif len(self.text) == 1 and self.text[-1] != '|':
                                self.text = self.text[:-1]
                        else:
                            self.text = self.text[:-1]# if self.text[-1] != '|' else self.text[:-2]
                    elif event.key == pg.K_RETURN:
                        self.enterEvent()
                    elif (event.unicode).isprintable() and event.unicode != '|' and not self.full:
                        if self.validate(event.unicode):
                            if len(self.text) > 0 and self.text[-1] == '|':
                                self.text = self.text[:-1]
                            if not self.allowWrap and len(self.text) >= maxChars:
                                self.text = self.text
                            else:
                                self.text += event.unicode
                    self.onChange()
        except:
            pass
                    
    def centerText(self):
        textSize = self.textFont.size(self.text)
        self.rect.width = textSize[0]
        self.rect.centerx = screen_width/2
                    
    def textWrap(self):
        offset = self.rect.x
        x = self.rect.x + 5
        y = self.rect.y + 5
        for line in self.textLines:
            for word in line:
                wordSurface = self.textFont.render(word, True, self.color)
                wordWidth, wordHeight = wordSurface.get_size()
                if (x - offset + wordWidth) >= self.rect.width:
                    x = self.rect.x + 5
                    y += wordHeight
                screen.blit(wordSurface, (x, y))
                x += wordWidth
            x = self.rect.x + 5
            y += wordHeight
            
    def showHideCursor(self):
        try:
            if self.active and self.useCursor:
                if not self.cursor:
                    textWidth = self.textFont.size(' ')[0]
                    if not self.allowWrap:
                        self.text += '|'
                        self.cursor = True
                    if (not (len(self.textLines[-1]) + 1) * textWidth > self.rect.width) and self.allowWrap:
                        self.text += '|'
                        self.cursor = True
                else:
                    self.text = self.text[:-1] if self.text[-1] == '|' else self.text
                    self.cursor = False
        except:
            pass
                    
    def update(self):
        if self.isActive():
            if self.group == 'input box':
                self.color = DARKGREY if self.static else self.color
                self.txt_surface = self.textFont.render(self.text, True, self.color)
                if self.static:
                    self.txt_surface = self.textFont.render(self.text, True, self.color)
                else:
                    if self.allowWrap:
                        textWidth, textHeight = self.textFont.size(' ')
                        maxChars = floor(self.rect.width / textWidth) - 1
                        self.textLines = ' ' if len(self.text) == 0 else textwrap.wrap(self.text, maxChars)
                        if (textHeight * len(self.textLines)) >= self.rect.height:
                            self.full = True
                        else:
                            self.full = False
                        self.textWrap()
                    else:
                        self.txt_surface = self.textFont.render(self.text, True, self.color)
                    
            if self.group == 'clock':
                localTime = currentTime(self.useDate, self.useTime)
                self.text = f'{localTime}'
                self.txt_surface = self.textFont.render(self.text, True, self.color)
        
    def draw(self, screen):
        if self.isActive():
            if not self.allowWrap:
                screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
                if self.center:
                    self.centerText()
            if self.showRect:
                pg.draw.rect(screen, self.color, self.rect, 2)