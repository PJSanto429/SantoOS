import pygame as pg

#!---------- local imports -------------------
from errorHandler import get_current_time
from inputBox import InputBox

class Clock:
    instances = []
    def __init__(
        self,
        x,
        y,
        width,
        height,
        textColor,
        parent = False,
        parentApp = 'none'
    ):
        self.__class__.instances.append(self)
        self = InputBox(x, y, width, height, '', changeable=False, inactiveColor=textColor, parent=parent, parentApp=parentApp)
        
    def update(self):
        currentTime = get_current_time()
        self.text = f'{currentTime}'
        
    def draw(self, screen):
        pass