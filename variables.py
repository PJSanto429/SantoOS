import pygame as pg

pg.font.init()

screen_width = 600
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Santo OS')
#!pg.display.set_icon(pg.image.load('assets/icon3.png'))
clock = pg.time.Clock()

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FUCHSIA = (255, 0, 255)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
TEAL = (0,128,128)

GRAY = (128, 128, 128)
LIGHTGREY = (170, 170, 170)
DARKGREY = (100, 100, 100)
VERYDARKGREY = (40, 40, 40)

activeColor = BLACK
inactiveColor = LIGHTGREY

#fonts
allFonts = {
    #!------------- extra large fonts ------------------------------------
    "extraLargeAlgerian": pg.font.SysFont('algerian', 55),
    "extraLargeBauhaus": pg.font.SysFont('bauhaus93', 55),
    "extraLargeConsolas": pg.font.SysFont('consolas', 55),
    "extraLargeImpact": pg.font.SysFont('impact', 55),
    "extraLargeLucidaConsole": pg.font.SysFont('lucidaconsole', 55),
    "extraLargeSegoeuiBlack": pg.font.SysFont('segoeuiblack', 55),
    "extraLargeAgencyfb": pg.font.SysFont('agencyfb', 55),
    "extraLargeBlackAdderitc": pg.font.SysFont('blackadderitc', 55),
    "extraLargeBritannic": pg.font.SysFont('britannic', 55),
    "extraLargeCastellar": pg.font.SysFont('castellar', 55),
    "extraLargeColonna": pg.font.SysFont('colonna', 55),
    "extraLargeEngravers": pg.font.SysFont('engravers', 55),
    "extraLargeLucidaHandwriting": pg.font.SysFont('lucidahandwriting', 55),
    "extraLargeLucidaSansTypewriter": pg.font.SysFont('lucidasanstypewriter', 55),
    "extraLargeMagneto": pg.font.SysFont('magneto', 55),
    "extraLargeNiagaraSolid": pg.font.SysFont('niagarasolid', 55),
    "extraLargeOldEnglishText": pg.font.SysFont('oldenglishtext', 55),
    "extraLargeStencil": pg.font.SysFont('stencil', 55),
    "extraLargeHPSimplifiedBDIT": pg.font.SysFont('largeHPSimplifiedBDIT', 55),
    "extraLargeHPSimplified": pg.font.SysFont('hpsimplified', 55),
    "extraLargeArial": pg.font.SysFont('arial', 55),
    #!------------- large fonts ------------------------------------------
    "largeAlgerian": pg.font.SysFont('algerian', 35),
    "largeBauhaus": pg.font.SysFont('bauhaus93', 35),
    "largeConsolas": pg.font.SysFont('consolas', 35),
    "largeImpact": pg.font.SysFont('impact', 35),
    "largeLucidaConsole": pg.font.SysFont('lucidaconsole', 35),
    "largeSegoeuiBlack": pg.font.SysFont('segoeuiblack', 35),
    "largeAgencyfb": pg.font.SysFont('agencyfb', 35),
    "largeBlackAdderitc": pg.font.SysFont('blackadderitc', 35),
    "largeBritannic": pg.font.SysFont('britannic', 35),
    "largeCastellar": pg.font.SysFont('castellar', 35),
    "largeColonna": pg.font.SysFont('colonna', 35),
    "largeEngravers": pg.font.SysFont('engravers', 35),
    "largeLucidaHandwriting": pg.font.SysFont('lucidahandwriting', 35),
    "largeLucidaSansTypewriter": pg.font.SysFont('lucidasanstypewriter', 35),
    "largeMagneto": pg.font.SysFont('magneto', 35),
    "largeNiagaraSolid": pg.font.SysFont('niagarasolid', 35),
    "largeOldEnglishText": pg.font.SysFont('oldenglishtext', 35),
    "largeStencil": pg.font.SysFont('stencil', 35),
    "largeHPSimplifiedBDIT": pg.font.SysFont('largeHPSimplifiedBDIT', 35),
    "largeHPSimplified": pg.font.SysFont('hpsimplified', 35),
    "largeArial": pg.font.SysFont('arial', 35),
    #!------------- medium fonts ------------------------------------------
    "mediumConsolas": pg.font.SysFont('consolas', 30),
    #!------------- small fonts -------------------------------------------
    "smallConsolas": pg.font.SysFont('consolas', 25),
}
#allPygameFonts = pg.font.get_fonts()

allApps = {
    "none": False,
    "all": True,
    #!----home----
    "homeNotLoggedIn": True,
    "homeLoggedIn": False,
    #!----notes----
    "notesMain": False,
    "notesNew": False,
    #!----calculator ----
    "calculatorMain": False
}

defaultButtonFont = allFonts['largeConsolas']
defaultTextInputFont = allFonts['largeConsolas']
defaultClockFont = allFonts['largeConsolas']