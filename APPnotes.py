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

#*------------------ edit/create note ----------
noteData = currentUser.getNoteInfo()
notesTitleInput = InputBox(25, 5, (screen_width - 50), 50, noteData[0], parentApp='notesEdit')

mainNotesInput = InputBox(25, (notesTitleInput.rect.bottom + 15), (screen_width - 50), 400, noteData[1], parentApp='notesEdit', allowWrap=True)
def notesInputChange():
    currentUser.currentNoteSaved = False
notesTitleInput.onChange = mainNotesInput.onChange = notesInputChange

notesDoneButton = Button(0, (mainNotesInput.rect.bottom + 5), (screen_width/3), (screen_height/8), color = BLUE, text = 'Done', parentApp='notesEdit')
notesDoneButton.rect.bottom = screen_height
doneRect = notesDoneButton.rect
def notesDoneButtonFunct():
    if not currentUser.currentNoteSaved:
        askSaveNoteModal.active = True if not askSaveNoteModal.active else False
    else:
        allApps['notesEdit'] = False
        allApps['notesMain'] = True
notesDoneButton.onClickFunction = notesDoneButtonFunct

notesEditStatusbar = InputBox(15, (mainNotesInput.rect.bottom + 10), (screen_width - 30), 0, '', inactiveColor=WHITE, changeable=False, parentApp='notesEdit')

saveNoteButton = Button(doneRect.right, (doneRect.y), (doneRect.width), (doneRect.height), color = GREEN, text = 'Save Note', parentApp='notesEdit')
saveNoteRect = saveNoteButton.rect
def saveNoteButtonFunct():
    #save the note here
    success = currentUser.createSaveHandler(notesTitleInput.text, mainNotesInput.text)
    currentUser.currentNoteSaved = success
    if success:
        notesEditStatusbar.text = 'note saved successfully'
    else:
        notesEditStatusbar.text = 'note save unsuccessful'
saveNoteButton.onClickFunction = saveNoteButtonFunct

askSaveNoteModal = Modal((screen_width/4), 100, 300, 150, 'Save note?', backgroundColor=FUCHSIA, parentApp='notesEdit')
askSaveNoteModal.rect.centerx = screen_width/2
askSaveNoteModal.rect.centery = screen_height/2

askRect = askSaveNoteModal.rect

yesSaveNoteButton = Button((askRect.left), (askRect.bottom - 50), (askRect.width / 2), 50, GREEN, 'Yes', parent=askSaveNoteModal, parentApp='notesEdit')
yesSaveRect = yesSaveNoteButton.rect
def yesSaveNoteFunct():
    success = currentUser.createSaveHandler(notesTitleInput.text, mainNotesInput.text)
    if success:
        mainNotesInput.text = 'body'
        notesTitleInput.text = 'title'
        mainNotesInput.edited = notesTitleInput.edited = False
        askSaveNoteModal.active = False
        currentUser.currentNote = None
        allApps['notesMain'] = True
        allApps['notesEdit'] = False
        notesEditStatusbar.text = ''
    else:
        askSaveNoteModal.active = False
        notesEditStatusbar.text = 'Failed to save'
yesSaveNoteButton.onClickFunction = yesSaveNoteFunct

dontSaveNoteButton = Button((yesSaveRect.right), (yesSaveRect.y), (yesSaveRect.width), (yesSaveRect.height), RED, 'No', parent=askSaveNoteModal, parentApp='notesEdit')
def dontSaveNoteFunct():
    mainNotesInput.text = 'body'
    notesTitleInput.text = 'title'
    mainNotesInput.edited = notesTitleInput.edited = False
    notesEditStatusbar.text = ''
    askSaveNoteModal.active = False
    currentUser.currentNote = None
    currentUser.currentNoteSaved = True
    allApps['notesMain'] = True
    allApps['notesEdit'] = False
dontSaveNoteButton.onClickFunction = dontSaveNoteFunct

