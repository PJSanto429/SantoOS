import pygame as pg

pg.font.init()

screen_width = 600
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Santo OS')
pg.display.set_icon(pg.image.load('assets/greenSnake.png').convert_alpha())
clock = pg.time.Clock()
tickSpeed = 60

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 122, 146)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

BLUE = (0, 0, 255)
LIGHTBLUE = (173,216,230)

RED = (255, 0, 0)
DARKRED = (128, 0, 0)

FUCHSIA = (255, 0, 255)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
TEAL = (0,128,128)
LIGHTTEAL = (0, 255, 240)

GREY = (128, 128, 128)
LIGHTGREY = (170, 170, 170)
DARKGREY = (100, 100, 100)
VERYDARKGREY = (40, 40, 40)

allColors = [
    WHITE,
    BLACK, 
    GREEN, 
    BLUE, 
    PINK, 
    ORANGE, 
    RED, 
    DARKRED, 
    FUCHSIA, 
    LIME, 
    MAROON, 
    NAVYBLUE, 
    LIGHTBLUE,
    OLIVE, 
    PURPLE, 
    TEAL, 
    LIGHTTEAL, 
    GREY, 
    LIGHTGREY, 
    DARKGREY, 
    VERYDARKGREY
]

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
    "mediumAlgerian": pg.font.SysFont('algerian', 30),
    "mediumBauhaus": pg.font.SysFont('bauhaus93', 30),
    "mediumConsolas": pg.font.SysFont('consolas', 30),
    "mediumImpact": pg.font.SysFont('impact', 30),
    "mediumLucidaConsole": pg.font.SysFont('lucidaconsole', 30),
    "mediumSegoeuiBlack": pg.font.SysFont('segoeuiblack', 30),
    "mediumAgencyfb": pg.font.SysFont('agencyfb', 30),
    "mediumBlackAdderitc": pg.font.SysFont('blackadderitc', 30),
    "mediumBritannic": pg.font.SysFont('britannic', 30),
    "mediumCastellar": pg.font.SysFont('castellar', 30),
    "mediumColonna": pg.font.SysFont('colonna', 30),
    "mediumEngravers": pg.font.SysFont('engravers', 30),
    "mediumLucidaHandwriting": pg.font.SysFont('lucidahandwriting', 30),
    "mediumLucidaSansTypewriter": pg.font.SysFont('lucidasanstypewriter', 30),
    "mediumMagneto": pg.font.SysFont('magneto', 30),
    "mediumNiagaraSolid": pg.font.SysFont('niagarasolid', 30),
    "mediumOldEnglishText": pg.font.SysFont('oldenglishtext', 30),
    "mediumStencil": pg.font.SysFont('stencil', 30),
    "mediumHPSimplifiedBDIT": pg.font.SysFont('largeHPSimplifiedBDIT', 30),
    "mediumHPSimplified": pg.font.SysFont('hpsimplified', 30),
    "mediumArial": pg.font.SysFont('arial', 30),
    #!------------- small fonts -------------------------------------------
    "smallAlgerian": pg.font.SysFont('algerian', 20),
    "smallBauhaus": pg.font.SysFont('bauhaus93', 20),
    "smallConsolas": pg.font.SysFont('consolas', 20),
    "smallImpact": pg.font.SysFont('impact', 20),
    "smallLucidaConsole": pg.font.SysFont('lucidaconsole', 20),
    "smallSegoeuiBlack": pg.font.SysFont('segoeuiblack', 20),
    "smallAgencyfb": pg.font.SysFont('agencyfb', 20),
    "smallBlackAdderitc": pg.font.SysFont('blackadderitc', 20),
    "smallBritannic": pg.font.SysFont('britannic', 20),
    "smallCastellar": pg.font.SysFont('castellar', 20),
    "smallColonna": pg.font.SysFont('colonna', 20),
    "smallEngravers": pg.font.SysFont('engravers', 20),
    "smallLucidaHandwriting": pg.font.SysFont('lucidahandwriting', 20),
    "smallLucidaSansTypewriter": pg.font.SysFont('lucidasanstypewriter', 20),
    "smallMagneto": pg.font.SysFont('magneto', 20),
    "smallNiagaraSolid": pg.font.SysFont('niagarasolid', 20),
    "smallOldEnglishText": pg.font.SysFont('oldenglishtext', 20),
    "smallStencil": pg.font.SysFont('stencil', 20),
    "smallHPSimplifiedBDIT": pg.font.SysFont('largeHPSimplifiedBDIT', 20),
    "smallHPSimplified": pg.font.SysFont('hpsimplified', 20),
    "smallArial": pg.font.SysFont('arial', 20),
}

largeFonts = [
    "largeAlgerian",
    "largeBauhaus",
    "largeConsolas",
    "largeImpact",
    "largeLucidaConsole",
    "largeSegoeuiBlack",
    "largeAgencyfb",
    "largeBlackAdderitc",
    "largeBritannic",
    "largeCastellar",
    "largeColonna",
    "largeEngravers",
    "largeLucidaHandwriting",
    "largeLucidaSansTypewriter",
    "largeMagneto",
    "largeNiagaraSolid",
    "largeOldEnglishText",
    "largeStencil",
    "largeHPSimplifiedBDIT",
    "largeHPSimplified",
    "largeArial"
]
#allPygameFonts = pg.font.get_fonts()

allApps = {
    "none": False, #? pretty much a testbed
    "all": True,
    # "testBed": False,
    #!----home----
    "homeLoading": True,
    "homeNotLoggedIn": False,
    "homeLoggedIn": False,
    #!----notes----
    "notesMain": False,
    "notesEdit": False,
    #!----calculator ----
    "calculatorMain": False,
    #!----paint----
    "paintMain": False,
    #!----pong game----
    "pongMain": False,
    #!----test game----
    "testGameMain": False,
    #!----snake game----
    "snakeGameMain": False,
    #!----dodge game----
    "dodgerGameMain": False,
    #!----breakout game----
    "breakoutMain": False,
    #!----rock paper scissors----
    "rpsMain": False,
    #!----flappy bird----
    "flappyMain": False,
    # !----shark game----
    "sharkGameMain": False,
}

defaultButtonFont = allFonts['largeConsolas']
defaultTextInputFont = allFonts['largeConsolas']
defaultClockFont = allFonts['largeConsolas']
defaultLoaderFont = allFonts['largeConsolas']
defaultSliderFont = allFonts['largeConsolas']
defaultToggleFont = allFonts['mediumConsolas']
