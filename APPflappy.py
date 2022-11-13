import pygame as pg
from pygame import Vector2
from random import randint
from inputBox import InputBox
from button import Button
from variables import *

class FlappyGame:
    def __init__(self):
        self.running = False
        self.created = False
        self.failed = False
        self.paused = False
        self.pausedTimer = pg.time.get_ticks()
        
    def createGame(self):
        if not self.created:
            self.created = True
            self.paused = False
            self.started = False
            self.score = 0
            
            self.pipeCreated = pg.time.get_ticks()
            
            self.pipes = pg.sprite.Group()
            self.player = pg.sprite.GroupSingle(FlappyPlayer())
            
    def createPipe(self):
        now = pg.time.get_ticks()
        if now - self.pipeCreated > 1500:
            self.pipeCreated = now
            topPipeHeight = randint(100, 300)
            bottomPipeTop = topPipeHeight + 150
            bottomPipeHeight = screen_height - bottomPipeTop
            self.pipes.add(
                FlappyPipe(0, topPipeHeight),
                FlappyPipe(bottomPipeTop, bottomPipeHeight)
            )
            
    def checkPause(self):
        keys = pg.key.get_pressed()
        now  = pg.time.get_ticks()
        if now - self.pausedTimer > 500:
            self.pausedTimer = now
            if keys[pg.K_ESCAPE]:
                self.paused = not self.paused
            if keys[pg.K_SPACE]:
                self.paused = False
                self.failed = False
            
    def checkCollide(self):
        player = self.player
        for pipe in self.pipes:
            if pg.sprite.spritecollide(pipe, player, False):
                self.failed = True
                self.pausedTimer = pg.time.get_ticks()
                self.created = False
                # print('player hit')
                
    def checkScore(self):
        for pipe in self.pipes:
            if pipe.rect.right + 5 < 130 and not pipe.passed:
                pipe.passed = True
                pipe.image.fill(RED)
                self.score += .5
        self.score = int(self.score)
        
    def run(self):
        if self.running:
            screen.fill(LIGHTBLUE)
            self.createGame()
            
            if not self.paused and not self.started and not self.failed:
                
                self.pipes.update()
                self.createPipe()
                
                self.player.update()
                
                self.checkCollide()
                self.checkScore()
                
                flappyGameScore.parentApp = 'flappyMain' if not self.paused else 'none'
                flappyGameScore.text = f'{self.score}'
                
            self.checkPause()
            
            flappyGameStatus.text = 'Game Over'
            flappyGameStatus.parentApp = 'flappyMain' if self.failed else 'none'
                
            # flappyGameStatus

            self.pipes.draw(screen)
            self.player.draw(screen)
                
class FlappyPipe(pg.sprite.Sprite):
    def __init__(self, ypos, height):
        super().__init__()
        self.image = pg.Surface([75, height])
        self.image.fill(GREEN)
        self.passed = False
        self.rect = self.image.get_rect(topleft = (screen_width + 100, ypos))
        
    def move(self):
        self.rect.x -= 4
        
    def checkBoundaries(self):
        if self.rect.left <= -50:
            self.kill()
    
    def update(self):
        self.move()
        self.checkBoundaries()
    
class FlappyPlayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([40, 40])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center = (150, screen_height / 2))
    
        self.direction = Vector2(0, 0)
        self.gravity = 0.6
        self.jumpSpeed = -7
        
    def checkInput(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.direction.y = self.jumpSpeed

    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def checkCollide(self):
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.direction.y = 0
            
        if self.rect.top <= 0:
            self.rect.top = 0
        
    def update(self):
        self.checkInput()
        self.applyGravity()
        self.checkCollide()
            
flappyGame = FlappyGame()

flappyGameStatus = InputBox(0, 350, screen_width, 50, '', changeable=False, center=True, showRect=False, inactiveColor=BLACK)
flappyGameScore = InputBox(0, 150, screen_width, 50, '', changeable=False, center=True, showRect=False, inactiveColor=BLACK)
