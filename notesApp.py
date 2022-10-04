import pygame as pg

#!-----local imports-----
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from clock import Clock
from loading import Loading
from user import *
from variables import *
from randomFuncts import *

#*------------------ notes main --------
notesMainHeader = InputBox(0, 15, 50, 0, 'Notes', textFont='extraLargeConsolas', changeable=False, inactiveColor=BLACK, parentApp='notesMain', center=True)
headerTextSize = notesMainHeader.textFont.size(notesMainHeader.text)

clock2 = Clock(0, 0, parentApp='notesMain', center=True)
clock2TextSize = clock2.textFont.size(clock2.text)
clock2.rect.bottom = (screen_height - (clock2TextSize[1] + 20))

newNoteButton = Button(0, (headerTextSize[1] + 35), (screen_width), (screen_height/6), color = GREEN, text='New Note', parentApp='notesMain')
def newNoteFunct():
    allApps['notesMain'] = False
    allApps['notesEdit'] = True
newNoteButton.onClickFunction = newNoteFunct

openViewModal = Modal(0, 0, 300, 200, 'Choose Note', WHITE, backgroundColor=MAROON, parentApp='notesMain')
openViewModal.rect.center = ((screen_width / 2), (screen_height / 2))
openViewRect = openViewModal.rect

chooseNoteInput = InputBox((openViewRect.x), (openViewRect.top + openViewModal.textRect.height + 15), (openViewRect.width), 100, 'note title', activeColor=GREEN, allowWrap=True, parentApp='notesMain', parent=openViewModal)

cancelChooseNoteButton = Button(openViewRect.x, 0, (openViewRect.width / 2), 50, RED, 'Cancel', parent=openViewModal, parentApp='notesMain')
def cancelChooseNoteFunct():
    openViewModal.active = False
cancelChooseNoteButton.onClickFunction = cancelChooseNoteFunct
cancelChooseRect = cancelChooseNoteButton.rect

submitChooseNoteButton = Button(cancelChooseRect.right, 0, cancelChooseRect.width, cancelChooseRect.height, GREEN, 'Open', parent=openViewModal, parentApp='notesMain')
def submitChooseNoteFunct():
    print('choose note input ==>', chooseNoteInput.text)
submitChooseNoteButton.onClickFunction = submitChooseNoteFunct
submitChooseNoteButton.rect.bottom = cancelChooseNoteButton.rect.bottom = openViewRect.bottom

openViewButton = Button(0, 0, (screen_width), (screen_height/6), color=BLUE, text='View Note', parentApp='notesMain')
def openViewButtonFunct():
    openViewModal.active = True if not openViewModal.active else False
    
openViewButton.onClickFunction = openViewButtonFunct
openViewButton.rect.centery = screen_height / 2

openNoteSettingsButton = Button(0, (openViewButton.rect.bottom + 35), (screen_width/2), (screen_height/6), color=VERYDARKGREY, text='Note Settings', textColor=WHITE, parentApp='notesMain')
openNoteSettingsButton.rect.bottom = (clock2.rect.bottom - 20)
def openNoteSettingsButtonFunct():
    print('open notes settings')
openNoteSettingsButton.onClickFunction = openNoteSettingsButtonFunct

goToNotesHomeButton = Button((openNoteSettingsButton.rect.right), (openNoteSettingsButton.rect.y), (screen_width/2), (screen_height/6), color=RED, text='Home', parentApp='notesMain')
def goToNotesHomeButtonFunct():
    openViewModal.active = False
    allApps['notesMain'] = False
    allApps['homeLoggedIn'] = True
goToNotesHomeButton.onClickFunction = goToNotesHomeButtonFunct

#*------------------ edit/create note ----------
noteData = currentUser.getNoteInfo()
notesTitleInput = InputBox(25, 5, (screen_width - 50), 50, noteData[0], parentApp='notesEdit', )

mainNotesInput = InputBox(25, (notesTitleInput.rect.bottom + 15), (screen_width - 50), 400, noteData[1], parentApp='notesEdit', allowWrap=True)

notesDoneButton = Button(0, (mainNotesInput.rect.bottom + 5), (screen_width/2), (screen_height/8), color = BLUE, text = 'Done', parentApp='notesEdit')
doneRect = notesDoneButton.rect
def notesDoneButtonFunct():
    if not currentUser.currentNoteSaved:
        askSaveNoteModal.active = True if not askSaveNoteModal.active else False
    else:
        allApps['notesEdit'] = False
        allApps['notesMain'] = True
notesDoneButton.onClickFunction = notesDoneButtonFunct

saveNoteButton = Button(doneRect.right, (mainNotesInput.rect.bottom + 5), (screen_width/2), (screen_height/8), color = GREEN, text = 'Save Note', parentApp='notesEdit')
def saveNoteButtonFunct():
    #save the note here
    #print('hit save button')
    success = currentUser.createSaveHandler(notesTitleInput.text, mainNotesInput.text)
    print(success)
    #currentUser.currentNote = None
    #print('save button')
saveNoteButton.onClickFunction = saveNoteButtonFunct

notesDoneButton.rect.bottom = saveNoteButton.rect.bottom = screen_height

askSaveNoteModal = Modal((screen_width/4), 100, 300, 150, 'Save note?', backgroundColor=FUCHSIA, parentApp='notesEdit')
askSaveNoteModal.rect.centerx = screen_width/2
askSaveNoteModal.rect.centery = screen_height/2

askRect = askSaveNoteModal.rect

yesSaveNoteButton = Button((askRect.left), (askRect.bottom - 50), (askRect.width / 2), 50, GREEN, 'Yes', parent=askSaveNoteModal, parentApp='notesEdit')
yesSaveRect = yesSaveNoteButton.rect
def yesSaveNoteFunct():
    currentUser.createSaveHandler(notesTitleInput.text, mainNotesInput.text)
yesSaveNoteButton.onClickFunction = yesSaveNoteFunct

dontSaveNoteButton = Button((yesSaveRect.right), (yesSaveRect.y), (yesSaveRect.width), (yesSaveRect.height), RED, 'No', parent=askSaveNoteModal, parentApp='notesEdit')

notesEditStatusbar = InputBox(15, (mainNotesInput.rect.bottom + 10), (screen_width - 30), 0, '', inactiveColor=WHITE, changeable=False, parentApp='notesEdit')
