import pygame as pg
#!---------- local imports -------------------
#from errorHandler import get_current_time
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
        #! input box stuff
        ): super().__init__(
            x,
            y,
            50,
            0,
            f'{currentTime(useDate, useTime)}',
            textFont,
            False,
            activeColor,
            color,
            parent,
            parentApp,
            'clock',
            center,
            useDate,
            useTime
        )