notesMoreOptionsModal = Modal(0, 0, 450, 400, 'More Options', textColor=WHITE, backgroundColor=NAVYBLUE, parentApp='notesEdit')
notesMoreOptionsModal.rect.center = (screen_width / 2, screen_height / 2)
notesMoreOptionsRect = notesMoreOptionsModal.rect

notesMoreOptionsStatusBar = InputBox(notesMoreOptionsRect.x, (notesMoreOptionsRect.bottom - 50), notesMoreOptionsRect.width, 50, changeable=False, inactiveColor=GREEN, parent=notesMoreOptionsModal, showRect=False)

mainDeleteNoteModal = Modal(0, 0, 350, 200, 'Delete Note?', textColor=WHITE, backgroundColor=DARKRED, parentApp='notesEdit')
mainDeleteNoteRect = mainDeleteNoteModal.rect
mainDeleteNoteModal.rect.center = (screen_width / 2, screen_height / 2)

shareNoteModal = Modal(0, 0, 350, 300, 'Share Note', backgroundColor=PINK, parentApp='notesEdit')
shareNoteRect = shareNoteModal.rect
shareNoteModal.rect.center = (screen_width / 2, screen_height / 2)

shareNoteInput = InputBox(shareNoteRect.left, (shareNoteRect.top + 65), shareNoteRect.width, 100, 'username', allowWrap=True, parent=shareNoteModal, parentApp='notesEdit')

shareNoteStatusBar = InputBox(shareNoteRect.left, (shareNoteInput.rect.bottom + 25), shareNoteRect.width, 50, changeable=False, allowWrap=True, inactiveColor=BLACK, showRect=False, parent=shareNoteModal, parentApp='notesEdit')

cancelShareNoteButton = Button(shareNoteRect.left, (shareNoteRect.bottom - 50), (shareNoteRect.width / 2), 50, RED, 'Cancel', parent=shareNoteModal, parentApp='notesEdit')
cancelShareNoteRect = cancelShareNoteButton.rect
def cancelShareNoteFunct():
    shareNoteInput.text = 'username'
    shareNoteStatusBar.text = ''
    shareNoteModal.active = shareNoteInput.edited = False
    notesMoreOptionsModal.active = True
cancelShareNoteButton.onClickFunction = cancelShareNoteFunct

submitShareNoteButton = Button(cancelShareNoteRect.right, cancelShareNoteRect.y, cancelShareNoteRect.width, cancelShareNoteRect.height, GREEN, 'Share', parent=shareNoteModal, parentApp='notesEdit')
def submitShareNoteFunct():
    userExists = currentUser.findUser(shareNoteInput.text)
    if userExists:
        success, message = currentUser.shareNote(shareNoteInput.text)
        if success:
            shareNoteStatusBar.text = 'note shared successfully'
        else:
            if message == 'error':
                shareNoteStatusBar.text = 'error sharing note'
            if message == 'noteShared':
                shareNoteStatusBar.text = 'already shared'
    else:
        shareNoteStatusBar.text = 'user not found'
submitShareNoteButton.onClickFunction = submitShareNoteFunct

confirmDeleteNoteButton = Button(mainDeleteNoteRect.x, (mainDeleteNoteRect.bottom - 50), (mainDeleteNoteRect.width / 2), 50, RED, 'Confirm', parent=mainDeleteNoteModal, parentApp='notesEdit')
confirmDeleteNoteRect = confirmDeleteNoteButton.rect
def confirmDeleteNoteFunct():
    success, message = currentUser.deleteNote()
    if success:
        allApps['notesEdit'] = False
        allApps['notesMain'] = True
        if message == 'noteDeleted':
            currentUser.currentNote = None
        mainDeleteNoteModal.active = notesMoreOptionsModal.active = False
        mainNotesInput.edited = notesTitleInput.edited = False
        mainNotesInput.text, notesTitleInput.text = 'body', 'title'
    else:
        pass
confirmDeleteNoteButton.onClickFunction = confirmDeleteNoteFunct

