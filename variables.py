import pygame as pg

pg.font.init()

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

activeColor = BLACK
inactiveColor = LIGHTGREY

#fonts
allFonts = {
    # large fonts
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

defaultButtonFont = allFonts['largeConsolas']
defaultTextInputFont = allFonts['largeConsolas']