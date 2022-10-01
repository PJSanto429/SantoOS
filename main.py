#this is an operating system application built with Python and pygame
# By Peyton Santo
# date started - 9/2/22 (2/9/22 for non-Americans)
#*-------------built in imports----------------
import pygame as pg
#from textwrap import TextWrapper
#import sys
#from time import gmtime, strftime, localtime
#from random import randint
#from glob import glob
#!-----------local imports---------------------
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from loading import Loading
from user import currentUser
#from clock import Clock
from variables import *

from notesApp import *
from homeApp import *

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    #wrapper = TextWrapper(initial_indent="* ")
    
    #*--------------------------------------
    def check_click(mouse):
        for button in Button.instances:
            if allApps[button.parentApp]:
                button.check_click(mouse)
        #add other class instances here
            
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
            modal.update(screen)

        #! custom button/input box stuff that will be changed
        
        userNameHeader.text = currentUser.userName
        userNameHeader.rect.width = userNameHeader.textFont.size(userNameHeader.text)[0]
        userNameHeader.rect.centerx = (screen_width / 2)
        
        #!login modal
        if testing.active:
            testBar.text = 'loading...' if not testing.finished else 'done!'
        else:
            testBar.text = 'ready to load'
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
    
    testing = Loading(50, 300, 500, 50, 10)
    testBar = InputBox(50, 150, 50, 0, '', changeable=False)
    testButton = Button(50, 450, 300, 100, RED, 'start loading')
    def testButtonFunct():
        testing.activate()
        #print(testing.setTime)
        #testing.setTime = 0
        #print(testing.setTime)
        #print('------------------------------')
    testButton.onClickFunction = testButtonFunct
    
    #allApps['homeNotLoggedIn'] = False
    #allApps['none'] = True
    #allApps['notesMain'] = True
    #currentUser.loggedIn = True
    #currentUser.userName = 'pjsanto'

    while True:
        #ticks = pg.time.get_ticks()
        #print(ticks)
        allEvents = pg.event.get()
        for event in allEvents:
            keys = pg.key.get_pressed()
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                handleQuit()
            if event.type == pg.MOUSEBUTTONDOWN:
                check_click(mouse)
            if event.type == cowGifTimer:
                currentCowImage += 1 if currentCowImage < 20 else -20
                dancingCowGif.picture = pg.image.load(f'assets/dancingCow/frame_{currentCowImage}.gif').convert_alpha()
                dancingCowGif.picture = pg.transform.scale(dancingCowGif.picture, (dancingCowGif.rect.width, dancingCowGif.rect.width))
            if event.type == cursorTimer:
                for box in InputBox.instances:
                    box.showHideCursor()    
            
            handleEventListener(event)

        screen.fill(TEAL)
        mouse = pg.mouse.get_pos()

        drawEverything(screen)
        
        pg.display.flip()
        clock.tick(60)