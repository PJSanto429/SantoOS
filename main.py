#this is an operating system application built with Python and pygame
# By Peyton Santo
# date started - 9/2/22 (2/9/22 for non-Americans)
#*-------------built in imports----------------
import pygame as pg
from random import randint
#!-----------local imports---------------------
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from loading import Loading
from toggle import Toggle
from user import currentUser
from slider import Slider
from clock import Clock
from firstStartup import firstStartUp
from graphics import *
from variables import *
#?------- apps --------------------
from APPnotes import *
from APPhome import *
from APPcalculator import *
from APPgameTest import *
from APPpaint import *
from APPpong import *
from APPsnake import *
from APPdodger import *
from APPbreakout import *
from APPrps import *
from APPflappy import *
from APPsharks import *
from APPFlight import *

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    firstStartUp()
    
    #*--------------------------------------
    def checkClick(mouse):
        for button in Button.instances:
            if allApps[button.parentApp]:
                button.check_click(mouse, Modal.instances)
                
        for toggle in Toggle.instances:
            if allApps[toggle.parentApp]:
                toggle.checkClick(mouse, Modal.instances)

    def drawEverything(screen):
        for button in Button.instances:
            if not button.parent and allApps[button.parentApp]:
                button.draw_button(screen)
                
        for box in InputBox.instances:
            if not box.parent and allApps[box.parentApp]:
                box.update()
                box.draw(screen)
            
        for loader in Loading.instances:
            if not loader.parent and allApps[loader.parentApp]:
                loader.update(screen)   
                
        for toggle in Toggle.instances:
            if not toggle.parent and allApps[toggle.parentApp]:
                toggle.draw(screen)
                
        for slider in Slider.instances:
            if not slider.parent and allApps[slider.parentApp]:
                slider.update(screen)

        for modal in Modal.instances:
            if allApps[modal.parentApp]:
                modal.update(screen)
            else:
                modal.active = False

        #! custom button/input box stuff that will be changed
        userNameHeader.text = currentUser.userName
        userNameHeader.rect.width = userNameHeader.textFont.size(userNameHeader.text)[0]
        userNameHeader.rect.centerx = (screen_width / 2)
        
        if not currentUser.currentNoteSaved:
            notesEditStatusbar.text = 'ready to save'
        
        #!login modal
        if not loginModal.active and not newUserModal.active:
            loginStatusBox.text = ''
            loginStatusMessageBox.text = ''
            userNameInput.text = 'username'
            passwordInput.text = 'password'
            userNameInput.edited = passwordInput.edited = False

    def handleEventListener(event):
        for box in InputBox.instances:
            modalsActive = False
            for modal in Modal.instances:
                if modal.active:
                    modalsActive = True
            
            parentActive = False
            if box.parent:
                if box.parent.active:
                    parentActive = True
            
            if not modalsActive or parentActive:
                box.handle_event(event)

    #!----timers-----
    cowGifTimer = pg.USEREVENT + 1
    pg.time.set_timer(cowGifTimer, 100) #* 100 miliseconds
    
    cursorTimer = pg.USEREVENT + 2
    pg.time.set_timer(cursorTimer, 500) #* 500 miliseconds
    
    #!---------------------------------------------
    
    # ? ------------------------------------------------------------------------
    # allApps['homeLoading'] = False
    # # allApps['homeNotLoggedIn'] = True
    # # allApps['homeLoggedIn'] = True
    # # allApps['none'] = True

    # # crt.active = False
    
    # # simpleGame.running = allApps['testGameMain'] = True
    # # pongGame.running = allApps['pongMain'] = True
    # # mainPaint.running = allApps['paintMain'] = True
    # # snakeGame.running = allApps['snakeGameMain'] = True
    # # dodgerGame.running = allApps['dodgerGameMain'] = True
    # # breakoutGame.running = allApps['breakoutMain'] = True
    # # rockPaperScissors.running = allApps['rpsMain'] = True 
    # # flappyGame.running = allApps['flappyMain'] = True
    # # sharkGame.running = allApps['sharkGameMain'] = True
    # flightGame.running = allApps['flightGameMain'] = True
    
    # currentUser.loggedIn = True
    # currentUser.userName = 'pjsanto'
    
    # ? ---------------- Test stuff on 'allApps['none'] ---------------------------------
    testInput = InputBox(0, 10, 600, 50, 'Not Active', changeable=False, inactiveColor=BLACK, showRect=False, center=True)

    testToggle = Toggle(250, 50, 100, 50, text='test toggle', textLocation='bottom')
    def testToggleFunct():
        testInput.text = 'Active' if testToggle.on else 'Not Active'
    testToggle.onChangeEvent = testToggleFunct
    testToggleRect = testToggle.rect
    
    # testSlider = Slider(20, (testToggleRect.bottom  + 125), (screen_width - 100), 50, title=['slider here', 'top'], showValue=[True, 'bottom'], maxVal=255, handleColor=GREY)
    
    # inputTest = InputBox(50, 100, 200, 50, largeFonts[0], largeFonts[0], False, parentApp='testBed', showRect=False,inactiveColor=BLACK)
    # buttonTest = Button(50, 250, 50, 50, RED, '0', parentApp='testBed')
    # def buttonFunct():
    #     fontNum = int(buttonTest.text)
    #     if fontNum + 1 == len(largeFonts):
    #         fontNum = 0
    #     else:
    #         fontNum += 1
    #     buttonTest.text = str(fontNum)
    #     inputTest.text = largeFonts[fontNum]
    #     inputTest.textFont = allFonts[largeFonts[fontNum]]
    # buttonTest.onClickFunction = buttonFunct
    
    #? ------------------------------------------------------------------------

    while True:
        mouse = pg.mouse.get_pos()
        allEvents = pg.event.get()
        keys = pg.key.get_pressed()
        for event in allEvents:
            if event.type == pg.QUIT or (keys[pg.K_LCTRL] and keys[pg.K_c]):
                handleQuit()
            if checkMouseClick(event)[0]:
                checkClick(mouse)
            if event.type == pg.KEYDOWN and keys[pg.K_LCTRL] and keys[pg.K_F1]:
                crt.activateDeactivate()
            #!----timer events----
            if event.type == cowGifTimer:
                currentCowImage += 1 if currentCowImage < 20 else -20
                dancingCowGif.picture = pg.image.load(f'assets/dancingCow/frame_{currentCowImage}.gif').convert_alpha()
                dancingCowGif.picture = pg.transform.scale(dancingCowGif.picture, (dancingCowGif.rect.width, dancingCowGif.rect.width))
            if event.type == cursorTimer:
                for box in InputBox.instances:
                    box.showHideCursor()
            #!input box stuff
            handleEventListener(event)
            #! slider stuff
            for slider in Slider.instances:
                if allApps[slider.parentApp]:
                    slider.moveHandle(mouse)
            
        simpleGame.run()
        mainPaint.run()
        pongGame.run()
        snakeGame.run()
        dodgerGame.run()
        breakoutGame.run()
        rockPaperScissors.run()
        flappyGame.run()
        sharkGame.run()
        flightGame.run()
        
        if not any([
            simpleGame.running,
            mainPaint.running,
            pongGame.running,
            snakeGame.running,
            dodgerGame.running,
            breakoutGame.running,
            rockPaperScissors.running,
            flappyGame.running,
            sharkGame.running,
            flightGame.running,
        ]):
            screen.fill(TEAL)

        drawEverything(screen)
        crt.draw()
        
        pg.display.flip()
        clock.tick(tickSpeed) if not mainPaint.running else clock.tick(mainPaint.tickSpeed)