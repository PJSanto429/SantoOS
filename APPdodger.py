import pygame as pg
from pygame.math import Vector2
from random import choice, randint
from glob import glob
from variables import *
from inputBox import InputBox

dodgerFilePath = 'assets/dodgeGame/'
dodgerFont = 'largeLucidaSansTypewriter'

largeShip = pg.transform.smoothscale(pg.image.load(f'{dodgerFilePath}enemyShip_large.png').convert_alpha(), [55, 55])
largeShip.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)

mediumShip = pg.transform.smoothscale(pg.image.load(f'{dodgerFilePath}enemyShip_medium.png').convert_alpha(), [45, 45])
mediumShip.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)

smallShip = pg.transform.smoothscale(pg.image.load(f'{dodgerFilePath}enemyShip_small.png').convert_alpha(), [35, 35])
smallShip.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)

planetImages = {}
for i, f in enumerate(glob(dodgerFilePath + 'planets/*')):
    img = pg.transform.smoothscale(pg.image.load(f).convert_alpha(), [100, 100])
    img.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
    planetImages[i] = img

redCircleExplosionImages = {}
expFiles = glob(dodgerFilePath + 'explosions/redCircle/*')
for i, f in enumerate(expFiles):
    img = pg.transform.smoothscale(pg.image.load(f).convert_alpha(), [100, 100])
    img.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
    redCircleExplosionImages[i] = img

blueCircleExplosionImages = {}
expFiles = glob(dodgerFilePath + 'explosions/blueCircle/*')
for i, f in enumerate(expFiles):
    img = pg.transform.smoothscale(pg.image.load(f).convert_alpha(), [100, 100])
    img.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
    blueCircleExplosionImages[i] = img

gassCircleExplosionImages = {}
expFiles = glob(dodgerFilePath + 'explosions/gasExplosion/*')
for i, f in enumerate(expFiles):
    img = pg.transform.smoothscale(pg.image.load(f).convert_alpha(), [100, 100])
    img.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
    gassCircleExplosionImages[i] = img
    
explosionTypes = [redCircleExplosionImages, blueCircleExplosionImages, gassCircleExplosionImages]

