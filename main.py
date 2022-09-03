#this is a post-it application built with Python and pygame
import pygame as pg
import textwrap
import sys
import json
from time import gmtime, strftime
from random import randint

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    screen_width = 600
    screen_height = 600
    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()
    
    #colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    lightGrey = (170, 170, 170)
    darkGrey = (100, 100, 100)
    
    activeColor = black
    inactiveColor = lightGrey
    
    #fonts
    allFonts = {
        # large fonts
        "largeAlgerian": pg.font.SysFont('algerian', 35),
        "largeBauhaus": pg.font.SysFont('bauhaus93', 35),
        "largeConsolas": pg.font.SysFont('consolas', 35),
        "largeImpact": pg.font.SysFont('impact', 35),
        "largeLucidaConsole": pg.font.SysFont('lucidaconsole', 35),
        "largeSegoeuiBlack": pg.font.SysFont('segoeuiblack', 35),
        "largeAgencyfb": pg.font.SysFont('agencyfb', 35),
        "largeBlackAdderitc": pg.font.SysFont('blackadderitc', 35),
        "largeBritannic": pg.font.SysFont('britannic', 35),
        "largeCastellar": pg.font.SysFont('castellar', 35),
        "largeColonna": pg.font.SysFont('colonna', 35),
        "largeEngravers": pg.font.SysFont('engravers', 35),
        "largeLucidaHandwriting": pg.font.SysFont('lucidahandwriting', 35),
        "largeLucidaSansTypewriter": pg.font.SysFont('lucidasanstypewriter', 35),
        "largeMagneto": pg.font.SysFont('magneto', 35),
        "largeNiagaraSolid": pg.font.SysFont('niagarasolid', 35),
        "largeOldEnglishText": pg.font.SysFont('oldenglishtext', 35),
        "largeStencil": pg.font.SysFont('stencil', 35),
        "largeHPSimplifiedBDIT": pg.font.SysFont('largeHPSimplifiedBDIT', 35),
        "largeHPSimplified": pg.font.SysFont('hpsimplified', 35),
        "largeArial": pg.font.SysFont('arial', 35)
    }
    #allFonts = pg.font.get_fonts()
    
    defaultButtonFont = allFonts['largeAlgerian']
    defaultTextInputFont = allFonts['largeConsolas']
    
    class Button(pg.sprite.Sprite):
        instances = []
        def __init__(self, width, height, x, y, color = red, text = False, textColor = black, textFont = defaultButtonFont):
            self.__class__.instances.append(self)
            pg.sprite.Sprite.__init__(self)
            self.image = pg.Surface([width, height])
            self.rect = self.image.get_rect(topleft = (x, y))
            self.onClickFunction = False
            self.textFont = allFonts[textFont] if textFont in allFonts else defaultButtonFont
            try:
                self.image.fill(color)
            except:
                self.image.fill(red)
            self.text = text
            if self.text:
                self.textImage = self.textFont.render(self.text, True, textColor)
                self.textRect = self.textImage.get_rect(center = self.rect.center)
            
        def check_click(self, mouse):
            if self.rect.collidepoint(mouse):
                if self.onClickFunction:
                    self.onClickFunction()
                else:
                    print(f"hit button")
        
        def draw_button(self, screen):
            screen.blit(self.image, self.rect)
            if self.text:
                screen.blit(self.textImage, self.textRect)
                
    class InputBox:
        instances = []
        def __init__ (self, x, y, width, height, text = '', textFont = defaultTextInputFont, changeable = True, activeColor = black, inactiveColor = lightGrey):
            self.__class__.instances.append(self)
            self.rect = pg.Rect(x, y, width, height)
            self.color = inactiveColor
            self.activeColor = activeColor
            self.inactiveColor = inactiveColor
            self.text = text
            self.textFont = allFonts[textFont] if textFont in allFonts else defaultTextInputFont
            print(self.textFont)
            self.txt_surface = self.textFont.render(self.text, True, self.color)
            self.active = False
            self.changable = changeable
        
        def handle_event(self, event):
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active if self.changable else self.active
                else:
                    self.active = False
                self.color = self.activeColor if self.active else self.inactiveColor
            
            if event.type == pg.KEYDOWN:
                if self.active and self.changable:
                    #if event.key == pg.K_RETURN:
                    #    self.text = ''
                    if event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                        
        def update(self):
            width = max(200, self.txt_surface.get_width() + 10)
            self.txt_surface = self.textFont.render(self.text, True, self.color)
            #print(f'width ==> {self.txt_surface.get_width()}')
            #self.rect.w = screen_width - 50 #width
            
        def draw(self, screen):
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
            pg.draw.rect(screen, self.color, self.rect, 2)
                
    #*--------------------------------------
    def check_click(mouse):
        for button in Button.instances:
            button.check_click(mouse)
        #add other class instances here
            
    def drawEverything(screen):
        for button in Button.instances:
            button.draw_button(screen)
        for box in InputBox.instances:
            box.update()
            box.draw(screen)
            
    def handleEventListener(event):
        for box in InputBox.instances:
            box.handle_event(event)
    
    #* all buttons        
    quitButton = Button((screen_width/2), (screen_height/8), 0, 0, text = 'quit', textFont = 'largeConsolas')
    def quitButtonFunct():
        pg.quit()
        sys.exit()
    quitButton.onClickFunction = quitButtonFunct
    
    newNoteButton = Button((screen_width/2), (screen_height/8), (screen_width/2), 0, color=green, text = 'new note')
    def newNoteFunct():
        print('new note')
    #testButton = Button(100, 50, (screen_width/2), (screen_width/2), color=('#52325c'), text = 'test')
    
    #* text boxes
    statusBox = InputBox(0, (quitButton.rect.height), screen_width, 50, 'status box', changeable = False)
    
    inputBox1 = InputBox(25, (statusBox.rect.bottom), (screen_width - 50), 50)
    
    #* timer that goes off every 800 miliseconds
    #fontTimer = pg.USEREVENT + 1
    #pg.time.set_timer(fontTimer, 800)
    
    #fontNum = 0
    #likedFonts = []
    #with open('likedFonts.txt', 'r') as infile:
    #    likedFontsToBe = infile.read()
    #    for font in likedFonts:
    #        likedFonts.append(font)
            
    while True:
        allEvents = pg.event.get()
        for event in allEvents:
            keys = pg.key.get_pressed()
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                check_click(mouse)
            handleEventListener(event)

        screen.fill(darkGrey) #* sets the screen a certain color
        mouse = pg.mouse.get_pos() #* gets the position of the mouse

        drawEverything(screen)
        
        pg.display.flip()
        clock.tick(60)