import pygame as pg
from inputBox import InputBox
from random import randint
from variables import *

flightBGCenter = pg.image.load('assets/flightClouds1.png')
flightBGCenter = pg.transform.scale(flightBGCenter, (screen_width, 275))
flightRectCenter = flightBGCenter.get_rect(topleft = (0, 0))

flightBG2 = pg.image.load('assets/flightClouds1.png')
flightBG2 = pg.transform.scale(flightBG2, (screen_width, 275))
flightRect2 = flightBG2.get_rect(topleft = (0, 0))

flightBG3 = pg.image.load('assets/flightClouds1.png')
flightBG3 = pg.transform.scale(flightBG3, (screen_width, 275))
flightRect3 = flightBG3.get_rect(topleft = (0, 0))

class FlightGameMain:
    def __init__(self):
        self.running = False
        self.paused = False

        self.created = False
        
    def createGame(self):
        if not self.created:
            self.created = True
            self.rectCreated = 100
            
            self.speed = [.2, 1]
            self.worldShift = 0
            self.player = pg.sprite.GroupSingle(FlightPlayer())
            self.rects = pg.sprite.Group()
            self.clouds = pg.sprite.Group()
            # self.createClouds()
            
    def createClouds(self):
        startPos = 0
        rangeSize = screen_width / 5
        for _ in range(50):
            pos = (randint(startPos, startPos + rangeSize), randint(25, 250))
            self.clouds.add(FlightClouds(pos))
            startPos += rangeSize
            
    def createRects(self):
        now = pg.time.get_ticks()
        if now - self.rectCreated > 200:
            self.rectCreated = now
            self.rects.add(FlightRect())
            
    def checkCollision(self):
        playerRect = self.player.sprite.rect
        #! vertical speed
        if playerRect.top in range(300, 345):
            if not self.speed[0] > .4 and not self.speed[1] > 3:
                self.speed[0] += .1
                self.speed[1] += 1

        elif playerRect.bottom in range(535, 570):
            if not self.speed[0] < .2 and not self.speed[1] < 1:
                self.speed[0] -= .1
                self.speed[1] -= 1
        else:
            self.speed = [.2, 1]
            
        #! horizontal speed/world shift
        if playerRect.left in range(100, 150):
            self.worldShift = 2 * self.speed[1]
        elif playerRect.right in range(screen_width - 150, screen_width - 50):
            self.worldShift = -2 * self.speed[1]
        else:
            self.worldShift = 0
            
    def run(self):
        if self.running:
            self.createGame()
            screen.fill(LIGHTBLUE)
            pg.draw.rect(screen, FLIGHTBLUE, (0, 275, screen_width, 325))
            # screen.blit(flightBG, flightRect)
            if not self.paused:
                self.rects.update()
                self.clouds.update(self.worldShift)
                self.player.update()
                
                self.createRects()
                self.checkCollision()
                
                self.rects.draw(screen)
                self.clouds.draw(screen)
                self.player.draw(screen)
                
            # pg.draw.line(screen, RED, (0, 300), (600, 300), 2)
            # pg.draw.line(screen, RED, (0, 345), (600, 345), 2)
            # pg.draw.line(screen, RED, (0, 535), (600, 535), 2)
            # pg.draw.line(screen, RED, (0, 570), (600, 570), 2)
            
            # pg.draw.line(screen, RED, (100, 275), (100, 600))
            # pg.draw.line(screen, RED, (500, 275), (500, 600))

class FlightClouds(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface([randint(45, 75), randint(45, 75)])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = pos)
        
    def move(self, worldShift):
        self.rect.x += worldShift
        
        if worldShift < 0 and self.rect.centerx < -300:
            self.rect.centerx = -300
        if worldShift > 0 and self.rect.centerx > 900:
            self.rect.centerx = 900
        
    def update(self, worldShift):
        self.move(worldShift)
                
class FlightRect(pg.sprite.Sprite):
    colorNum = 0
    colors = {
        0: [FLIGHTBLUE, 3],
        1: [LIGHTPURPLE, 2]
    }
    
    def __init__(self):
        super().__init__()
        self.__class__.colorNum += 1
        self.image = pg.Surface([screen_width, 5])
        self.color = LIGHTPURPLE
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft = (0, 275))
        
        self.moveAmt = 1
        
    def move(self):
        self.rect.y += self.moveAmt
        self.moveAmt += self.speed[0]
        
        if self.rect.top > screen_height + 10:
            self.kill()
        
    def resize(self):
        oldPos = self.rect.topleft
        self.image = pg.transform.scale(self.image, (screen_width, self.rect.height + self.speed[1]))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft = oldPos)
        
    def update(self):
        self.speed = flightGame.speed
        self.move()
        self.resize()
            
class FlightPlayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([20, 20])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center = (screen_width / 2, 450))
        
    def getInput(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.rect.y -= 4
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.rect.y += 4
        
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rect.x -= 4
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rect.x += 4
            
        if self.rect.top < 300:
            self.rect.top = 300
        if self.rect.bottom > 565:
            self.rect.bottom = 565
            
        if self.rect.left < 100:
            self.rect.left = 100
        if self.rect.right > screen_width - 100:
            self.rect.right = screen_width - 100
        
    def update(self):
        self.getInput()
        
flightGame = FlightGameMain()

flightStatusBox = InputBox(0, 150, 600, 50, '', inactiveColor=BLACK, parentApp='none', showRect=False) # !flightGameMain
