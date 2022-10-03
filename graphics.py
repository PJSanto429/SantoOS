import pygame as pg
from random import randint

from variables import *

class CRT:
    def __init__(self):
        self.tv = pg.image.load('assets/tv.png').convert_alpha()
        self.tv = pg.transform.scale(self.tv, (screen_width, screen_height))
        self.active = True

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pg.draw.line(self.tv, BLACK, (0, y_pos), (screen_width, y_pos), 1)

    def draw(self):
        if self.active:
            self.tv.set_alpha(randint(70, 90))
            self.create_crt_lines()
            screen.blit(self.tv, (0, 0))

crt = CRT()