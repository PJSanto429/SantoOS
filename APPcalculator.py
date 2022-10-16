
#!-----local imports-----
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from clock import Clock
from loading import Loading
from randomFuncts import handleQuit
from user import *
from variables import *

#*------------------ main calculator ----------------------

def doMath(equation):
    try:
        completeMath = False
        for i in '/*+-':
            if i in equation:
                completeMath = True
        if completeMath:
            while equation[-1] in '/*+-':
                funct = funct[:-1]
            return f'{eval(equation)}'
        return equation
    except:
        return 'error'

calcHeader = InputBox(0, 5, screen_width, 50, 'Calculator', changeable=False, inactiveColor=BLACK, parentApp='calculatorMain', center=True, showRect=False)

calcMainInput = InputBox(0, 50, screen_width, 50, 'Enter Equation', changeable=False, inactiveColor=BLACK, parentApp='calculatorMain')
calcMainInputRect = calcMainInput.rect
calcMainInput.eraseAll = True

clearCalcButton = Button(0, calcMainInputRect.bottom, (screen_width / 2), 100, RED, 'CE', parentApp='calculatorMain', showOutline=True)
clearCalcRect = clearCalcButton.rect
def clearCalcFunct():
    calcMainInput.text = 'Enter Equation'
    calcMainInput.eraseAll = True
clearCalcButton.onClickFunction = clearCalcFunct

calcHomeButton = Button(clearCalcRect.right, clearCalcRect.y, (clearCalcRect.width / 2), clearCalcRect.height, BLUE, 'Home', parentApp='calculatorMain', showOutline=True)
calcHomeRect = calcHomeButton.rect
def calcHomeFunct():
    allApps['homeLoggedIn'] = True
    allApps['calculatorMain'] = False
calcHomeButton.onClickFunction = calcHomeFunct

calcDivideButton = Button(calcHomeRect.right, calcHomeRect.y, calcHomeRect.width, calcHomeRect.height, ORANGE, '/', parentApp='calculatorMain', showOutline=True)
calcDivideRect = calcDivideButton.rect

calcMultiplyButton = Button(calcDivideRect.x, calcDivideRect.bottom, calcDivideRect.width, calcDivideRect.height, ORANGE, '*', parentApp='calculatorMain', showOutline=True)
calcMultiplyRect = calcMultiplyButton.rect

calcMinusButton = Button(calcMultiplyRect.x, calcMultiplyRect.bottom, calcMultiplyRect.width, calcMultiplyRect.height, ORANGE, '-', parentApp='calculatorMain', showOutline=True)
calcMinusRect = calcMinusButton.rect

calcAddButton = Button(calcMinusRect.x, calcMinusRect.bottom, calcMinusRect.width, calcMinusRect.height, ORANGE, '+', parentApp='calculatorMain', showOutline=True)
calcAddRect = calcAddButton.rect

calcEqualButton = Button(calcAddRect.x, calcAddRect.bottom, calcAddRect.width, calcAddRect.height, ORANGE, '=', parentApp='calculatorMain', showOutline=True)
def calcEqualFunct():
    calcMainInput.eraseAll = True
    calcMainInput.text = doMath(calcMainInput.text)
calcEqualButton.onClickFunction = calcEqualFunct

calcSevenButton = Button(0, clearCalcRect.bottom, (clearCalcRect.width / 2), clearCalcRect.height, GREEN, '7', parentApp='calculatorMain', showOutline=True)
calcSevenRect = calcSevenButton.rect

calcEightButton = Button(calcSevenRect.right, calcSevenRect.y, calcSevenRect.width, calcSevenRect.height, GREEN, '8', parentApp='calculatorMain', showOutline=True)
calcEightRect = calcEightButton.rect

calcNineButton = Button(calcEightRect.right, calcEightRect.y, calcEightRect.width, calcEightRect.height, GREEN, '9', parentApp='calculatorMain', showOutline=True)
calcNineRect = calcNineButton.rect

calcFourButton = Button(0, calcNineRect.bottom, calcNineRect.width, calcNineRect.height, GREEN, '4', parentApp='calculatorMain', showOutline=True)
calcFourRect = calcFourButton.rect

calcFiveButton = Button(calcFourRect.right, calcFourRect.y, calcFourRect.width, calcFourRect.height, GREEN, '5', parentApp='calculatorMain', showOutline=True)
calcFiveRect = calcFiveButton.rect

calcSixButton = Button(calcFiveRect.right, calcFiveRect.y, calcFiveRect.width, calcFiveRect.height, GREEN, '6', parentApp='calculatorMain', showOutline=True)
calcSixRect = calcSixButton.rect

calcOneButton = Button(0, calcSixRect.bottom, calcSixRect.width, calcSixRect.height, GREEN, '1', parentApp='calculatorMain', showOutline=True)
calcOneRect = calcOneButton.rect

calcTwoButton = Button(calcOneRect.right, calcOneRect.y, calcOneRect.width, calcOneRect.height, GREEN, '2', parentApp='calculatorMain', showOutline=True)
calcTwoRect = calcTwoButton.rect

calcThreeButton = Button(calcTwoRect.right, calcTwoRect.y, calcTwoRect.width, calcTwoRect.height, GREEN, '3', parentApp='calculatorMain', showOutline=True)
calcThreeRect = calcThreeButton.rect

calcZeroButton = Button(calcThreeRect.right, calcThreeRect.bottom, calcThreeRect.width, calcThreeRect.height, GREEN, '0', parentApp='calculatorMain', showOutline=True)
calcZeroButton.rect.right = clearCalcRect.right
calcZeroRect = calcZeroButton.rect

calcPeriodButton = Button(calcZeroRect.right, calcZeroRect.y, calcZeroRect.width, calcZeroRect.height, GREEN, '.', parentApp='calculatorMain', showOutline=True)

for button in Button.instances:
    if button.parentApp == 'calculatorMain':
        if button not in [clearCalcButton, calcHomeButton, calcEqualButton]:
            button.group = ['calc', calcMainInput]
