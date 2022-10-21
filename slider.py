import pygame as pg

from variables import *

#! not done - maybe never :p
class Slider:
    instances = []
    def __init__(
        self,
        x,
        y,
        width,
        height,
        scope = (0, 101),
        title = False, #['slider', 'top']
        showValue = False, #[True, 'right']
        backgroundColor = VERYDARKGREY,
        activeColor = BLUE,
        textColor = BLACK,
        textFont = defaultSliderFont,
        parentApp = 'none',
        parent = False,
    ):
        self.__class__.instances.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scope = scope
        
        self.title = title
        if self.title:
            self.title, self.titleLocation = self.title
            
        self.showValue = showValue
        if self.showValue:
            self.showValue, self.valueLocation = self.showValue
        
        
        