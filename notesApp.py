from re import L
import pygame as pg

#!-----local imports-----
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from clock import Clock
from user import *
from variables import *
from randomFuncts import *

#*------------------ notes main --------
notesMainHeader = InputBox(0, 15, 50, 0, 'Notes', textFont='extraLargeConsolas', changeable=False, inactiveColor=BLACK, parentApp='notesMain')
headerTextSize = notesMainHeader.textFont.size(notesMainHeader.text)
notesMainHeader.rect.width = headerTextSize[0]
notesMainHeader.rect.centerx = screen_width/2

clock2 = Clock(0, 0, parentApp='notesMain')
clock2TextSize = clock2.textFont.size(clock2.text)
clock2.rect.bottom = (screen_height - (clock2TextSize[1] + 20))
clock2.rect.width = clock2TextSize[0]
clock2.rect.centerx = screen_width/2

newNoteButton = Button(0, (headerTextSize[1] + 35), (screen_width), (screen_height/6), color = GREEN, text='New Note', parentApp='notesMain')
def newNoteFunct():
    allApps['notesMain'] = False
    allApps['notesNew'] = True
newNoteButton.onClickFunction = newNoteFunct

allNotesButton = Button(0, 0, (screen_width), (screen_height/6), color=BLUE, text='All Notes', parentApp='notesMain')
def allNotesButtonFunct():
    print('goto all notes')
allNotesButton.onClickFunction = allNotesButtonFunct
allNotesButton.rect.centery = screen_height / 2

openNoteSettingsButton = Button(0, (allNotesButton.rect.bottom + 35), (screen_width/2), (screen_height/6), color=VERYDARKGREY, text='Note Settings', textColor=WHITE, parentApp='notesMain')
openNoteSettingsButton.rect.bottom = (clock2.rect.bottom - 20)
def openNoteSettingsButtonFunct():
    print('open notes settings')
openNoteSettingsButton.onClickFunction = openNoteSettingsButtonFunct

goToNotesHomeButton = Button((openNoteSettingsButton.rect.right), (openNoteSettingsButton.rect.y), (screen_width/2), (screen_height/6), color=RED, text='Home', parentApp='notesMain')
def goToNotesHomeButtonFunct():
    allApps['notesMain'] = False
    allApps['homeLoggedIn'] = True
goToNotesHomeButton.onClickFunction = goToNotesHomeButtonFunct

#*------------------ new note ----------
#quitButton = Button(0, 0, (screen_width/2), (screen_height/8), text = 'quit', textFont = 'largeConsolas', parentApp='notesNew')
#def quitButtonFunct():
#    handleQuit()
#quitButton.onClickFunction = quitButtonFunct

#* text boxes
notesStatusBox = InputBox(0, (screen_height/8), screen_width, 50, '', changeable = False, parentApp='notesNew')
#notesStatusBox.static = True

mainNotesInput = InputBox(25, (notesStatusBox.rect.bottom), (screen_width - 50), 400, 'ok', parentApp='notesNew')

notesDoneButton = Button(0, (mainNotesInput.rect.bottom + 5), (screen_width/2), (screen_height/8), color = BLUE, text = 'Done', parentApp='notesNew')
doneRect = notesDoneButton.rect
def notesDoneButtonFunct():
    #first check if the current note is saved
    askSaveNoteModal.active = True if not askSaveNoteModal.active else False
    #allApps['notesNew'] = False
    #allApps['notesMain'] = True
notesDoneButton.onClickFunction = notesDoneButtonFunct

saveNoteButton = Button(doneRect.right, (mainNotesInput.rect.bottom + 5), (screen_width/2), (screen_height/8), color = GREEN, text = 'save note', parentApp='notesNew')
def saveNoteButtonFunct():
    #save the note here
    print('save button')
saveNoteButton.onClickFunction = saveNoteButtonFunct

askSaveNoteModal = Modal((screen_width/4), 100, 300, 150, 'Save note?', backgroundColor=FUCHSIA, parentApp='notesNew')
askSaveNoteModal.rect.centerx = screen_width/2
askSaveNoteModal.rect.centery = screen_height/2

askRect = askSaveNoteModal.rect

yesSaveNoteButton = Button((askRect.left), (askRect.bottom - 50), (askRect.width / 2), 50, GREEN, 'Yes', parent=askSaveNoteModal, parentApp='notesNew')
yesSaveRect = yesSaveNoteButton.rect

dontSaveNoteButton = Button((yesSaveRect.right), (yesSaveRect.y), (yesSaveRect.width), (yesSaveRect.height), RED, 'No', parent=askSaveNoteModal, parentApp='notesNew')