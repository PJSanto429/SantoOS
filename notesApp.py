import pygame as pg

#!-----local imports-----
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from user import *
from variables import *
from randomFuncts import *

#*------------------ notes stuff --------
quitButton = Button(0, 0, (screen_width/2), (screen_height/8), text = 'quit', textFont = 'largeConsolas', parentApp='notes')
def quitButtonFunct():
    handleQuit()
quitButton.onClickFunction = quitButtonFunct

newNoteButton = Button((screen_width/2), 0, (screen_width/2), (screen_height/8), color = BLUE, textColor = WHITE, text = 'new note', parentApp='notes')
def newNoteFunct():
    print('new note button')
    #loginModal.active = True if not loginModal.active else False
    #currentUser.loginUser('pjsanto', '')
newNoteButton.onClickFunction = newNoteFunct

#* text boxes
statusBox = InputBox(0, (quitButton.rect.height), screen_width, 50, '', changeable = False, parentApp='notes')
statusBox.static = True

bottomStatusBox = statusBox

inputBox1 = InputBox(25, (bottomStatusBox.rect.bottom), (screen_width - 50), 400, 'ok', parentApp='notes')
#testWords = 'wow this is cool \n ok i pull up'
#inputBox2 = InputBox(25, -250, (screen_width - 50), 100, testWords) #(inputBox1.rect.bottom)

saveButton = Button(0, (inputBox1.rect.bottom + 5), (screen_width/2), (screen_height/8), color = GREEN, text = 'save note', textFont = 'largeOldEnglishText', parentApp='notes')
def saveButtonFunct():
    print('save button')
saveButton.onClickFunction = saveButtonFunct

cancelButton = Button((saveButton.rect.right), (inputBox1.rect.bottom + 5), (screen_width/2), (screen_height/8), color = RED, text = 'Cancel', parentApp='notes')
def cancelButtonFunct():
    inputBox1.text = ''
    #print(inputBox1.textFont.size)
    #inputBox1.textFont = allFonts['mediumConsolas']
cancelButton.onClickFunction = cancelButtonFunct