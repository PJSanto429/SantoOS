import pygame as pg #?not needed?

#!-----local imports-----
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from user import *
from variables import *

#*------------------ not logged in stuff -------------------
topHeader = InputBox(0, 10, 50, 0, 'SantoOS', 'largeMagneto', False, parentApp='homeNotLoggedIn', inactiveColor=BLACK)
topHeader.rect.width = topHeader.textFont.size(topHeader.text)[0]
topHeader.rect.centerx = (screen_width / 2)

mainLogo = Button(0, (topHeader.rect.bottom + 100), 350, 350, parentApp='homeNotLoggedIn', picture='assets/mainIcon.png')
mainLogo.rect.centerx = screen_width / 2

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
userNameHeader = InputBox(0, 10, 50, 0, '', 'largeMagneto', False, inactiveColor=BLACK, parentApp='homeLoggedIn')