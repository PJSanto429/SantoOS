import json
from time import sleep
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
                #* sets the circle location
                location = data[1]
                for num in location:
                    location = location.replace(num, '') if num in '(),' else location
                location = tuple([int(x) for x in location.split()])
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
        except:
            pass
        for group in self.resetStuff:
            if type(group) == Button:
                group.draw_button(screen)
            if type(group) == InputBox:
                group.draw(screen)
            if type(group) == Slider:
                group.update(screen)
    
    def checkCollide(self, mouse):
        self.brushSize = int(self.sizeInput.value)
        self.brushSize = 5 if self.brushSize < 5 else self.brushSize
        if mainPaintBodyRect.collidepoint(mouse):
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

redColorValueSlider = Slider(0, (mainPaintBodyRect.bottom + 50), (screen_width / 2), 55, 255, activeColor=RED, handleColor=RED, parentApp='paintMain')
redColorRect = redColorValueSlider.rect

greenColorValueSlider = Slider(0, redColorRect.bottom, redColorRect.width, redColorRect.height, 255, activeColor=GREEN, handleColor=GREEN, parentApp='paintMain')
greenColorRect = greenColorValueSlider.rect

blueColorValueSlider = Slider(redColorRect.right, greenColorRect.y, redColorRect.width, redColorRect.height, 255, activeColor=BLUE, handleColor=BLUE, parentApp='paintMain')
blueColorRect = blueColorValueSlider.rect

brushSizeValueSlider = Slider(redColorRect.right, redColorRect.y, redColorRect.width, redColorRect.height, maxVal=25, activeColor=WHITE, handleColor=LIGHTGREY, parentApp='paintMain')

resetSize = 50
mainPaintResetButton = Button(0, mainPaintBodyRect.bottom, resetSize * 2, resetSize, picture='assets/resetLogo.png', parentApp='paintMain')
mainPaintResetRect = mainPaintResetButton.rect

loadPaintButton = Button(mainPaintResetRect.right, mainPaintResetRect.y, mainPaintResetRect.width, mainPaintResetRect.height, BLACK, 'load', parentApp='paintMain')
loadPaintRect = loadPaintButton.rect
def loadPaintFunct():
    try:
        with open('allNotes/paintTestsa.json', 'r') as infile:
            inData = json.load(infile)
            mainPaint.circles = inData
    except:
        pass
loadPaintButton.onClickFunction = loadPaintFunct

paintShowColorButton = Button(loadPaintRect.right, loadPaintRect.y, 50, 50, BLACK, parentApp='paintMain')
paintShowColorButton.showOutline, paintShowColorButton.outlineColor = [True, WHITE]

mainPaint = paintApp(
    [mainPaintBodyImage, mainPaintBodyRect],
    (
        mainPaintResetButton,
        paintShowColorButton,
        loadPaintButton,
        redColorValueSlider,
        greenColorValueSlider,
        blueColorValueSlider,
        brushSizeValueSlider
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
