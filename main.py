#this is a post-it application built with Python and pygame
from math import floor
import textwrap
import pygame as pg
from textwrap import TextWrapper
import sys
import json
from time import gmtime, strftime, localtime
from random import randint

from errorHandler import handleError

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    screen_width = 600
    screen_height = 600
    wrapper = TextWrapper(initial_indent="* ")
    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()
    currentUser = None
    
    #colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    FUCHSIA = (255, 0, 255)
    LIME = (0, 128, 0)
    MAROON = (128, 0, 0)
    NAVYBLUE = (0, 0, 128)
    OLIVE = (128, 128, 0)
    PURPLE = (128, 0, 128)
    TEAL = (0,128,128)
    
    GRAY = (128, 128, 128)
    LIGHTGREY = (170, 170, 170)
    DARKGREY = (100, 100, 100)
    
    activeColor = BLACK
    inactiveColor = LIGHTGREY
    
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
    #allPygameFonts = pg.font.get_fonts()
    
    defaultButtonFont = allFonts['largeConsolas']
    defaultTextInputFont = allFonts['largeConsolas']
    
    class User:
        def __init__(self):
            self.loggedIn = False
            self.name = ''
            self.userName = ''
            self.password = None
            
        def loginUser(self, userName, password):
            try:
                with open('allNotes/allUsers.json', 'r') as infile:
                    data = json.load(infile)
                    try:
                        print('userName ==> ', userName)
                        self.password = data[userName][0]['password']
                        self.name = data[userName][0]['name']
                        print('password ==> ', self.password)
                        print('name ==> ', self.name)
                    except Exception as err:
                        print(err)
                        handleError(err)
                    #print(data)
            except Exception as err:
                handleError(err)
                print('error ==> ', err)
                
    class Modal:
        instances = []
        def __init__(
            self,
            x,
            y,
            width,
            height,
            title: list,
            children: list = [],
            textColor = BLACK,
            textFont = defaultTextInputFont,
            backgroundColor = TEAL
        ):
            self.__class__.instances.append(self)
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.textColor = textColor
            self.textFont = allFonts[textFont] if textFont in allFonts else defaultTextInputFont
            self.backgroundColor = backgroundColor
            self.image = pg.Surface([width, height])
            self.rect = self.image.get_rect(topleft = (x, y))
            try:
                self.title = title
                self.titleFont = title[1] if title[1] else defaultTextInputFont
                self.textImage = self.textFont.render(self.title, True, self.textColor)
                self.textRect = self.textImage.get_rect(top = self.rect.top + 15, left = self.rect.left + 15)
                try:
                    self.image.fill(self.backgroundColor)
                except Exception as err:
                    self.image.fill(RED)
                    self.backgroundColor = RED
                    handleError(err)
            except Exception as err:
                self.title = False
                self.titleFont = ''
                handleError(err)
            self.children = children if type(children) == list else [children]
            self.active = False
            
        def update(self):
            if self.active:
                screen.blit(self.image, self.rect)
                screen.blit(self.textImage, self.textRect)
                for child in self.children:
                    try:
                        if type(child) == Button:
                            child.check_click(mouse)
                            child.draw_button(screen)
                        if type(child) == InputBox:
                            pass
                    except Exception as err:
                        handleError(err)
                
            
    class Button(pg.sprite.Sprite):
        instances = []
        user = None
        def __init__(self, width, height, x, y, color = RED, text = False, textColor = BLACK, textFont = defaultButtonFont):
            self.__class__.instances.append(self)
            pg.sprite.Sprite.__init__(self)
            self.image = pg.Surface([width, height])
            self.rect = self.image.get_rect(topleft = (x, y))
            self.onClickFunction = False
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
            
        def check_click(self, mouse):
            if self.rect.collidepoint(mouse):
                if self.onClickFunction and not self.disabled:
                    self.onClickFunction()
                else:
                    print(f"hit button")
        
        def draw_button(self, screen):
            screen.blit(self.image, self.rect)
            if self.text:
                self.textImage = self.textFont.render(self.text, True, self.textColor)
                self.textRect = self.textImage.get_rect(center = self.rect.center)
                screen.blit(self.textImage, self.textRect)
                
    class InputBox:
        instances = []
        def __init__ (self, x, y, width, height, text = '', textFont = defaultTextInputFont, changeable = True, activeColor = BLACK, inactiveColor = LIGHTGREY):
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
        
        def handle_event(self, event):
            modalsActive = False
            for modal in Modal.instances:
                if modal.active:
                    modalsActive = True
            if not modalsActive:
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
                        
        def textWrap(self):
            textLines = []
            textWidth = self.textFont.size(' ')[0]
            maxChars = floor(self.rect.width / textWidth)
            textLinesToBe = textwrap.wrap(self.text, maxChars)
            #self.text = textLinesToBe[0] if len(textLinesToBe) > 0 else self.text
            #print(textLinesToBe)
            
            #print(f'{self.textFont.size(self.text)[0]} ==> {len(self.text)}')
            #print(textLinesToBe)
                        
        def update(self):
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
                        
    #*--------------------------------------
    def check_click(mouse):
        for button in Button.instances:
            button.check_click(mouse)
        #add other class instances here
            
    def drawEverything(screen):
        for button in Button.instances:
            button.draw_button(screen)
        newNoteButton.text = 'new note' if Button.user else 'currentUser'
        #print(newNoteButton.text)
        for box in InputBox.instances:
            #if box != inputBox2:
            box.update()
            box.draw(screen)
        testModal.update()
            
    def handleEventListener(event):
        for box in InputBox.instances:
            box.handle_event(event)
            
    #user
    currentUser = User()
    
    testModal = Modal(100, 100, 400, 400, 'title here')
    testModal.active = True
    
    loginBox = 0
    
    #* all buttons        
    quitButton = Button((screen_width/2), (screen_height/8), 0, 0, text = 'quit', textFont = 'largeConsolas')
    def quitButtonFunct():
        pg.quit()
        sys.exit()
    quitButton.onClickFunction = quitButtonFunct
    
    newNoteButton = Button((screen_width/2), (screen_height/8), (screen_width/2), 0, color = BLUE, textColor = WHITE, text = 'new note')
    def newNoteFunct():
        #print('new note')
        Button.user = 'user' if not Button.user else None
        currentUser.loginUser('pjsanto', '')
    newNoteButton.onClickFunction = newNoteFunct
    #testButton = Button(100, 50, (screen_width/2), (screen_width/2), color=('#52325c'), text = 'test')
    
    #* text boxes
    statusBox = InputBox(0, (quitButton.rect.height), screen_width, 50, 'status box', changeable = False)
    statusBox.static = True
    
    bottomStatusBox = statusBox
    
    inputBox1 = InputBox(25, (bottomStatusBox.rect.bottom), (screen_width - 50), 400)
    #testWords = 'wow this is cool \n ok i pull up'
    #inputBox2 = InputBox(25, -250, (screen_width - 50), 100, testWords) #(inputBox1.rect.bottom)
    
    saveButton = Button((screen_width/2), (screen_height/8), 0, (inputBox1.rect.bottom + 5), color = GREEN, text = 'save note', textFont = 'largeOldEnglishText')
    def saveButtonFunct():
        print('save button')
    saveButton.onClickFunction = saveButtonFunct
    
    cancelButton = Button((screen_width/2), (screen_height/8), (saveButton.rect.right), (inputBox1.rect.bottom + 5), color = RED, text = 'Cancel')
    def cancelButtonFunct():
        inputBox1.text = ''
    cancelButton.onClickFunction = cancelButtonFunct

    #* timer that goes off every 800 miliseconds
    #fontTimer = pg.USEREVENT + 1
    #pg.time.set_timer(fontTimer, 800)
            
    while True:
        allEvents = pg.event.get()
        for event in allEvents:
            keys = pg.key.get_pressed()
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit(1)
            if event.type == pg.MOUSEBUTTONDOWN:
                check_click(mouse)
            handleEventListener(event)

        screen.fill(DARKGREY) #* sets the screen a certain color
        mouse = pg.mouse.get_pos() #* gets the position of the mouse

        drawEverything(screen)
        
        pg.display.flip()
        clock.tick(60)