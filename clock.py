#import pygame as pg
#!---------- local imports -------------------
from inputBox import InputBox
from variables import *
from randomFuncts import *
          
class Clock(InputBox):
    def __init__(
        self,
        x,
        y,
        color = BLACK,
        useDate = True,
        useTime = True,
        textFont = defaultClockFont,
        parent = False,
        parentApp = 'none',
        center = False
        ): super().__init__(
            #! input box stuff
            x = x,
            y = y,
            width = 50,
            height = 0,
            text = f'{currentTime(useDate, useTime)}',
            textFont = textFont,
            changeable = False,
            activeColor = activeColor,
            inactiveColor = color,
            parent = parent,
            parentApp = parentApp,
            maxChars = False,
            group = 'clock',
            center = center,
            allowWrap = False,
            showRect = False,
            useDate = useDate,
            useTime = useTime
        )