class DodgerGame:
    def __init__(self):
        self.running = False
        self.paused = False
        self.setup = False
        self.started = False
        
        self.lives = 3
        self.score = 0
        self.failed = False
        
        self.enemyFired = 1000
        self.failedTimer = 0
        self.pausedTimer = 0
        self.lastEnemyCreated = 0
        self.bgTimer = 0
        
        self.startGameImage = pg.transform.scale(pg.image.load(dodgerFilePath + 'text/startGame.png'), [350, 50])
        self.startGameRect = self.startGameImage.get_rect(center = (screen_width / 2, 400))
        
    def setupLevel(self):
        if not self.setup:
            self.setup = True
            self.enemies = pg.sprite.Group()
            self.bg = pg.sprite.Group()
            self.explosions = pg.sprite.Group()
            self.enemyLasers = pg.sprite.Group()
            self.player = pg.sprite.GroupSingle()
            self.player.add(DodgerPlayer())
            
    def checkCollide(self):
        playerLasers = self.player.sprite.lasers
        if playerLasers:
            for laser in playerLasers:
                if pg.sprite.spritecollide(laser, self.enemies, True):
                    self.explosions.add(DodgerExplosion(laser.rect))
                    laser.kill()
                    
        enemyLasers = self.enemyLasers
        if enemyLasers:
            for laser in enemyLasers:
                if pg.sprite.spritecollide(laser, self.player, False):
                    self.gameFailed()
                    
    def gameFailed(self):
        self.failed = True
        self.lives -= 1
        if not self.lives < 0:
            self.failedTimer = pg.time.get_ticks()
            killAll = [
                self.player.sprite.lasers,
                self.enemies,
                self.enemyLasers,
                self.explosions
            ]
            for group in killAll:
                for thing in group:
                    thing.kill()

        else:
            self.lives = 3
            self.score = 0
        
    def createExplosion(self, enemy):
        self.explosions.add(DodgerExplosion(enemy.rect))
        enemy.kill()
        
    def enemyShoot(self):
        now = pg.time.get_ticks()
        if now - self.enemyFired > 250 and self.enemies.sprites:
            self.enemyFired = now
            enemy = choice(self.enemies.sprites())
            self.enemyLasers.add(DodgerLaser(enemy.rect.center, 'enemy'))
        
    def checkPause(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.paused = False
            if not self.started:
                self.started = True
        if keys[pg.K_ESCAPE] and pg.time.get_ticks() - self.pausedTimer > 500:
            self.pausedTimer = pg.time.get_ticks()
            self.paused = not self.paused
            
    def createEnemy(self):
        if pg.time.get_ticks() - self.lastEnemyCreated > 150:
            self.lastEnemyCreated = pg.time.get_ticks()
            self.enemies.add(DodgerEnemy())

    def createBG(self):
        now = pg.time.get_ticks()
        if now - self.bgTimer > 5 and self.started:
            self.bgTimer = now
            self.bg.add(DodgerBG())

    def run(self):
        if self.running:
            self.setupLevel()
            screen.fill(BLACK)
            
            self.checkCollide()
            
            dodgerStartBox.parentApp = 'dodgerGameMain' if not self.started else 'none'
            
            dodgerStatusBox.text = f'{self.lives} extra lives'
            dodgerStatusBox.parentApp = 'dodgerGameMain' if self.failed else 'none'
                
            if self.started:
                if not self.paused and not self.failed:
                    self.createBG()
                    self.bg.update()
                    
                    self.createEnemy()
                    self.enemies.update()
                    
                    self.enemyShoot()
                    self.enemyLasers.update()
                    
                    self.explosions.update()
                    
                    self.player.sprite.lasers.update()
                
                self.bg.draw(screen)
                self.enemyLasers.draw(screen)
                self.enemies.draw(screen)
                self.explosions.draw(screen)
                
            self.checkPause()
            
            self.player.sprite.lasers.draw(screen)
            self.player.update()
            if not self.failed:
                self.player.draw(screen)
            self.player.sprite.explosion.draw(screen)
            self.player.sprite.explosion.update()
            
class DodgerBG(pg.sprite.Sprite):
    instances = []
    def __init__(self):
        super().__init__()
        self.__class__.instances.append(self)
        group = len(self.__class__.instances) % 3750 != 1
        self.group = 'star' if group else 'planet'
        if self.group == 'star':
            self.image = pg.Surface([2, 2])
            self.image.fill(WHITE)
            
        if self.group == 'planet':
            self.startTime = pg.time.get_ticks()
            self.image = choice(planetImages)

        self.rect = self.image.get_rect(center = (randint(0, screen_width), -65))
        
    def move(self):
        if self.group == 'star':
            self.rect.y += 5
        
        if self.group == 'planet':
            now  = pg.time.get_ticks()
            if now - self.startTime > 150:
                self.startTime = now
                self.rect.y += 1
            
        if self.rect.y >= screen_height + 25:
            self.kill()
        
    def update(self):
        self.move()
            
class DodgerEnemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = choice(['small', 'medium', 'large'])
        if self.size == 'small':
            self.image = smallShip
        if self.size == 'medium':
            self.image = mediumShip
        if self.size == 'large':
            self.image = largeShip
        self.rect = self.image.get_rect(center = (randint(5, screen_width - 5), -50))
        self.zigZag = choice([True, False])
        if self.zigZag:
            self.direction = choice(['left', 'right'])
            self.speed = randint(1, 4)
        
    def move(self):
        if self.size == 'small':
            self.rect.y += 5
        if self.size == 'medium':
            self.rect.y += 3
        if self.size == 'large':
            self.rect.y += 2
            
        if self.zigZag:
            if self.direction == 'right':
                self.rect.x += self.speed
            if self.direction == 'left':
                self.rect.x -= self.speed
            
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direction = 'right'
                self.speed = randint(1, 4)

            if self.rect.right >= screen_width:
                self.rect.right = screen_width
                self.direction = 'left'
                self.speed = randint(1, 4)
        
    def checkBoundaries(self):
        if self.rect.y > screen_height + 25:
            self.kill()
            
    def update(self):
        self.move()
        
class DodgerExplosion(pg.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.imageNum = 0
        self.explosionType = choice(explosionTypes)
        self.image = self.explosionType[self.imageNum]
        self.pos = rect.center
        self.rect = self.image.get_rect(center = rect.center)
        self.start = pg.time.get_ticks()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.start > 75:
            self.start = now
            self.imageNum += 1
            if self.imageNum > len(self.explosionType) - 1:
                self.kill()
            else:
                self.image = self.explosionType[self.imageNum]
                self.rect = self.image.get_rect(center = self.pos)
        
    def update(self):
        self.animate()
            
class DodgerLaser(pg.sprite.Sprite):
    def __init__(self, pos, whoShot = 'player'):
        super().__init__()
        self.image = pg.Surface([5, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = pos)
        
        self.direction = Vector2(0, -1) if whoShot == 'player' else Vector2(0, 1)
        
        self.onScreenTime = pg.time.get_ticks()
        
    def move(self):
        self.rect.y += (self.direction.y) * 8
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
        self.image = pg.transform.smoothscale(pg.image.load(dodgerFilePath + 'playerShip.png').convert_alpha(), (45, 45))
        self.image.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
        self.rect = self.image.get_rect(center = (screen_width / 2, screen_height - 25))
        
        self.lasers = pg.sprite.Group()
        self.laserTimeout = 0
        
        self.explosion = pg.sprite.GroupSingle()
        self.explosionCreated = False
        
        self.direction = Vector2(0, 0)
        self.speed = 5
        
    def checkInput(self):
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
        now = pg.time.get_ticks()
        
        if (keys[pg.K_SPACE] or mouse[0]) and (now - self.laserTimeout > 100):
            if not dodgerGame.paused:
                self.laserTimeout = now
                if not dodgerGame.failed:
                    self.lasers.add(DodgerLaser(self.rect.center))
                else:
                    now = pg.time.get_ticks()
                    if now - dodgerGame.failedTimer > 1000:
                        dodgerGame.failedTimer = now
                        dodgerGame.failed = False
        
        if not dodgerGame.paused and not dodgerGame.failed:
            if keys[pg.K_LEFT] or keys[pg.K_a]  or mouse[0]:
                self.rect.x -= 5
            if keys[pg.K_RIGHT] or keys[pg.K_d] or mouse[2]:
                self.rect.x += 5
            
            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.right >= screen_width:
                self.rect.right = screen_width
            
    def explode(self):
        if not self.explosion and not dodgerGame.failed:
            self.explosionCreated = False
        if dodgerGame.failed and not self.explosionCreated:
            self.explosionCreated = True
            self.explosion.add(DodgerExplosion(self.rect))
        
    def update(self):
        self.checkInput()
        self.explode()
        
dodgerGame = DodgerGame()

dodgerStartBox = InputBox(0, 450, screen_width, 50, 'Press Space to Start', dodgerFont, False, inactiveColor=WHITE, showRect=False, center=True)
dodgerStartRect = dodgerStartBox.rect

dodgerStatusBox = InputBox(0, (dodgerStartRect.top - 100), screen_width, 50, '', dodgerFont, False, inactiveColor=WHITE, showRect=False, center=True)
