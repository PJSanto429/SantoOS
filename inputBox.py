import pygame as pg
import textwrap
from math import floor

#!------local imports------
from variables import *
from errorHandler import handleError
from randomFuncts import *
#from modal import Modal

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
        parentApp = 'none'
    ):
        self.__class__.instances.append(self)
        self.rect = pg.Rect(x, y, width, height)
        self.color = inactiveColor
        self.activeColor = activeColor
        self.inactiveColor = inactiveColor
        self.text = text
        self.textFont = allFonts[textFont] if textFont in allFonts else defaultTextInputFont
        self.txt_surface = self.textFont.render(self.text, True, self.color)
        self.active = False
        self.changable = changeable
        self.static = False
        self.edited = False
        self.parentApp = parentApp
        self.parent = parent #Modal
        childToParent(self, self.parent)
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active if self.changable else self.active
            else:
                self.active = False
            self.color = self.activeColor if self.active else self.inactiveColor
        
        if event.type == pg.KEYDOWN:
            if self.active and self.changable:
                if not self.edited:
                    self.edited = True
                    self.text = ''
                #if event.key == pg.K_RETURN:
                #    self.text = ''
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    
    def textWrap(self): #not working yet
        textLines = []
        textWidth = self.textFont.size(' ')[0]
        maxChars = floor(self.rect.width / textWidth)
        textLinesToBe = textwrap.wrap(self.text, maxChars)
        #self.text = textLinesToBe[0] if len(textLinesToBe) > 0 else self.text
        #print(textLinesToBe)
        
        #print(f'{self.textFont.size(self.text)[0]} ==> {len(self.text)}')
        #print(textLinesToBe)
                    
    def update(self):
        self.color = DARKGREY if self.static else self.color
        self.txt_surface = self.textFont.render(self.text, True, self.color)
        if self.static:
            self.txt_surface = self.textFont.render(self.text, True, self.color)
        else:
            self.textWrap()
            
            self.txt_surface = self.textFont.render(self.text, True, self.color)
            #if self.txt_surface.get_width() > self.rect.width - 5:
            #self.text = drawText(self.txt_surface, self.text, BLACK, self.rect, self.textFont)
            #print(f'self.text = {self.text}')
            
        #inputBox2.rect.top = self.rect.bottom
        #if self.txt_surface.get_width() > self.rect.width:
        #    self.rect.height += 50
            #print(f'it is over {self.rect.x}')
        
    def draw(self, screen):
        parentActive = False
        if self.parent:
            if self.parent.active:
                parentActive = True
        else:
            parentActive = True
        if parentActive:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
            pg.draw.rect(screen, self.color, self.rect, 2)
                
#! ------------------------------------------------------------------        
def blit_text(surface, text, pos, font, color = BLACK):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
        
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pg.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
#! ------------------------------------------------------------------