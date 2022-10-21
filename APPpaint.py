import json
from random import choice, randint
import pygame as pg

from inputBox import InputBox
from modal import Modal
from button import Button
from variables import *
from randomFuncts import *

paintMainHeader = InputBox(0, 10, screen_width, 40, 'Paint', showRect=False, changeable=False, inactiveColor=BLACK, parentApp='paintMain', center=True)
paintMainRect = paintMainHeader.rect

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
            for i in self.colorInputs:
                i.text = '255' if int(i.text) > 255 else i.text 
            self.paintColor = (int(self.colorInputs[0].text), int(self.colorInputs[1].text), int(self.colorInputs[2].text))
            paintShowColorButton.color = self.paintColor
        except:
            pass
        for group in self.resetStuff:
            if type(group) == Button:
                group.draw_button(screen)
            if type(group) == InputBox:
                group.draw(screen)
        screen.blit(self.mainPaintBodyImage, self.mainPaintBodyRect)

    def checkClick(self, mouse):
        if mainPaintBodyRect.collidepoint(mouse) and pg.mouse.get_pressed()[0]:
            self.circles[len(self.circles)] = f'{self.paintColor}|{mouse}|{self.brushSize}'
            pg.draw.circle(screen, self.paintColor, mouse, self.brushSize)

    def run(self, mouse):
        self.resetScreen()
        self.drawPainting()
        self.checkClick(mouse)

mainPaintBodyImage = pg.Surface([screen_width, 450])
mainPaintBodyImage.fill(WHITE)
mainPaintBodyRect = mainPaintBodyImage.get_rect(topleft = (0, (paintMainRect.bottom + 10)))

redColorValueInput = InputBox(0, 0, 150, 50, '0', parentApp='paintMain', maxChars=3, allowedChars='int')
redColorValueInput.rect.bottom = screen_height
redColorRect = redColorValueInput.rect

blueColorValueInput = InputBox(redColorRect.right, redColorRect.y, redColorRect.width, redColorRect.height, '0', parentApp='paintMain', maxChars=3, allowedChars='int')
blueColorRect = blueColorValueInput.rect

greenColorValueInput = InputBox(blueColorRect.right, redColorRect.y, redColorRect.width, redColorRect.height, '0', parentApp='paintMain', maxChars=3, allowedChars='int')
greenColorRect = greenColorValueInput.rect

redColorValueInput.edited = blueColorValueInput.edited = greenColorValueInput.edited = True
redColorValueInput.useCursor = blueColorValueInput.useCursor = greenColorValueInput.useCursor = False

resetSize = mainPaintBodyRect.top
mainPaintResetButton = Button(0, 0, resetSize, resetSize, picture='assets/resetLogo.png', parentApp='paintMain')

paintShowColorButton = Button(greenColorRect.right, (screen_height - 50), 50, 50, BLACK, parentApp='paintMain')
# paintShowColorButton.rect.bottom = screen_height
# paintShowColorButton.rect.height = greenColorRect.height

mainPaint = paintApp(
    [mainPaintBodyImage, mainPaintBodyRect],
    (
        paintMainHeader,
        mainPaintResetButton,
        paintShowColorButton,
        redColorValueInput,
        greenColorValueInput,
        blueColorValueInput
    ),
    (
        redColorValueInput,
        greenColorValueInput,
        blueColorValueInput
    )
)

def mainPaintResetFunct():
    print(mainPaint.circles)
    mainPaint.circles = {}
mainPaintResetButton.onClickFunction = mainPaintResetFunct
