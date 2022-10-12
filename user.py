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
        self.userName = ''
        self.password = None
        #note stuff
        self.allNotes = []
        self.currentNote = None
        self.currentNoteSaved = True
        
    def loginCreateHandler(self, userName, password):
        with open('allNotes/allUsers.json') as infile:
            inData = json.load(infile)
        if userName not in inData:
            return self.createUser(userName, password)
        return False, 'userAlreadyMade' #self.loginUser(userName, password)
        
    def createUser(self, userName, password):
        try:
            with open('allNotes/allUsers.json', 'r') as infile:
                inData = json.load(infile)
            newUser = {
                userName: [
                    {
                    "password": password,
                    "encryptNotes": "False",
                    "createdNotes": [],
                    "sharedNotes": [],
                    "dateCreated": currentTime()
                    }
                ]
            }
            inData.update(newUser)
            with open('allNotes/allUsers.json', 'w') as outfile:
                json.dump(inData, outfile)
            return True, 'userCreated'
        except:# Exception as err:
            return False, 'error'
        
    def loginUser(self, userName, password):
        userName = '' if userName == 'username here' else userName
        try:
            with open('allNotes/allUsers.json', 'r') as infile:
                data = json.load(infile)
                try:
                    self.userName = userName
                    if userName in data:
                        self.password = data[userName][0]['password']
                        if self.password == password:
                            return True, 'success'
                        else:
                            self.userName = ''
                            self.password = None
                            return False, 'password'
                    else:
                        self.userName = ''
                        self.password = None
                        return False, 'username'
                except Exception as err:
                    print(err)
                    #handleError(err)
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
        
    def findUser(self, username):
        with open('allNotes/allUsers.json', 'r') as infile:
            inData = json.load(infile)
        return True if username in inData else False
        
    def handlePermissions(self, noteId, noteData):
        with open(f'allNotes/allUsers.json') as infile:
            inData = json.load(infile)
        myNotes = inData[self.userName][0]['createdNotes']
        sharedNotes = inData[self.userName][0]['sharedNotes']
        if noteId in myNotes + sharedNotes:
            return noteData
        
    def getCreatedNotes(self, setNotes = True) -> list:
        with open('allNotes/allUsers.json', 'r') as infile:
            inData = json.load(infile)
        myNotes = inData[self.userName][0]['createdNotes']
        if setNotes: #to set the gotten user notes as self.notes
            self.allNotes = myNotes
        else:
            return myNotes
        
    def getSharedNotes(self):
        with open('allNotes/allUsers.json', 'r') as infile:
            inData = json.load(infile)
        sharedNotes = inData[self.userName][0]['sharedNotes']
        return sharedNotes
        
    def findNote(self, noteTitle):
        allNotes = self.getCreatedNotes(False) + self.getSharedNotes()
        for note in allNotes:
            with open(f'allNotes/{note}.json', 'r') as infile:
                inData = json.load(infile)
                if noteTitle == inData['title'] and inData['archived'] == 'false':
                    return note, inData
        return False
                
    def getNoteInfo(self):
        if self.currentNote:
            with open(f'allNotes/{self.currentNote}.json', 'r') as infile:
                inData = json.load(infile)
            title = inData['title']
            body = inData['body']
            return title, body
        else:
            return 'title', 'body'
        
    def createSaveHandler(self, newNoteTitle, newNoteBody):
        if self.currentNote:
            return self.saveNote(newNoteTitle, newNoteBody)
        else:
            return self.createNewNote(newNoteTitle, newNoteBody)
        
    def createNewNote(self, newNoteTitle, newNoteBody):
        try:
            with open('allNotes/allUsers.json', 'r') as infile:
                inData = json.load(infile)
            inData["noteNum"] += 1
            noteNum = str(inData["noteNum"]).zfill(4)
            inData[self.userName][0]['createdNotes'].append(noteNum)
            self.currentNote = noteNum
            noteData = {
                "title": newNoteTitle,
                "body": newNoteBody,
                "createdBy": self.userName,
                "createdAt": currentTime(),
                "updatedAt": currentTime(),
                "archived": "false"
            }
            with open(f'allNotes/{noteNum}.json', 'w') as outfile:
                x = json.dumps(noteData)
                outfile.write(x)
            self.currentNoteSaved = True
            with open('allNotes/allUsers.json', 'w') as outfile:
                json.dump(inData, outfile)
            return True
        except:
            return False
        
    def deleteNote(self):
        try:
            if self.currentNote:
                with open('allNotes/allUsers.json', 'r') as inUserData:
                    inUsers = json.load(inUserData)
                if self.currentNote in inUsers[self.userName][0]['createdNotes']:
                    with open(f'allNotes/{self.currentNote}.json', 'r') as infile:
                        inData = json.load(infile)
                    inData["archived"] = "true"
                    with open(f'allNotes/{self.currentNote}.json', 'w') as outfile:
                        json.dump(inData, outfile)
                    return True, 'noteDeleted'
                if self.currentNote in inUsers[self.userName][0]['sharedNotes']:
                    inUsers[self.userName][0]['sharedNotes'].remove(self.currentNote)
                    with open('allNotes/allUsers.json', 'w') as outFile:
                        json.dump(inUsers, outFile)
                    return True, 'noteDeleted'
            return True, 'noNote'
        except Exception as err:
            print(err)
            return False, 'error'
    
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
        
    def shareNote(self, userName):
        try:
            with open('allNotes/allUsers.json', 'r') as infile:
                inData = json.load(infile)
            if self.currentNote not in inData[userName][0]["sharedNotes"]:
                inData[userName][0]["sharedNotes"].append(self.currentNote)
            else:
                return False, 'noteShared'
            with open('allNotes/allUsers.json', 'w') as outfile:
                json.dump(inData, outfile)
            return True, 'success'
        except:
            return False, 'error'

