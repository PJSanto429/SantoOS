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
from user import User
from variables import *

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    screen_width = 600
    screen_height = 600
    wrapper = TextWrapper(initial_indent="* ")
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption('notes app')
    #!pg.display.set_icon(pg.image.load('assets/icon3.png'))
    clock = pg.time.Clock()
    currentUser = None
    
    #*--------------------------------------
    def check_click(mouse):
        for button in Button.instances:
            button.check_click(mouse)
        #add other class instances here
            
    def drawEverything(screen):
        for button in Button.instances:
            if not button.parent:
                button.draw_button(screen)
        for box in InputBox.instances:
            box.update()
            box.draw(screen)
        loginModal.update(screen)

        #! custom button/input box stuff that will be changed
        newNoteButton.text = 'new note' if currentUser.loggedIn else 'log in'
        statusBox.text = 'username here' if currentUser.loggedIn else 'no user'
        
        #!login modal
        loginStatusBox.text = '' if not loginModal.active else loginStatusBox.text
        userNameInput.text = 'username' if not loginModal.active else userNameInput.text
        passwordInput.text = 'password' if not loginModal.active else passwordInput.text

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
            
    def handleQuit():
        #save and encrypt current note before quitting
        pg.quit()
        sys.exit()
            
    #user
    currentUser = User()
    #*------------------login modal -------------------------
    loginModal = Modal(100, 100, 400, 400, 'log in')
    userNameInput = InputBox(loginModal.rect.left, (loginModal.rect.top + 75), (loginModal.rect.width), 50, 'username', parent = loginModal)
    passwordInput = InputBox((loginModal.rect.left), (userNameInput.rect.bottom + 25), (loginModal.rect.width), 50, 'password', parent = loginModal)
    
    cancelLoginButton = Button((loginModal.rect.left), (loginModal.rect.bottom - 25), (loginModal.rect.width / 2), 50, RED, 'Cancel', parent = loginModal)
    def cancelLoginButtonFunct():
        userNameInput.text = ''
        passwordInput.text = ''
        loginModal.active = False
    cancelLoginButton.onClickFunction = cancelLoginButtonFunct
    
    loginButton = Button((cancelLoginButton.rect.right), (cancelLoginButton.rect.y), cancelLoginButton.rect.width, cancelLoginButton.rect.height, GREEN, 'Login', parent = loginModal)
    def loginButtonFunct():
        loggedIn, status = currentUser.loginUser(userNameInput.text, passwordInput.text)
        print(f'logged in == {loggedIn}')
        print(f'status == {status}')
        currentUser.loggedIn = loggedIn
        if currentUser.loggedIn:
            loginStatusBox.text = 'user logged in'
            #print('user logged in')
        else:
            loginStatusBox.text = 'login failed'
            #print('login failed')
    loginButton.onClickFunction = loginButtonFunct
    
    loginStatusBox = InputBox((loginModal.rect.left + 15), (passwordInput.rect.bottom + 25), (loginModal.rect.width - 30), 50, changeable=False, parent=loginModal)
    #* ------------------------------------------------------------------------
    
    #* all buttons        
    quitButton = Button(0, 0, (screen_width/2), (screen_height/8), text = 'quit', textFont = 'largeConsolas')
    def quitButtonFunct():
        handleQuit()
    quitButton.onClickFunction = quitButtonFunct
    
    newNoteButton = Button((screen_width/2), 0, (screen_width/2), (screen_height/8), color = BLUE, textColor = WHITE, text = 'new note')
    def newNoteFunct():
        #print('new note')
        #Button.user = 'user' if not Button.user else None
        loginModal.active = True if not loginModal.active else False
        #currentUser.loginUser('pjsanto', '')
    newNoteButton.onClickFunction = newNoteFunct
    
    #* text boxes
    statusBox = InputBox(0, (quitButton.rect.height), screen_width, 50, '', changeable = False)
    statusBox.static = True
    
    bottomStatusBox = statusBox
    
    inputBox1 = InputBox(25, (bottomStatusBox.rect.bottom), (screen_width - 50), 400, 'ok')
    #testWords = 'wow this is cool \n ok i pull up'
    #inputBox2 = InputBox(25, -250, (screen_width - 50), 100, testWords) #(inputBox1.rect.bottom)
    
    saveButton = Button(0, (inputBox1.rect.bottom + 5), (screen_width/2), (screen_height/8), color = GREEN, text = 'save note', textFont = 'largeOldEnglishText')
    def saveButtonFunct():
        print('save button')
    saveButton.onClickFunction = saveButtonFunct
    
    cancelButton = Button((saveButton.rect.right), (inputBox1.rect.bottom + 5), (screen_width/2), (screen_height/8), color = RED, text = 'Cancel')
    def cancelButtonFunct():
        inputBox1.text = ''
        #print(inputBox1.textFont.size)
        #inputBox1.textFont = allFonts['mediumConsolas']
    cancelButton.onClickFunction = cancelButtonFunct

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