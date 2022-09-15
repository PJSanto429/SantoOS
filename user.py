import pygame as pg
import json

#!------ local imports -----
from errorHandler import handleError

class User:
    instances = []
    def __init__(self):
        self.__class__.instances.append(self)
        self.loggedIn = False
        self.name = ''
        self.userName = ''
        self.password = None
        
    def loginUser(self, userName, password):
        #print('given username ==>', userName)
        #print('given password ==>', password)
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