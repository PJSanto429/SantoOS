import pygame as pg
import json

#!------ local imports -----
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from variables import *
from randomFuncts import *

class User:
    instances = []
    def __init__(self):
        self.__class__.instances.append(self)
        self.loggedIn = False
        self.name = ''
        self.userName = ''
        self.password = None
        #note stuff
        self.currentNote = None
        self.currentNoteSaved = True
        
    def loginUser(self, userName, password):
        userName = '' if userName == 'username here' else userName
        try:
            with open('allNotes/allUsers.json', 'r') as infile:
                data = json.load(infile)
                try:
                    #print('userName ==> ', userName)
                    self.userName = data[userName][0]['name']
                    self.password = data[userName][0]['password']
                    
                    #print('password ==> ', self.password)
                    #print('name ==> ', self.userName)
                    if self.userName:
                        if self.password == password:
                            return True, 'success'
                        else:
                            return False, 'password'
                    else:
                        return False, 'userName'
                except Exception as err:
                    #print(err)
                    handleError(err)
                    return False, 'error'
                #print(data)
        except Exception as err:
            handleError(err)
            #print('error ==> ', err)
            return False, 'error'
    
    def logoutUser(self):
        self.name = ''
        self.userName = ''
        self.password = None
        self.loggedIn = False
        allApps['homeNotLoggedIn'] = True
        allApps['homeLoggedIn'] = False
        
    def createSaveHandler(self, newNoteTitle, newNoteBody):
        if self.currentNote:
            self.saveNote(newNoteTitle, newNoteBody)
        else:
            self.createNewNote(newNoteTitle, newNoteBody)
        
    def createNewNote(self, newNoteTitle, newNoteBody):
        try:
            with open('allNotes/allUsers.json', 'r') as infile:
                inData = json.load(infile)
            inData["noteNum"] += 1
            noteNum = str(inData["noteNum"] + 1)
            while len(noteNum) < 4:
                noteNum = f'0{noteNum}'
            self.currentNote = noteNum
            noteData = {
                "title": newNoteTitle,
                "body": newNoteBody,
                "createdAt": currentTime(),
                "updatedAt": currentTime()
            }
            with open(f'allNotes/{noteNum}.json') as outfile:
                x = json.dumps(noteData)
                outfile.write(x)
            self.currentNoteSaved = True
            return True
        except:
            return False
        
        #with open('allNotes/allUsers.json', 'r') as infile:
        #    inData = json.load(infile)
        with open('allNotes/allUsers.json', 'w') as outfile:
            json.dump(inData, outfile)
        
    def saveNote(self, newNoteTitle, newNoteBody):
        try:
            with open(f'allNotes/{self.currentNote}.json', 'r') as infile:
                inData = json.load(infile)
            inData["title"] = newNoteTitle
            inData["body"] = newNoteBody
            inData["updatedAt"] = currentTime()
            with open(f'allNotes/{self.currentNote}.json', 'w') as outfile:
                json.dump(inData, outfile)
            return True
        except Exception as err:
            print('error ==> ', err)
            return False

# current user
currentUser = User()

#*------------------login modal -------------------------
loginModal = Modal(100, 100, 400, 400, 'log in', parentApp='homeNotLoggedIn')
userNameInput = InputBox(loginModal.rect.left, (loginModal.rect.top + 75), (loginModal.rect.width), 50, 'username', parent = loginModal, parentApp='homeNotLoggedIn')
passwordInput = InputBox((loginModal.rect.left), (userNameInput.rect.bottom + 25), (loginModal.rect.width), 50, 'password', parent = loginModal, parentApp='homeNotLoggedIn')

#testButton = Button(0, 0, 400, 400, picture='assets/icon.png', parent=loginModal, parentApp='homeNotLoggedIn')

cancelLoginButton = Button((loginModal.rect.left), (loginModal.rect.bottom - 25), (loginModal.rect.width / 2), 50, RED, 'Cancel', parent=loginModal, parentApp='homeNotLoggedIn')
def cancelLoginButtonFunct():
    userNameInput.text = ''
    passwordInput.text = ''
    loginModal.active = False
cancelLoginButton.onClickFunction = cancelLoginButtonFunct

loginButton = Button((cancelLoginButton.rect.right), (cancelLoginButton.rect.y), cancelLoginButton.rect.width, cancelLoginButton.rect.height, GREEN, 'Login', parent = loginModal, parentApp='homeNotLoggedIn')
def loginButtonFunct():
    loggedIn, status = currentUser.loginUser(userNameInput.text, passwordInput.text)
    #print(f'logged in == {loggedIn}')
    #print(f'status == {status}')
    currentUser.loggedIn = loggedIn
    if currentUser.loggedIn:
        loginStatusBox.text = 'user logged in'
        currentUser.userName = userNameInput.text
        allApps['homeNotLoggedIn'] = False
        loginModal.active = False
        allApps['homeLoggedIn'] = True
    else:
        loginStatusBox.text = 'login failed'
loginButton.onClickFunction = loginButtonFunct

loginStatusBox = InputBox((loginModal.rect.left + 15), (passwordInput.rect.bottom + 25), (loginModal.rect.width - 30), 0, changeable=False, parent=loginModal, parentApp='homeNotLoggedIn')
#* ------------------------------------------------------------------------