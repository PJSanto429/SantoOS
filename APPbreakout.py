from random import choice
import pygame as pg
from pygame import Vector2
from variables import *
from button import Button
from inputBox import InputBox

class BreakoutGame:
    def __init__(self):
        self.running = False
        self.created = False
        self.paused = False
        self.started = False
        self.failed = False
        self.gameOver = False
        self.pausedTimer = 0
        
        self.barrierSize = [screen_width / 5, 25]
        self.barrierAmount = [screen_width / self.barrierSize[0], 5]
        
    def checkPause(self):
        keys = pg.key.get_pressed()
        if (keys[pg.K_SPACE] or keys[pg.K_ESCAPE]) and pg.time.get_ticks() - self.pausedTimer > 1000:
            if keys[pg.K_SPACE]:
                self.paused = False
            if keys[pg.K_ESCAPE]:
                self.pausedTimer = pg.time.get_ticks()
                self.paused = not self.paused
            if not self.started:
                self.started = True
                
    def checkCollide(self):
        barrierCollide = pg.sprite.groupcollide(self.ball, self.barriers, False, True)
        if barrierCollide:
            self.ball.sprite.direction.x *= choice([-1, 1])
            self.ball.sprite.direction.y *= -1
                    
        if pg.sprite.spritecollide(self.ball.sprite, self.player, False):
            self.ball.sprite.direction.y *= -1
            
            playerRect = self.player.sprite.rect
            ballRect = self.ball.sprite.rect
            if ballRect.left < playerRect.centerx:
                self.ball.sprite.direction.x = 1
            else:
                self.ball.sprite.direction.x = -1
            
        ballRect = self.ball.sprite.rect
        if ballRect.right >= screen_width or ballRect.left <= 0:
            self.ball.sprite.direction.x *= -1
        if ballRect.top <= 0 or ballRect.bottom >= screen_height:
            self.ball.sprite.direction.y *= -1
        
    def createGame(self):
        if not self.created:
            self.created = True
            
            self.barriers = pg.sprite.Group()
            self.ball = pg.sprite.GroupSingle(BreakoutBall())
            self.player = pg.sprite.GroupSingle(BreakoutPlayer())
            
            self.barrierSetup()
            
    def barrierSetup(self):
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PINK, PURPLE]
        colorNum = 0
        for col in range(int(self.barrierAmount[1] + 1)):
            for row in range(int(self.barrierAmount[0] + 1)):
                x = row * self.barrierSize[0]
                y = col * self.barrierSize[1]
                self.barriers.add(BreakoutTile((x, y + 100), self.barrierSize, colors[colorNum]))
            colorNum += 1
            
    def barriersDraw(self):
        for barrier in self.barriers:
            pg.draw.rect(screen, WHITE, barrier.rect, 1)
            
    def run(self):
        if self.running:
            self.createGame()
            screen.fill(BLACK)
            
            if self.started:
                if not self.paused and not self.failed:
                    self.ball.update()
                    
            self.checkPause()
            self.checkCollide()
                
            self.barriers.draw(screen)
            self.barriersDraw()
            
            self.ball.draw(screen)
            
            self.player.draw(screen)
            self.player.update()
            
            breakoutStartBox.parentApp = 'breakoutMain' if not self.started else 'none'
            breakoutHomeButton.parentApp = 'breakoutMain' if self.paused else 'none'

class BreakoutTile(pg.sprite.Sprite):
    def __init__(self, pos, size, color):
        super().__init__()
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = pos)
        
class BreakoutBall(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = (screen_width / 2, screen_height / 2))
        self.direction = Vector2(0, 1)
        
    def move(self):
        self.rect.x += self.direction.x * 5
        self.rect.y += self.direction.y * 5
    
    def update(self):
        self.move()
        
class BreakoutPlayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([150, 15])
        self.image.fill(RED)
        self.rect = self.image.get_rect(center = (screen_width / 2, 575))
        
    def getInput(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rect.centerx += 8
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rect.centerx -= 8
            
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
    
    def update(self):
        self.getInput()

breakoutGame = BreakoutGame()

breakoutStartBox = InputBox(0, 450, screen_width, 50, 'Press Space to Start', changeable=False, inactiveColor=WHITE, showRect=False, center=True)

breakoutHomeButton = Button(0, 0, 100, 50, BLUE, 'Home')
breakoutHomeButton.rect.center = (screen_width / 2, 450)
def breakoutHomeFunct():
    breakoutGame.created = breakoutGame.running = allApps['breakoutMain'] = False
    allApps['homeLoggedIn'] = True
    breakoutHomeButton.parentApp = 'none'
breakoutHomeButton.onClickFunction = breakoutHomeFunct