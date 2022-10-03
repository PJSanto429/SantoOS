import pygame as pg #?not needed?
from glob import glob

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

#*------------------ loading ------------------------------
mainLoader = Loading(50, 300, 500, 50, 10, loadedColor=LIGHTTEAL, parentApp='homeLoading', loadingTitle='System Starting...')
startSystemButton = Button(0, 0, 300, 100, BLACK, 'Start System', textColor=WHITE, parentApp='homeLoading')
startSystemButton.rect.center = ((screen_width / 2), (screen_height / 2))
def startSystemButtonFunct():
    startSystemButton.parentApp = 'none'
    mainLoader.activate()
startSystemButton.onClickFunction = startSystemButtonFunct

def mainLoaderDoneFunct():
    allApps['homeLoading'] = False
    allApps['homeNotLoggedIn'] = True
mainLoader.doneLoadingFunct = mainLoaderDoneFunct

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

openCreateUserButton = Button(0, (screen_height - (screen_height/8)), (screen_width/2), (screen_height/8), color=GREEN, text='create user', parentApp='homeNotLoggedIn')
openCreateRect = openCreateUserButton.rect
def openCreateUserFunct():
    loginModal.active = False
    newUserModal.active = True if not newUserModal.active else False
    #!changing parents and text
    loginStatusMessageBox.parent = loginStatusBox.parent = cancelLoginButton.parent = loginButton.parent = userNameInput.parent = passwordInput.parent = newUserModal
    loginStatusMessageBox.inactiveColor = loginStatusBox.inactiveColor = userNameInput.inactiveColor = passwordInput.inactiveColor = WHITE
    loginButton.text = 'Create'
openCreateUserButton.onClickFunction = openCreateUserFunct

openLoginButton = Button((openCreateRect.right), (openCreateRect.y), (openCreateRect.width), (openCreateRect.height), color = BLUE, textColor = WHITE, text = 'login', parentApp='homeNotLoggedIn')
def openLoginFunct():
    newUserModal.active = False
    loginModal.active = True if not loginModal.active else False
    #!changing parents and text
    loginStatusMessageBox.parent = loginStatusBox.parent = cancelLoginButton.parent = loginButton.parent = userNameInput.parent = passwordInput.parent = loginModal
    loginStatusMessageBox.inactiveColor = loginStatusBox.inactiveColor = userNameInput.inactiveColor = passwordInput.inactiveColor = LIGHTGREY
    loginButton.text = 'Login'
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