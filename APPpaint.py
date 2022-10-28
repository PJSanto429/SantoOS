import json
from random import randint
import pygame as pg

from inputBox import InputBox
from modal import Modal
from slider import Slider
from button import Button
from variables import *
from randomFuncts import *

class paintApp():
    def __init__(self, mainBody, colorInputs, sizeInput):
        self.tickSpeed = 0
        self.running = False
        self.paintColor = BLACK
        self.circles = {}
        self.delayTime = 0
        
        self.mainPaintBodyImage = mainBody[0]
        self.mainPaintBodyRect = mainBody[1]
        
        self.colorInputs = colorInputs
        
        self.sizeInput = sizeInput
        self.brushSize = 10
        
    def drawPainting(self):
        # print(len(self.circles))
        screen.blit(self.mainPaintBodyImage, self.mainPaintBodyRect)
        for i in self.circles:
            try:
                data = self.circles[i]
                data = data.split('|')
                #* sets the color value
                color = data[0]
                for num in color:
                    color = color.replace(num, '') if num in '(),' else color
                color = tuple([int(x) for x in color.split()])
                # color = (randint(1, 255), randint(1, 255), randint(1, 255))
                #* sets the circle location
                location = data[1]
                for num in location:
                    location = location.replace(num, '') if num in '(),' else location
                location = tuple([int(x) for x in location.split()])
                # location = (randint(5, 595), randint(0, 400))
                #* sets the brush size
                brushSize = int(data[2])
                #! draws the circle
                pg.draw.circle(screen, color, location, brushSize)
            except:
                pass
        
    def resetScreen(self):
        screen.blit(backGroundHiderImage, backGroundHiderRect)
        screen.blit(backGroundHider2Image, backGroundHider2Rect)
        try:
            self.paintColor = (int(self.colorInputs[0].value), int(self.colorInputs[1].value), int(self.colorInputs[2].value))
            # self.paintColor = (randint(1, 255), randint(1, 255), randint(1, 255))
            paintShowColorButton.color = self.paintColor
        except:
            pass
        
    def drawLines(self, moving = False, static = False):
        mouse = pg.mouse.get_pos()
        if static:
            pg.draw.line(screen, BLACK, (0, 0), ((mainPaintBodyRect.w / 2), mainPaintBodyRect.h / 2))
            pg.draw.line(screen, BLACK, (screen_width / 2, 0), ((mainPaintBodyRect.w / 2), mainPaintBodyRect.h / 2))
            pg.draw.line(screen, BLACK, (screen_width, 0), ((mainPaintBodyRect.w / 2), mainPaintBodyRect.h / 2))
            pg.draw.line(screen, BLACK, (screen_width, mainPaintBodyRect.height / 2), ((mainPaintBodyRect.w / 2), mainPaintBodyRect.h / 2))
            pg.draw.line(screen, BLACK, (0, mainPaintBodyRect.height / 2), ((mainPaintBodyRect.w / 2), mainPaintBodyRect.h / 2))
            pg.draw.line(screen, BLACK, (0, mainPaintBodyRect.bottom), ((mainPaintBodyRect.w / 2), mainPaintBodyRect.h / 2))
            pg.draw.line(screen, BLACK, (mainPaintBodyRect.width / 2, mainPaintBodyRect.bottom), ((mainPaintBodyRect.w / 2), mainPaintBodyRect.h / 2))
            pg.draw.line(screen, BLACK, (screen_width, mainPaintBodyRect.bottom), ((mainPaintBodyRect.w / 2), mainPaintBodyRect.h / 2))
        
        if moving:
            size = (mainPaintBodyRect.height / 2) + mainPaintBodyRect.top
            pg.draw.aaline(screen, BLACK, (mainPaintBodyRect.topleft), mouse)                                 #top left
            pg.draw.aaline(screen, BLACK, (screen_width, mainPaintBodyRect.top), mouse)                       #top right
            pg.draw.aaline(screen, BLACK, (0, mainPaintBodyRect.bottom), mouse)                               #bottom left
            pg.draw.aaline(screen, BLACK, (screen_width, mainPaintBodyRect.bottom), mouse)                    #bottom right
            pg.draw.aaline(screen, BLACK, (screen_width / 2, mainPaintBodyRect.top), mouse)                   #top center
            pg.draw.aaline(screen, BLACK, (mainPaintBodyRect.width / 2, mainPaintBodyRect.bottom), mouse)     #bottom center
            pg.draw.aaline(screen, BLACK, (0, size), mouse)                                                   #center left
            pg.draw.aaline(screen, BLACK, (screen_width, size), mouse)                                        #center right
    
    def checkCollide(self):
        mouse = pg.mouse.get_pos()
        self.brushSize = int(self.sizeInput.value)
        self.brushSize = 5 if self.brushSize < 5 else self.brushSize
        currTicks = pg.time.get_ticks()
        # self.brushSize = (self.brushSize + 1) if (self.brushSize < 50) else 2
        
        if mainPaintBodyRect.collidepoint(mouse) and not paintChangeColorModal.active:
            if (currTicks - self.delayTime) / 1000 > .5:
                pg.mouse.set_visible(False)
                # circColor = ((255 - self.paintColor[0]), (255 - self.paintColor[1]), (255 - self.paintColor[2]))
                pg.draw.circle(screen, self.paintColor, mouse, self.brushSize, 2)
                if pg.mouse.get_pressed()[0]:
                    self.circles[len(self.circles)] = f'{self.paintColor}|{mouse}|{self.brushSize}'
                    # pg.draw.circle(screen, self.paintColor, mouse, self.brushSize)
        else:
            pg.mouse.set_visible(True)
        
    def run(self):
        if self.running:
            screen.fill(TEAL)
            self.drawPainting()
            self.resetScreen()
            self.checkCollide()
            self.drawLines(False, False)
        
