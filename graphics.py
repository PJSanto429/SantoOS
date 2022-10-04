import pygame as pg
from random import randint

from variables import *

class CRT:
    def __init__(self):
        self.tv = pg.image.load('assets/tv.png').convert_alpha()
        self.tv = pg.transform.scale(self.tv, (screen_width, screen_height))
        #!activation and deactivation stuff
        self.cooldown = 1
        self.activateDeactivateTime = 0
        self.ready = True
        self.active = False

    def createCrtLines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pg.draw.line(self.tv, BLACK, (0, y_pos), (screen_width, y_pos), 1)
            
    def activateDeactivate(self):
        if self.ready:
            self.ready = False
            self.active = True if not self.active else False
            self.activateDeactivateTime = round(pg.time.get_ticks()/1000)

    def draw(self):
        if round(pg.time.get_ticks()/1000) - self.activateDeactivateTime >= self.cooldown:
            self.ready = True
        if self.active:
            self.tv.set_alpha(randint(70, 90))
            self.createCrtLines()
            screen.blit(self.tv, (0, 0))

crt = CRT()
crt.activateDeactivate()