cancelDeleteNoteButton = Button(confirmDeleteNoteRect.right, confirmDeleteNoteRect.y, confirmDeleteNoteRect.width, confirmDeleteNoteRect.height, GREEN, 'Cancel', parent=mainDeleteNoteModal, parentApp='notesEdit')
def cancelDeleteNoteFunct():
    mainDeleteNoteModal.active = False
    notesMoreOptionsModal.active = True
cancelDeleteNoteButton.onClickFunction = cancelDeleteNoteFunct

notesMoreOptionButton = Button(saveNoteRect.right, saveNoteRect.y, saveNoteRect.width, saveNoteRect.height, PURPLE, 'More', WHITE, parentApp='notesEdit')
def notesMoreOptionFunct():
    mainDeleteNoteModal.active = False
    notesMoreOptionsModal.active = True if notesMoreOptionsModal.active == False else False
notesMoreOptionButton.onClickFunction = notesMoreOptionFunct

mainDeleteNoteButton = Button(notesMoreOptionsRect.left, (notesMoreOptionsRect.top + 65), (notesMoreOptionsRect.width / 2), 75, RED, 'Delete Note', parent=notesMoreOptionsModal, parentApp='notesEdit')
mainDeleteNoteRect = mainDeleteNoteButton.rect
def mainDeleteNoteFunct():
    notesMoreOptionsModal.active = False
    mainDeleteNoteModal.active = True if mainDeleteNoteModal.active == False else False
mainDeleteNoteButton.onClickFunction = mainDeleteNoteFunct

openShareNoteButton = Button(mainDeleteNoteRect.right, mainDeleteNoteRect.y, mainDeleteNoteRect.width, mainDeleteNoteRect.height, PINK, 'Share', parent=notesMoreOptionsModal, parentApp='notesEdit')
def openShareNoteFunct():
    notesMoreOptionsModal.active = False
    shareNoteModal.active = True if not shareNoteModal.active else False
openShareNoteButton.onClickFunction = openShareNoteFunct

#*------------------ notes main --------
notesMainHeader = InputBox(0, 15, 50, 0, 'Notes', textFont='extraLargeConsolas', changeable=False, inactiveColor=BLACK, parentApp='notesMain', center=True)
headerTextSize = notesMainHeader.textFont.size(notesMainHeader.text)

clock2 = Clock(0, 0, parentApp='notesMain', center=True)
clock2TextSize = clock2.textFont.size(clock2.text)
clock2.rect.bottom = (screen_height - (clock2TextSize[1] + 20))

newNoteButton = Button(0, (headerTextSize[1] + 35), (screen_width), (screen_height/6), color = GREEN, text='New Note', parentApp='notesMain')
def newNoteFunct():
    currentUser.currentNote = None
    currentUser.currentNoteSaved = True
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
    chooseNoteInput.text = 'Choose Note'
    chooseNoteInput.edited = chooseNoteInput.active = False
cancelChooseNoteButton.onClickFunction = cancelChooseNoteFunct
cancelChooseRect = cancelChooseNoteButton.rect

submitChooseNoteButton = Button(cancelChooseRect.right, 0, cancelChooseRect.width, cancelChooseRect.height, GREEN, 'Open', parent=openViewModal, parentApp='notesMain')
def submitChooseNoteFunct():
    chooseNoteInput.text  = chooseNoteInput.text[:-1] if chooseNoteInput.text[-1] == '|' else chooseNoteInput.text
    foundNote = currentUser.findNote(chooseNoteInput.text)
    if foundNote:
        chooseNoteInput.text = 'Choose Note'
        currentUser.currentNoteSaved = True
        chooseNoteInput.edited = openViewModal.active = False
        currentUser.currentNote = foundNote[0]
        notesTitleInput.text = foundNote[1]['title']
        mainNotesInput.text = foundNote[1]['body']
        notesTitleInput.edited = mainNotesInput.edited = True
        allApps['notesMain'] = False
        allApps['notesEdit'] = True
    else:
        chooseNoteInput.text = 'note not found'
        chooseNoteInput.edited = chooseNoteInput.active = False

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