mainPaintHeader = InputBox(0, 5, screen_width, 50, 'Paint', changeable=False, parentApp='paintMain', center=True, showRect=False, inactiveColor=BLACK)

paintHomeButton = Button(0, 0, 100, 50, BLUE, 'Home', WHITE, parentApp='paintMain', showOutline=True)
def paintHomeFunct():
    mainPaint.running = False
    allApps['paintMain'] = False
    allApps['homeLoggedIn'] = True
paintHomeButton.onClickFunction = paintHomeFunct

mainPaintBodyImage = pg.Surface([screen_width, 450])
mainPaintBodyImage.fill(WHITE)
mainPaintBodyRect = mainPaintBodyImage.get_rect(topleft = (0, 50))

backGroundHiderImage = pg.Surface([screen_width, (screen_height - mainPaintBodyRect.bottom)])
backGroundHiderImage.fill(TEAL)
backGroundHiderRect = backGroundHiderImage.get_rect(topleft = (0, mainPaintBodyRect.bottom))

backGroundHider2Image = pg.Surface([screen_width, mainPaintBodyRect.top])
backGroundHider2Image.fill(TEAL)
backGroundHider2Rect = backGroundHider2Image.get_rect(topleft = (0, 0))

paintChangeColorModal = Modal(0, 0, 400, 400, 'Brush Settings', parentApp='paintMain', textColor=WHITE)
# paintChangeColorModal.active = True
paintChangeColorModal.rect.center = (screen_width / 2, screen_height / 2)
paintChangeColorRect = paintChangeColorModal.rect

closePaintColorButton = Button(0, 0, 50, 50, RED, parentApp='paintMain', parent=paintChangeColorModal, picture='assets/closeXLogo.png')
closePaintColorButton.rect.topright = paintChangeColorRect.topright
def closePaintColorFunct():
    paintChangeColorModal.active = False
    mainPaint.delayTime = pg.time.get_ticks()
closePaintColorButton.onClickFunction = closePaintColorFunct

brushSizeValueSlider = Slider(0, mainPaintBodyRect.bottom, (paintChangeColorRect.width - 50), 35, maxVal=30, activeColor=WHITE, handleColor=LIGHTGREY, parentApp='paintMain')#, parent=paintChangeColorModal)
brushSizeValueRect = brushSizeValueSlider.rect

redColorValueSlider = Slider(paintChangeColorRect.x, (paintChangeColorRect.y + 85), (paintChangeColorRect.width - 70), 55, 255, ['Red', 'top'], [True, 'right'], activeColor=RED, handleColor=RED, parentApp='paintMain', parent=paintChangeColorModal)
redColorRect = redColorValueSlider.rect

greenColorValueSlider = Slider(redColorRect.x, (redColorRect.bottom + 50), redColorRect.width, redColorRect.height, 255, ['Green', 'top'], [True, 'right'], activeColor=GREEN, handleColor=GREEN, parentApp='paintMain', parent=paintChangeColorModal)
greenColorRect = greenColorValueSlider.rect

blueColorValueSlider = Slider(redColorRect.x, (greenColorRect.bottom + 50), redColorRect.width, redColorRect.height, 255, ['Blue', 'top'], [True, 'right'], activeColor=BLUE, handleColor=BLUE, parentApp='paintMain', parent=paintChangeColorModal)
blueColorRect = blueColorValueSlider.rect

mainPaintResetButton = Button(0, 0, 50, 50, picture='assets/resetLogo.png', parentApp='paintMain')
mainPaintResetButton.rect.right = screen_width
mainPaintResetRect = mainPaintResetButton.rect

customColorInput = InputBox(0, 0, 160, 35, 'Custom Color:', 'smallConsolas', False, inactiveColor=BLACK, parentApp='paintMain', showRect=False)
customColorInput.rect.bottom = screen_height
customColorRect = customColorInput.rect

paintShowColorButton = Button(customColorRect.right, customColorRect.y, 50, 50, BLACK, parentApp='paintMain')
paintShowColorButton.rect.bottom = screen_height
paintShowColorButton.showOutline, paintShowColorButton.outlineColor = [True, WHITE]
def paintShowColorFunct():
    try:
        paintChangeColorModal.active = True if not paintChangeColorModal.active else False
        # pg.image.save(screen, 'allNotes/testImage.png')
        # with open('allNotes/paintTest2.json', 'r') as infile:
        #    inData = json.load(infile)
        #    mainPaint.circles = inData
    except:
        print('error')
paintShowColorButton.onClickFunction = paintShowColorFunct

mainPaint = paintApp(
    [mainPaintBodyImage, mainPaintBodyRect],
    (
        redColorValueSlider,
        greenColorValueSlider,
        blueColorValueSlider
    ),
    (
        brushSizeValueSlider
    )
)

def mainPaintResetFunct():
    print(len(mainPaint.circles))
    # try:
    #     with open(f'allNotes/textPaint.json', 'w') as outfile:
    #         x = json.dumps(mainPaint.circles)
    #         outfile.write(x)
    # except:
    #     pass
    mainPaint.circles = {}
mainPaintResetButton.onClickFunction = mainPaintResetFunct
