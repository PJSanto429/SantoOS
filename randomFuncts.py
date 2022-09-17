import pygame as pg
import sys

#!-------local imports -------
from errorHandler import handleError

def childToParent(child, parent):
    try:
        parent.children.append(child)
    except Exception as err:
        handleError(err)
        
def handleQuit():
    #save and encrypt current note before quitting
    pg.quit()
    sys.exit()