#this is a post-it application built with Python and pygame
#*-------------built in imports----------------
import pygame as pg
from textwrap import TextWrapper
import sys
from time import gmtime, strftime, localtime
from random import randint
#!-----------local imports---------------------
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from user import currentUser
from variables import *

from notesApp import *
from homeApp import *

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    wrapper = TextWrapper(initial_indent="* ")
    #currentUser = None
    
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
            if allApps[box.parentApp]:
                box.update()
                box.draw(screen)
        #for modal in Modal.instances:
        #    modal.update(screen)
        loginModal.update(screen)
        #notLoggedInModal.update(screen)

        #! custom button/input box stuff that will be changed
        newNoteButton.text = 'new note' if currentUser.loggedIn else 'log in'
        statusBox.text = 'username here' if currentUser.loggedIn else 'no user'
        
        userNameHeader.text = currentUser.userName
        
        #!login modal
        #loginStatusBox.text = '' if not loginModal.active else loginStatusBox.text
        if not loginModal.active:
            loginStatusBox.text = ''
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

    #* timer that goes off every 150 miliseconds
    #fontTimer = pg.USEREVENT + 1
    #pg.time.set_timer(fontTimer, 150)

    while True:
        allEvents = pg.event.get()
        for event in allEvents:
            keys = pg.key.get_pressed()
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                handleQuit()
            if event.type == pg.MOUSEBUTTONDOWN:
                check_click(mouse)
            handleEventListener(event)

        screen.fill(DARKGREY) #* sets the screen a certain color
        mouse = pg.mouse.get_pos() #* gets the position of the mouse

        drawEverything(screen)
        
        pg.display.flip()
        clock.tick(60)