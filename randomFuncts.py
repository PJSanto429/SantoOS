from time import localtime
from variables import *
import pygame as pg
import sys
def handleQuit():
    #save and encrypt current note before quitting
    pg.quit()
    sys.exit()
    
def checkMouseClick(event):
    if event.type == pg.MOUSEBUTTONDOWN:
        return pg.mouse.get_pressed()
    return (False, False, False)
    
def currentTime(showDate = True, showTime = True): #this gets the current time
    time1 = localtime()

    day = time1[1]
    month = time1[2]
    year = time1[0]
    
    hour = time1[3] - 12 if time1[3] > 13 else time1[3]
    hour = 12 if hour == 0 else hour
    
    minutes = time1[4] if time1[4] >= 10 else f'0{time1[4]}'
    seconds = time1[5] if time1[5] >= 10 else f'0{time1[5]}'
    amPm = 'PM' if time1[3] > 12 else 'AM'
    
    date = f'{day}/{month}/{year}'
    time = f'{hour}:{minutes}:{seconds} {amPm}'
    
    if showDate and showTime:
        return f'{date} {time}'
    if showDate and not showTime:
        return date
    if not showDate and showTime:
        return time