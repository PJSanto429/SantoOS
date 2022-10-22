import json
import pygame as pg

from inputBox import InputBox
from modal import Modal
from slider import Slider
from button import Button
from variables import *
from randomFuncts import *

# paintMainHeader = InputBox(0, 10, screen_width, 40, 'Paint', showRect=False, changeable=False, inactiveColor=BLACK, parentApp='paintMain', center=True)
# paintMainRect = paintMainHeader.rect

class paintApp():
    def __init__(self, mainBody, resetStuff, colorInputs):
        self.tickSpeed = 6000
        self.running = False
        self.backgroundDrawn = False
        self.paintColor = BLACK
        self.circles = {}
        
        self.mainPaintBodyImage = mainBody[0]
        self.mainPaintBodyRect = mainBody[1]
        
        self.resetStuff = resetStuff
        self.colorInputs = colorInputs

        self.brushSizes = {
            "small": 5,
            "medium": 10,
            "large": 20
        }
        self.brushSize = self.brushSizes['small']
        
    def drawPainting(self):
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
        self.backgroundDrawn = True
        screen.fill(TEAL)
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
        screen.blit(self.mainPaintBodyImage, self.mainPaintBodyRect)

    def checkClick(self, mouse):
        if mainPaintBodyRect.collidepoint(mouse) and pg.mouse.get_pressed()[0]:
            self.circles[len(self.circles)] = f'{self.paintColor}|{mouse}|{self.brushSize}'
            pg.draw.circle(screen, self.paintColor, mouse, self.brushSize)

    def run(self, mouse):
        self.resetScreen()
        self.drawPainting()
        self.checkClick(mouse)

mainPaintBodyImage = pg.Surface([screen_width, 440])
mainPaintBodyImage.fill(WHITE)
mainPaintBodyRect = mainPaintBodyImage.get_rect(topleft = (0, 0))

redColorValueSlider = Slider(0, (mainPaintBodyRect.bottom + 50), (screen_width / 2), 55, 255, activeColor=RED, handleColor=WHITE, parentApp='paintMain')
redColorRect = redColorValueSlider.rect

greenColorValueSlider = Slider(0, redColorRect.bottom, redColorRect.width, redColorRect.height, 255, activeColor=GREEN, handleColor=WHITE, parentApp='paintMain')
greenColorRect = greenColorValueSlider.rect

blueColorValueSlider = Slider(redColorRect.right, greenColorRect.y, redColorRect.width, redColorRect.height, 255, activeColor=BLUE, handleColor=WHITE, parentApp='paintMain')
blueColorRect = blueColorValueSlider.rect

paintShowColorButton = Button(0, 0, 50, 50, BLACK, parentApp='paintMain')
paintShowColorButton.rect.centerx = blueColorRect.centerx
paintShowColorButton.rect.bottom = blueColorRect.top - 5

resetSize = 50
mainPaintResetButton = Button(0, mainPaintBodyRect.bottom, resetSize * 2, resetSize, picture='assets/resetLogo.png', parentApp='paintMain')

mainPaint = paintApp(
    [mainPaintBodyImage, mainPaintBodyRect],
    (
        # paintMainHeader,
        mainPaintResetButton,
        paintShowColorButton,
        redColorValueSlider,
        greenColorValueSlider,
        blueColorValueSlider
    ),
    (
        redColorValueSlider,
        greenColorValueSlider,
        blueColorValueSlider
    )
)

def mainPaintResetFunct():
    mainPaint.circles = {}
mainPaintResetButton.onClickFunction = mainPaintResetFunct
