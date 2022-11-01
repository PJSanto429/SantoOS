import pygame as pg
from pygame.math import Vector2
from random import choice, randint
from variables import *

class DodgerGame:
    def __init__(self):
        self.running = False
        self.paused = False
        self.setup = False
        
        self.lastEnemyCreated = 0
        self.bgTimer = 0
        
    def setupLevel(self):
        if not self.setup:
            self.setup = True
            self.enemies = pg.sprite.Group()
            self.bg = pg.sprite.Group()
            
            self.player = pg.sprite.GroupSingle()
            self.player.add(DodgerPlayer())
            
    def checkCollide(self):
        playerLasers = self.player.sprite.lasers
        if playerLasers:
            for laser in playerLasers:
                if pg.sprite.spritecollide(laser, self.enemies, True):
                    laser.kill()
            
    def createEnemy(self):
        if pg.time.get_ticks() - self.lastEnemyCreated > 1000:
            self.lastEnemyCreated = pg.time.get_ticks()
            self.enemies.add(DodgerEnemy(choice(['small', 'medium', 'large']), (randint(5, screen_width - 5), -50)))

    def createBG(self):
        now = pg.time.get_ticks()
        if now - self.bgTimer > 5:
            self.bgTimer = now
            self.bg.add(DodgerBG((randint(0, screen_width), -5)))

    def run(self):
        if self.running:
            self.setupLevel()
            self.createBG()
            screen.fill(BLACK)
            
            self.checkCollide()
            
            self.bg.update()
            self.bg.draw(screen)
            
            self.createEnemy()
            self.enemies.draw(screen)
            self.enemies.update()
            
            self.player.draw(screen)
            self.player.update()
            
class DodgerBG(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.group = 'star'
        if self.group == 'star':
            self.image = pg.Surface([2, 2])
            self.image.fill(WHITE)

        self.rect = self.image.get_rect(center = pos)
        
    def move(self):
        if self.group == 'star':
            self.rect.y += 5
            
        if self.rect.y >= screen_height + 25:
            self.kill()
        
    def update(self):
        self.move()
            
class DodgerEnemy(pg.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()
        enemySizes = {
            'small': [15, 15],
            'medium': [25, 25],
            'large': [35, 35]
        }
        self.size = size
        self.image = pg.Surface(enemySizes[size])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center = pos)
        
    def move(self):
        if self.size == 'small':
            self.rect.y += 5
        if self.size == 'medium':
            self.rect.y += 3
        if self.size == 'large':
            self.rect.y += 2
        
    def checkBoundaries(self):
        if self.rect.y > screen_height + 25:
            self.kill()
        
    def update(self):
        self.move()
            
class DodgerLaser(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface([5, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = pos)
        
        self.direction = Vector2(0, 1)
        
        self.onScreenTime = pg.time.get_ticks()
        
    def move(self):
        self.rect.y += (self.direction.y) * -8
        self.delete()
        
    def delete(self):
        if 0 > self.rect.x or self.rect.x > screen_width:
            self.kill()
        if 0 > self.rect.y or self.rect.y > screen_height:
            self.kill()
        
        if pg.time.get_ticks() - self.onScreenTime > 5000:
            self.kill()
    
    def update(self):
        self.move()

class DodgerPlayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pg.image.load('assets/spaceShip3.png').convert_alpha()
        # self.image = pg.transform.smoothscale(self.image, (150, 150))
        self.image = pg.Surface([25, 25])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = (screen_width / 2, screen_height - 25))
        
        self.lasers = pg.sprite.Group()
        self.laserTimeout = 0
        
        self.direction = Vector2(0, 0)
        self.speed = 5
        
    def checkInput(self):
        keys = pg.key.get_pressed()
        now = pg.time.get_ticks()
        if (keys[pg.K_SPACE] or pg.mouse.get_pressed()[0]) and (now - self.laserTimeout > 100):
            self.laserTimeout = now
            self.lasers.add(DodgerLaser(self.rect.center))
        
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rect.x -= 5
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rect.x += 5
            
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
        
    def update(self):
        self.checkInput()
        
        # print(len(self.lasers))
        self.lasers.update()
        self.lasers.draw(screen)

dodgerGame = DodgerGame()