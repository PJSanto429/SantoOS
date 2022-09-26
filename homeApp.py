import pygame as pg #?not needed?
from glob import glob

#!-----local imports-----
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from clock import Clock
from randomFuncts import handleQuit
from user import *
from variables import *

#*------------------ not logged in stuff -------------------
topHeader = InputBox(0, 10, 50, 0, 'SantoOS', 'extraLargeMagneto', False, parentApp='homeNotLoggedIn', inactiveColor=BLACK, center=True)
#topHeader.rect.width = topHeader.textFont.size(topHeader.text)[0]
#topHeader.rect.centerx = (screen_width / 2)

powerOffButton = Button(0, 0, 120, 120, parentApp='homeNotLoggedIn', picture='assets/powerOffLogo.png')
powerOffButton.rect.right = screen_width
def powerOffButtonFunct():
    handleQuit()
powerOffButton.onClickFunction = powerOffButtonFunct

mainLogo = Button(0, (topHeader.rect.bottom + 100), 350, 350, parentApp='homeNotLoggedIn', picture='assets/mainIcon.png') # 
mainLogo.rect.centerx = screen_width / 2
def mainLogoButtonFunct():
    pass
mainLogo.onClickFunction = mainLogoButtonFunct

currentCowImage = 1
dancingCowGif = Button(0, 0, 120, 120, picture='assets/dancingCow/frame_0.gif', parentApp='homeNotLoggedIn')

clock1 = Clock(15, (mainLogo.rect.bottom + 15), GREEN, parentApp='homeNotLoggedIn')
clock1.rect.width = clock1.textFont.size(clock1.text)[0]
clock1.rect.centerx = (screen_width / 2)

openLoginButton = Button((screen_width/4), (screen_width - (screen_height/8)), (screen_width/2), (screen_height/8), color = BLUE, textColor = WHITE, text = 'login', parentApp='homeNotLoggedIn')
def openLoginFunct():
    loginModal.active = True if not loginModal.active else False
openLoginButton.onClickFunction = openLoginFunct

#* --------------- logged in stuff ---------------------
spacer = 18.75
userNameHeader = InputBox(0, 0, 50, 0, '', 'extraLargeHPSimplified', False, inactiveColor=BLACK, parentApp='homeLoggedIn')
userNameHeaderSize = userNameHeader.textFont.size(userNameHeader.text)

openNotesAppButton = Button(spacer, (userNameHeaderSize[1] + 35), 175, 75, RED, 'Notes', parentApp='homeLoggedIn')
def openNotesButtonFunct():
    allApps['homeLoggedIn'] = False
    allApps['notesMain'] = True
openNotesAppButton.onClickFunction = openNotesButtonFunct

openCalculatorButton = Button((openNotesAppButton.rect.right + spacer), (openNotesAppButton.rect.y), (openNotesAppButton.rect.width), (openNotesAppButton.rect.height), BLUE, 'Calc.', parentApp='homeLoggedIn')

testAppButton = Button((openCalculatorButton.rect.right + spacer), (openNotesAppButton.rect.y), (openNotesAppButton.rect.width), (openNotesAppButton.rect.height), GREEN, 'Other', parentApp='homeLoggedIn')

openAllSettingsButton = Button(0, 0, 125, 125, BLACK, '', WHITE, parentApp='homeLoggedIn', picture='assets/settingsLogo2.png')
openAllSettingsButton.rect.bottom = screen_height

logoutButton = Button(0, 0, 250, 50, RED, 'Logout', parentApp='homeLoggedIn')
logoutButton.rect.width = (logoutButton.textFont.size(logoutButton.text)[0]) + 50
logoutButton.rect.bottom = screen_height
logoutButton.rect.right = screen_width
def logoutButtonFunc():
    currentUser.logoutUser()
logoutButton.onClickFunction = logoutButtonFunc