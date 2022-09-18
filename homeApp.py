import pygame as pg #?not needed?
from glob import glob

#!-----local imports-----
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from clock import Clock
from user import *
from variables import *

#*------------------ not logged in stuff -------------------
topHeader = InputBox(0, 10, 50, 0, 'SantoOS', 'extraLargeMagneto', False, parentApp='homeNotLoggedIn', inactiveColor=BLACK)
topHeader.rect.width = topHeader.textFont.size(topHeader.text)[0]
topHeader.rect.centerx = (screen_width / 2)

mainLogo = Button(0, (topHeader.rect.bottom + 100), 350, 350, parentApp='homeNotLoggedIn', picture='assets/mainIcon.png') # 
mainLogo.rect.centerx = screen_width / 2

currentCowImage = 1
dancingCowGif = Button(0, 0, 120, 120, picture='assets/dancingCow/frame_0.gif', parentApp='homeNotLoggedIn')

openLoginButton = Button((screen_width/4), (screen_width - (screen_height/8)), (screen_width/2), (screen_height/8), color = BLUE, textColor = WHITE, text = 'login', parentApp='homeNotLoggedIn')
def openLoginFunct():
    loginModal.active = True if not loginModal.active else False
openLoginButton.onClickFunction = openLoginFunct

def mainLogoFunct():
    print('main logo hit')
    #allApps["notes"] = True
    #allApps["homeNotLoggedIn"] = False
mainLogo.onClickFunction = mainLogoFunct

#* --------------- logged in stuff ---------------------
spacer = 18.75
userNameHeader = InputBox(0, 0, 50, 0, '', 'extraLargeHPSimplified', False, inactiveColor=BLACK, parentApp='homeLoggedIn')
userNameHeaderSize = userNameHeader.textFont.size(userNameHeader.text)

openNotesAppButton = Button(spacer, (userNameHeaderSize[1] + 35), 175, 75, RED, 'Notes', parentApp='homeLoggedIn')

openCalculatorButton = Button((openNotesAppButton.rect.right + spacer), (openNotesAppButton.rect.y), (openNotesAppButton.rect.width), (openNotesAppButton.rect.height), BLUE, 'Calc.', parentApp='homeLoggedIn')

testAppButton = Button((openCalculatorButton.rect.right + spacer), (openNotesAppButton.rect.y), (openNotesAppButton.rect.width), (openNotesAppButton.rect.height), GREEN, 'Other', parentApp='homeLoggedIn')

openNotesSettingsButton = Button(0, 550, 250, 50, BLACK, 'settings', WHITE, parentApp='homeLoggedIn')

clock1 = Clock((openNotesSettingsButton.rect.right + 25), (openNotesSettingsButton.rect.y), 50, 0, RED)