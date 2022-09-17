import pygame as pg
import json

#!------ local imports -----
from errorHandler import handleError
from button import Button
from inputBox import InputBox
from modal import Modal
from variables import *

class User:
    instances = []
    def __init__(self):
        self.__class__.instances.append(self)
        self.loggedIn = False
        self.name = ''
        self.userName = ''
        self.password = None
        
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