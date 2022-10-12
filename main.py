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
from clock import Clock
from graphics import *
from variables import *
#?------- apps --------------------
from APPnotes import *
from APPhome import *
from APPcalculator import *

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    
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
            if not button.parent and allApps[box.parentApp]:
                box.update()
                box.draw(screen)
            
        for loader in Loading.instances:
            if not loader.parent and allApps[loader.parentApp]:
                loader.update(screen)   

        for modal in Modal.instances:
            if allApps[modal.parentApp]:
                modal.update(screen)
            else:
                modal.active = False
                
        for toggle in Toggle.instances:
            if not toggle.parent and allApps[toggle.parentApp]:
                toggle.draw(screen)

        #! custom button/input box stuff that will be changed
        userNameHeader.text = currentUser.userName
        userNameHeader.rect.width = userNameHeader.textFont.size(userNameHeader.text)[0]
        userNameHeader.rect.centerx = (screen_width / 2)
        
        print(openCalculatorButton.rect.collidepoint(mouse))
        
        testInput.text = 'Active' if testToggle.on else 'Not Active'

        if not currentUser.currentNoteSaved:
            notesEditStatusbar.text = 'ready to save'
        
        #!login modal
        if not loginModal.active and not newUserModal.active:
            loginStatusBox.text = ''
            loginStatusMessageBox.text = ''
            userNameInput.text = 'username'
            passwordInput.text = 'password'
            userNameInput.edited = passwordInput.edited = False

    def handleEventListener(event, keys):
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
                box.handle_event(event, keys)

    #!----timers-----
    cowGifTimer = pg.USEREVENT + 1
    pg.time.set_timer(cowGifTimer, 100) #* 100 miliseconds
    
    cursorTimer = pg.USEREVENT + 2
    pg.time.set_timer(cursorTimer, 500) #* 500 miliseconds
    
    #allApps['homeLoading'] = False
    #allApps['calculatorMain'] = True
    ##allApps['none'] = True
    #currentUser.loggedIn = True
    #currentUser.userName = 'pjsanto' 
    
    testToggle = Toggle(250, 250, 100, 50)
    testInput = InputBox(0, 100, 600, 50, '', changeable=False, inactiveColor=BLACK, showRect=False, center=True)

    while True:
        #ticks = pg.time.get_ticks()
        allEvents = pg.event.get()
        keys = pg.key.get_pressed()
        for event in allEvents:
            if event.type == pg.QUIT:# or keys[pg.K_ESCAPE]:
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
            handleEventListener(event, keys)

        screen.fill(TEAL)
        mouse = pg.mouse.get_pos()

        drawEverything(screen)
        crt.draw()
        
        pg.display.flip()
        clock.tick(60)