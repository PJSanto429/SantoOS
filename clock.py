import pygame as pg
from time import localtime

#!---------- local imports -------------------
from errorHandler import get_current_time
from variables import *
from randomFuncts import *

def currentTime(showDate = True, showTime = True): #this gets the current time
    time2 = localtime()
    hour = time2[3] - 12 if time2[3] > 12 else time2[3]
    amPm = 'PM' if time2[3] > 12 else 'AM'
    seconds = time2[5] if time2[5] >= 10 else f'0{time2[5]}'
    
    date = f'{time2[1]}/{time2[2]}/{time2[0]}'
    time = f'{hour}:{time2[4]}:{seconds} {amPm}'
    fullTime = f'{time2[1]}/{time2[2]}/{time2[0]} {hour}:{time2[4]}:{seconds} {amPm}'
    
    if showDate and showTime:
        return fullTime
    if showDate and not showTime:
        return date
    if not showDate and showTime:
        return time

class Clock:
    instances = []
    def __init__(
        self,
        x,
        y,
        width,
        height,
        textColor,
        showDate = True,
        showTime = True,
        textFont = defaultClockFont,
        parent = False,
        parentApp = 'none'
    ):
        self.__class__.instances.append(self)
        self.rect = pg.Rect(x, y, width, height)
        self.color = textColor
        self.showDate = showDate
        self.showTime = showTime
        self.text = currentTime(self.showDate, self.showTime)
        self.textFont = textFont
        self.txt_surface = self.textFont.render(self.text, True, self.color)
        self.parentApp = parentApp
        self.parent = parent
        childToParent(self, self.parent)

    def update(self):
        localTime = currentTime(self.showDate, self.showTime)
        self.text = f'{localTime}'
        self.txt_surface = self.textFont.render(self.text, True, self.color)
        
    def draw(self, screen):
        parentActive = False
        if self.parent:
            if self.parent.active:
                parentActive = True
        else:
            parentActive = True
        if parentActive:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
            pg.draw.rect(screen, self.color, self.rect, 2)