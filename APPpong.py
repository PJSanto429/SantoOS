from random import randint, choice
import pygame as pg

from variables import *
from inputBox import InputBox
from button import Button

leftScore = InputBox(0, 0, 150, 50, '0', inactiveColor=WHITE, parentApp='pongMain', changeable=False)
leftScore.rect.right = screen_width / 2
rightScore = InputBox(leftScore.rect.right, 0, 150, 50, '0', inactiveColor=WHITE, parentApp='pongMain', changeable=False)

class PongGame:
    def __init__(self):
        self.running = False
        self.createGame()
        
        self.paused = False
        self.pausedTime = 0
        
    def createGame(self):
        self.paddles = pg.sprite.Group()
        self.ball = pg.sprite.GroupSingle()
        
        self.ball.add(
            Ball()
        )
        
        self.paddles.add(
            Paddle((screen_width - 40, screen_height / 2), ['player', 'p1']),
            Paddle((40, screen_height / 2), ['bot', 'p2'])
        )
        
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
            
    def checkPause(self):
        if pg.key.get_pressed()[pg.K_SPACE]:
            if (pg.time.get_ticks() - self.pausedTime) / 1000 >= 1:
                self.pausedTime = pg.time.get_ticks()
                self.paused = False if self.paused else True
        
    def run(self):
        if self.running:
            screen.fill(BLACK)
            self.ball.update()
            self.ball.draw(screen)
            self.checkCollision()
            self.checkPause()
            
            self.paddles.update(ball = self.ball.sprite.rect)
            self.paddles.draw(screen)
    
class Ball(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([5, 5])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = (screen_width / 2, screen_height / 2))
        
        self.direction = pg.math.Vector2([choice([-1, 1]), randint(-1, 1)])
        self.horSpeed = 5
        
    def update(self):
        if not pongGame.paused:
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
            self.rect.centery = ball.centery #!impossible mode
        if not pongGame.paused:
            self.rect.y += self.direction.y * self.speed
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= screen_height:
                self.rect.bottom = screen_height
    
    def update(self, ball):
        self.move(ball)
        
pongGame = PongGame()