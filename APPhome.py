import pygame as pg #?not needed?

#!-----local imports-----
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from toggle import Toggle
from clock import Clock
from loading import Loading
from randomFuncts import handleQuit
#* -------- apps ----------
from APPgameTest import simpleGame
from APPpaint import mainPaint
from APPpong import pongGame
from APPsnake import *
from APPdodger import *
from APPbreakout import *
# from APPrps import rockPaperScissors
#*----------------------
from user import *
from variables import *

#*------------------ loading ------------------------------
mainLoader = Loading(50, 300, 500, 50, 10, loadedColor=GREEN, parentApp='homeLoading', loadingTitle='System Starting...')
mainStartToggle = Toggle(225, 400, parentApp='homeLoading', text='start system', textLocation='bottom')
def mainStartFunct():
    mainStartToggle.text = 'Cancel' if mainStartToggle.on else 'Start System'
    mainLoader.activate() if not mainLoader.active else mainLoader.deactivate()
mainStartToggle.onChangeEvent = mainStartFunct

def mainLoaderDoneFunct():
    allApps['homeLoading'] = False
    allApps['homeNotLoggedIn'] = True
mainLoader.doneLoadingFunct = mainLoaderDoneFunct

#*------------------ not logged in stuff -------------------
topHeader = InputBox(0, 10, 50, 0, 'SantoOS', 'extraLargeMagneto', False, parentApp='homeNotLoggedIn', inactiveColor=BLACK, center=True)

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
openNotesAppRect = openNotesAppButton.rect
def openNotesButtonFunct():
    allApps['homeLoggedIn'] = False
    allApps['notesMain'] = True
openNotesAppButton.onClickFunction = openNotesButtonFunct

openCalculatorButton = Button((openNotesAppButton.rect.right + spacer), (openNotesAppButton.rect.y), (openNotesAppButton.rect.width), (openNotesAppButton.rect.height), BLUE, 'Calc.', parentApp='homeLoggedIn')
# openCalculatorButton.showOutline = True
def openCalculatorFunct():
    allApps['homeLoggedIn'] = False
    allApps['calculatorMain'] = True
openCalculatorButton.onClickFunction = openCalculatorFunct

openGameButton = Button((openCalculatorButton.rect.right + spacer), (openNotesAppButton.rect.y), (openNotesAppButton.rect.width), (openNotesAppButton.rect.height), GREEN, 'Game Test', parentApp='homeLoggedIn')
def openGameFunct():
    allApps['homeLoggedIn'] = False
    allApps['testGameMain'] = True
    simpleGame.running = True
openGameButton.onClickFunction = openGameFunct

openPaintButton = Button(openNotesAppRect.x, (openNotesAppRect.bottom + spacer), openNotesAppRect.width, openNotesAppRect.height, PURPLE, 'Paint', parentApp='homeLoggedIn')
openPaintRect = openPaintButton.rect
def openPaintFunct():
    allApps['homeLoggedIn'] = False
    allApps['paintMain'] = True
    mainPaint.running = True
    mainPaint.delayTime = pg.time.get_ticks()
openPaintButton.onClickFunction = openPaintFunct

openPongButton = Button((openPaintRect.right + spacer), openPaintRect.y, openPaintRect.width, openPaintRect.height, BLACK, 'Pong', textColor=WHITE, parentApp='homeLoggedIn')
openPongrect = openPongButton.rect
def openPongFunct():
    allApps['homeLoggedIn'] = False
    allApps['pongMain'] = True
    pongGame.running = True
openPongButton.onClickFunction = openPongFunct

openSnakeGameButton = Button((openPongrect.right + spacer), openPongrect.y, openPongrect.width, openPongrect.height, PINK, 'Snake', textColor=BLACK, parentApp='homeLoggedIn')
def openSnakeGameFunct():
    allApps['homeLoggedIn'] = False
    allApps['snakeGameMain'] = True
    snakeGame.running = True
    snakeGame.paused = True
    snakeHomeButton.parentApp = snakeStatusBox.parentApp = 'snakeGameMain'
    snakeStatusBox.text = 'Press Space to Start'
openSnakeGameButton.onClickFunction = openSnakeGameFunct

openDodgerButton = Button(openPaintRect.x, (openPaintRect.bottom + spacer), openPaintRect.width, openPaintRect.height, GREY, 'FarSpace', parentApp='homeLoggedIn')
openDodgerRect = openDodgerButton.rect
openDodgerButton.textFont = allFonts['mediumConsolas']
def openDodgeFunct():
    dodgerGame.running = True
    allApps['homeLoggedIn'] = False
    allApps['dodgerGameMain'] = True
openDodgerButton.onClickFunction = openDodgeFunct

openBreakoutButton = Button(openPongrect.x, openDodgerRect.y, openPaintRect.width, openPaintRect.height, ORANGE, 'Breakout', parentApp='homeLoggedIn')
openBreakoutRect = openBreakoutButton.rect
openBreakoutButton.textFont = allFonts['mediumConsolas']
def openBreakoutFunct():
    breakoutGame.running = True
    allApps['homeLoggedIn'] = False
    allApps['breakoutMain'] = True
openBreakoutButton.onClickFunction = openBreakoutFunct

# openRPSbutton = Button((openBreakoutRect.right + spacer), openDodgerRect.y, openPaintRect.width, openPaintRect.height, DARKRED, 'RPS', parentApp='homeLoggedIn')
# def openRPSfunct():
#     rockPaperScissors.running = True
#     rockPaperScissors.createGame()
#     allApps['homeLoggedIn'] = False
#     allApps['rpsMain'] = True
# openRPSbutton.onClickFunction = openRPSfunct

openAllSettingsButton = Button(0, 0, 125, 125, BLACK, '', WHITE, parentApp='none', picture='assets/settingsLogo2.png')
openAllSettingsButton.rect.bottom = screen_height

logoutButton = Button(0, 0, 250, 50, RED, 'Logout', parentApp='homeLoggedIn')
logoutButton.rect.width = (logoutButton.textFont.size(logoutButton.text)[0]) + 50
logoutButton.rect.bottom = screen_height
logoutButton.rect.right = screen_width
def logoutButtonFunc():
    currentUser.logoutUser()
logoutButton.onClickFunction = logoutButtonFunc