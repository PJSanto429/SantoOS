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
    def __init__(self, mainBody, resetStuff, colorInputs, sizeInput):
        self.tickSpeed = 0
        self.running = False
        self.paintColor = BLACK
        self.circles = {}
        
        self.mainPaintBodyImage = mainBody[0]
        self.mainPaintBodyRect = mainBody[1]
        
        self.resetStuff = resetStuff
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
        try:
            self.paintColor = (int(self.colorInputs[0].value), int(self.colorInputs[1].value), int(self.colorInputs[2].value))
            paintShowColorButton.color = self.paintColor
        except Exception as err:
            print('error ==> ', err)
        # for group in self.resetStuff:
        #     if not group.parent:
        #         if type(group) == Button:
        #             group.draw_button(screen)
        #         if type(group) == InputBox:
        #             group.draw(screen)
        #         if type(group) == Slider:
        #             group.update(screen)
        #         if type(group) == Modal:
        #             group.update(screen)
    
    def checkCollide(self, mouse):
        self.brushSize = int(self.sizeInput.value)
        self.brushSize = 5 if self.brushSize < 5 else self.brushSize
        
        modalClick = False
        for thing in self.resetStuff:
            if type(thing) == Modal:
                if thing.active:# and thing.rect.collidepoint(mouse):
                    modalClick = True
        
        if mainPaintBodyRect.collidepoint(mouse) and not modalClick:
            pg.draw.circle(screen, self.paintColor, mouse, self.brushSize, 2)
            if pg.mouse.get_pressed()[0]:
                self.circles[len(self.circles)] = f'{self.paintColor}|{mouse}|{self.brushSize}'
                pg.draw.circle(screen, self.paintColor, mouse, self.brushSize)
    
    def run(self, mouse):
        self.drawPainting()
        self.resetScreen()
        self.checkCollide(mouse)

mainPaintBodyImage = pg.Surface([screen_width, 440])
mainPaintBodyImage.fill(WHITE)
mainPaintBodyRect = mainPaintBodyImage.get_rect(topleft = (0, 0))

backGroundHiderImage = pg.Surface([screen_width, (screen_height - mainPaintBodyRect.bottom)])
backGroundHiderImage.fill(TEAL)
backGroundHiderRect = backGroundHiderImage.get_rect(topleft = (0, mainPaintBodyRect.bottom))

paintChangeColorModal = Modal(0, 0, 400, 400, 'Brush Settings', parentApp='paintMain', textColor=WHITE)
paintChangeColorModal.rect.center = (screen_width / 2, screen_height / 2)
paintChangeColorRect = paintChangeColorModal.rect

brushSizeValueSlider = Slider(paintChangeColorRect.x, (paintChangeColorRect.y + 50), (paintChangeColorRect.width - 50), 55, maxVal=25, activeColor=WHITE, handleColor=LIGHTGREY, parentApp='paintMain', parent=paintChangeColorModal)
brushSizeValueRect = brushSizeValueSlider.rect

redColorValueSlider = Slider(brushSizeValueRect.x, brushSizeValueRect.bottom, brushSizeValueRect.width, brushSizeValueRect.height, 255, activeColor=RED, handleColor=RED, parentApp='paintMain', parent=paintChangeColorModal)
redColorRect = redColorValueSlider.rect

greenColorValueSlider = Slider(redColorRect.x, redColorRect.bottom, redColorRect.width, redColorRect.height, 255, activeColor=GREEN, handleColor=GREEN, parentApp='paintMain', parent=paintChangeColorModal)
greenColorRect = greenColorValueSlider.rect

blueColorValueSlider = Slider(redColorRect.x, greenColorRect.bottom, redColorRect.width, redColorRect.height, 255, activeColor=BLUE, handleColor=BLUE, parentApp='paintMain', parent=paintChangeColorModal)
blueColorRect = blueColorValueSlider.rect

resetSize = 50 * 2
mainPaintResetButton = Button(0, 0, resetSize, resetSize, picture='assets/resetLogo.png', parentApp='paintMain')
mainPaintResetButton.rect.bottom = screen_height
mainPaintResetRect = mainPaintResetButton.rect

loadPaintButton = Button(mainPaintResetRect.right, mainPaintResetRect.y, mainPaintResetRect.width, mainPaintResetRect.height, BLACK, 'load', parentApp='paintMain')
loadPaintRect = loadPaintButton.rect
def loadPaintFunct():
    try:
        paintChangeColorModal.active = True if not paintChangeColorModal.active else False
        # with open('allNotes/paintTest2.json', 'r') as infile:
        #     inData = json.load(infile)
        #     mainPaint.circles = inData
    except:
        pass
loadPaintButton.onClickFunction = loadPaintFunct

paintShowColorButton = Button(loadPaintRect.right, loadPaintRect.y, 50, 50, BLACK, parentApp='paintMain')
paintShowColorButton.showOutline, paintShowColorButton.outlineColor = [True, WHITE]


mainPaint = paintApp(
    [mainPaintBodyImage, mainPaintBodyRect],
    (
        paintChangeColorModal,
        # mainPaintResetButton,
        # paintShowColorButton,
        # loadPaintButton,
        # redColorValueSlider,
        # greenColorValueSlider,
        # blueColorValueSlider,
        # brushSizeValueSlider
    ),
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
    #     with open(f'allNotes/paintTest.json', 'w') as outfile:
    #         x = json.dumps(mainPaint.circles)
    #         outfile.write(x)
    # except:
    #     pass
    mainPaint.circles = {}
mainPaintResetButton.onClickFunction = mainPaintResetFunct
