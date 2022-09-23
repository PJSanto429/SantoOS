from time import localtime
import pygame as pg
import sys

#!-------local imports -------
from errorHandler import handleError

def childToParent(child, parent):
    try:
        if parent:
            parent.children.append(child)
    except Exception as err:
        handleError(err)
        
def handleQuit():
    #save and encrypt current note before quitting
    pg.quit()
    sys.exit()
    
def currentTime(showDate = True, showTime = True): #this gets the current time
    time1 = localtime()

    day = time1[1]
    month = time1[2]
    year = time1[0]
    
    hour = time1[3] - 12 if time1[3] > 12 else time1[3]
    minutes = time1[4] if time1[4] >= 10 else f'0{time1[4]}'
    seconds = time1[5] if time1[5] >= 10 else f'0{time1[5]}'
    amPm = 'PM' if time1[3] > 12 else 'AM'
    
    date = f'{day}/{month}/{year}'
    time = f'{hour}:{minutes}:{seconds} {amPm}'
    #fullTime = f'{time1[1]}/{time1[2]}/{time1[0]} {hour}:{minutes}:{seconds} {amPm}'
    
    if showDate and showTime:
        return f'{date} {time}'
    if showDate and not showTime:
        return date
    if not showDate and showTime:
        return time