# current user
currentUser = User()

#*------------------ login modal -------------------------
loginModal = Modal(100, 100, 400, 400, 'log in', parentApp='homeNotLoggedIn')
userNameInput = InputBox(loginModal.rect.left, (loginModal.rect.top + 75), (loginModal.rect.width), 50, 'username', parent = loginModal, parentApp='homeNotLoggedIn')
passwordInput = InputBox((loginModal.rect.left), (userNameInput.rect.bottom + 25), (loginModal.rect.width), 50, 'password', parent = loginModal, parentApp='homeNotLoggedIn')

#testButton = Button(0, 0, 400, 400, picture='assets/icon.png', parent=loginModal, parentApp='homeNotLoggedIn')

cancelLoginButton = Button((loginModal.rect.left), (loginModal.rect.bottom - 25), (loginModal.rect.width / 2), 50, RED, 'Cancel', parent=loginModal, parentApp='homeNotLoggedIn')
def cancelLoginButtonFunct():
    userNameInput.text = ''
    passwordInput.text = ''
    if loginModal.active:
        loginModal.active = False
    if newUserModal.active:
        newUserModal.active = False
cancelLoginButton.onClickFunction = cancelLoginButtonFunct

loginButton = Button((cancelLoginButton.rect.right), (cancelLoginButton.rect.y), cancelLoginButton.rect.width, cancelLoginButton.rect.height, GREEN, 'Login', parent = loginModal, parentApp='homeNotLoggedIn')
def loginButtonFunct():
    if loginModal.active:
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
            if status == 'username':
                loginStatusMessageBox.text = 'user not found'
            if status == 'password':
                loginStatusMessageBox.text = 'incorrect password'
    if newUserModal.active:
        userCreated = currentUser.loginCreateHandler(userNameInput.text, passwordInput.text)
        if userCreated:
            loginStatusBox.text = 'user successfully created'
            currentUser.userName = userNameInput.text
            allApps['homeNotLoggedIn'] = False
            newUserModal.active = False
            allApps['homeLoggedIn'] = True
        else:
            loginStatusBox.text = 'user creation failed'
            if status == 'userAlreadyMade':
                loginStatusMessageBox.text = 'user already exists'
            
loginButton.onClickFunction = loginButtonFunct

loginStatusBox = InputBox((loginModal.rect.left + 15), (passwordInput.rect.bottom + 25), (loginModal.rect.width - 30), 0, changeable=False, parent=loginModal, parentApp='homeNotLoggedIn')
loginStatusRect = loginStatusBox.rect

loginStatusMessageBox = InputBox((loginStatusRect.x), (loginStatusRect.y + 50), (loginStatusRect.width), 0, changeable=False, parent=loginModal, parentApp='homeNotLoggedIn')

#* ---------------------create new user modal-----------------------------

newUserModal = Modal(100, 100, 400, 400, 'create user', parentApp='homeNotLoggedIn', backgroundColor=FUCHSIA)