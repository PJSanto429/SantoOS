import json
from random import randint, choice
import pygame as pg

from variables import *
from inputBox import InputBox
from button import Button
from modal import Modal

leftScore = InputBox(0, 0, 150, 50, '', inactiveColor=WHITE, parentApp='pongMain', changeable=False)
leftScore.rect.right = screen_width / 2

rightScore = InputBox(leftScore.rect.right, 0, 150, 50, '', inactiveColor=WHITE, parentApp='pongMain', changeable=False)

class PongGame:
    def __init__(self):
        self.running = False
        self.gameCreated = False
        
        self.paused = True
        self.pausedTime = 0
        
    def createGame(self):
        if not self.gameCreated:
            self.leftScore = 0
            self.rightScore = 0
            self.paddles = pg.sprite.Group()
            self.ball = pg.sprite.GroupSingle()
            
            self.ball.add(
                Ball()
            )
            
            self.paddles.add(
                Paddle((screen_width - 40, screen_height / 2), ['player', 'p1']),
                Paddle((40, screen_height / 2), ['bot', 'p2'])
            )
            self.gameCreated = True
    
    def stop(self):
        allApps['pongMain'] = False
        allApps['homeLoggedIn'] = True
        self.running = self.gameCreated = False
        startPongButton.parentApp = 'pongMain'
        gamePausedBox.parentApp = pongHomeButton.parentApp = 'none'
    
    def checkCollision(self):
        ball = self.ball.sprite
        
        for sprite in self.paddles.sprites():
            if sprite.rect.colliderect(ball.rect):
                ball.direction.x *= -1
                ball.direction.y = randint(-3, 3)
                while ball.direction.y == 0:
                    ball.direction.y = randint(-3, 3)
                
        if ball.rect.top <= 0:
            ball.direction.y *= -1
            ball.rect.top = 2
        if ball.rect.bottom >= screen_height:
            ball.rect.bottom = screen_height - 2
            ball.direction.y *= -1

        if ball.rect.centerx > screen_width + 25 or ball.rect.centerx < -25:
            if (ball.rect.centerx < -25):
                self.rightScore += 1
            if (ball.rect.centerx > screen_width + 25):
                self.leftScore += 1
            ball.rect.center = (screen_width / 2, screen_height / 2)
            ball.direction.x *= -1
            ball.pauseTimer = pg.time.get_ticks()
        
    def checkPause(self):
        if pg.key.get_pressed()[pg.K_SPACE]:
            if (pg.time.get_ticks() - self.pausedTime) / 1000 >= 1:
                self.pausedTime = pg.time.get_ticks()
                self.paused = False if self.paused else True
                pongHomeButton.parentApp = gamePausedBox.parentApp = ('pongMain' if self.paused else 'none')
                startPongButton.parentApp = 'none'

    def drawStuff(self):
        screen.fill(BLACK)
        leftScore.text = str(self.leftScore)
        rightScore.text = str(self.rightScore)
        pg.draw.line(screen, WHITE, [300, 0], [300, 600], 2)

    def run(self):
        if self.running and allApps['pongMain']:
            self.createGame()
            self.drawStuff()
            self.ball.update()
            self.ball.draw(screen)
            self.checkCollision()
            self.checkPause()
            
            self.paddles.update(ball = self.ball.sprite.rect)
            self.paddles.draw(screen)
    
class Ball(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = (screen_width / 2, screen_height / 2))
        
        self.pauseTimer = 0
        
        self.direction = pg.math.Vector2([choice([-1, 1]), randint(-1, 1)])
        self.horSpeed = 5
        
    def update(self):
        ready = (pg.time.get_ticks() - self.pauseTimer) / 1000 > 2
        if not pongGame.paused and ready:
            self.rect.y += self.direction.y * randint(1, 3)
            self.rect.x += self.direction.x * self.horSpeed
    
class Paddle(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__()
        self.image = pg.Surface([25, 100])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = pos)
        self.group = group
        
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 9
        
    def move(self, ball):
        if self.group[0] == 'player':
            keys = pg.key.get_pressed()
            if self.group[1] == 'p1':
                if keys[pg.K_UP]:
                    self.direction.y = -1
                elif keys[pg.K_DOWN]:
                    self.direction.y = 1
                else:
                    self.direction.y = 0
            if self.group[1] == 'p2':
                if keys[pg.K_s]:
                    self.direction.y = 1
                elif keys[pg.K_w]:
                    self.direction.y = -1
                else:
                    self.direction.y = 0

        if self.group[0] == 'bot':
            self.rect.centery = ball.centery
        
        if not pongGame.paused:
            self.rect.y += self.direction.y * self.speed
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= screen_height:
                self.rect.bottom = screen_height
                
    def drawLines(self):
        ball = pongGame.ball.sprite
        if self.group[1] == 'p1':
            pg.draw.line(screen, BLUE, self.rect.topleft, ball.rect.center, 2)
            pg.draw.line(screen, BLUE, self.rect.bottomleft, ball.rect.center, 2)
        if self.group[1] == 'p2':
            pg.draw.line(screen, GREEN, self.rect.topright, ball.rect.center, 2)
            pg.draw.line(screen, GREEN, self.rect.bottomright, ball.rect.center, 2)
    
    def update(self, ball):
        self.move(ball)
        self.drawLines()

gamePausedBox = InputBox(0, (screen_height / 2), 0, 0, 'Game Paused', changeable=False, inactiveColor=RED, center=True)

pongHomeButton = Button(0, 0, 100, 50, GREEN, 'Home')
pongHomeButton.rect.center = (screen_width / 2, (screen_height / 2) + 150)

startPongButton = Button(0, 0, 150, 50, BLUE, 'Start', parentApp='pongMain')
startPongButton.rect.center = (screen_width / 2, screen_height / 2)
def startPongFunct():
    startPongButton.parentApp = 'none'
    pongGame.paused = False
startPongButton.onClickFunction = startPongFunct

pongGame = PongGame()

def pongHomeFunct():
    pongGame.stop()
pongHomeButton.onClickFunction = pongHomeFunct