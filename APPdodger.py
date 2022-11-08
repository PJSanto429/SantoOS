import pygame as pg
from pygame.math import Vector2
from random import choice, randint, choices
from glob import glob
from variables import *
from inputBox import InputBox
from button import Button

dodgerFilePath = 'assets/dodgeGame/'
dodgerFont = 'largeLucidaSansTypewriter'
smallDodgerFont = 'smallLucidaSansTypewriter'

class DodgerGame:
    def __init__(self):
        self.running = False
        self.paused = False
        self.setup = False
        self.started = False
        self.gameOver = False
        self.pausedTimer = 0
        
    def setupLevel(self):
        if not self.setup:
            self.enemyTime = 125
            self.enemyShootTime = 250
            self.maxEnemies = 125
            self.difficultyTime = 0
            
            self.powerupTime = 2500
            self.powerupCreated = 1500
            
            self.setup = True
            self.score = 0
            self.health = 100
            self.started = False
            self.paused = False
            
            self.enemyFired = 1000
            self.failedTimer = pg.time.get_ticks()
            self.lastEnemyCreated = 0
            self.bgTimer = 0
            self.lives = 3
            
            self.lastScore = 0
            self.failed = False
            
            self.enemies = pg.sprite.Group()
            self.bg = pg.sprite.Group()
            self.explosions = pg.sprite.Group()
            self.powerups = pg.sprite.Group()
            self.enemyLasers = pg.sprite.Group()
            self.player = pg.sprite.GroupSingle(DodgerPlayer())
            self.player.sprite.ammo = {
                'singleBlaster': 0,
                'doubleBlaster': 50,
                'superLaser': 100
            }
            
    def checkCollide(self):
        playerLasers = self.player.sprite.lasers
        #* getting powerups
        
        getPowerup = pg.sprite.groupcollide(self.powerups, playerLasers, True, True)
        if getPowerup:
            self.player.sprite.handleGetPowerup(list(getPowerup)[0])
            self.explosions.add(DodgerExplosion(list(getPowerup)[0].rect))
            
        getPowerup = pg.sprite.groupcollide(self.powerups, self.player, True, False)
        if getPowerup:
            self.player.sprite.handleGetPowerup(list(getPowerup)[0])
            self.explosions.add(DodgerExplosion(list(getPowerup)[0].rect))
            
        pg.sprite.groupcollide(self.enemyLasers, playerLasers, True, True)

        #* player shooting
        if playerLasers:
            for laser in playerLasers:
                #* hitting enemy
                if pg.sprite.spritecollide(laser, self.enemies, True):
                    self.score += 5
                    self.explosions.add(DodgerExplosion(laser.rect))
                    laser.kill()
                    
        #* enemy shooting player
        enemyLasers = self.enemyLasers
        if enemyLasers:
            for laser in enemyLasers:
                if pg.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    if not self.player.sprite.firing and self.player.sprite.weapon != 'superLaser':
                        self.health -= 5
                    if self.health <= -5:
                        self.gameFailed()
                    
    def gameFailed(self):
        self.failed = True
        self.health = 100
        self.lastScore = self.score
        self.lives -= 1
        self.failedTimer = pg.time.get_ticks()
        killAll = [
            self.player.sprite.lasers,
            self.powerups,
            self.enemies,
            self.enemyLasers,
            self.explosions
        ]
        for group in killAll:
            for thing in group:
                thing.kill()

        if self.lives == 0:
            self.setup = False
            self.gameOver = True
            self.pausedTimer = pg.time.get_ticks()
            self.lives = 3
            self.lastScore = self.score
            self.score = 0
            
    def increaseDifficulty(self):
        now = pg.time.get_ticks()
        if now - self.difficultyTime > 5000:
            self.difficultyTime = now
            self.powerupTime -= 5
            self.enemyTime -= 1
            self.enemyShootTime -= 1
            self.maxEnemies += 1
        
    def enemyShoot(self):
        now = pg.time.get_ticks()
        if now - self.enemyFired > self.enemyShootTime and self.enemies.sprites:
            self.enemyFired = now
            enemy = choice(self.enemies.sprites())
            self.enemyLasers.add(DodgerLaser(enemy.rect.center, 'enemy'))
        
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

    def createPowerUp(self):
        now  = pg.time.get_ticks()
        if now - self.powerupCreated > self.powerupTime:
            self.powerupCreated = now
            self.powerups.add(DodgerPowerup())
            
    def createEnemy(self):
        # if (pg.time.get_ticks() - self.lastEnemyCreated > 1) and (not len(self.enemies) >= 9999999999):
        if (pg.time.get_ticks() - self.lastEnemyCreated > self.enemyTime) and (not len(self.enemies) >= self.maxEnemies):
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
            
            lifeWord = 'lives' if self.lives > 1 else 'life'
            dodgerStatusBox.text = f'{self.lives} {lifeWord} remaining'
            if self.gameOver:
                dodgerStatusBox.text = f'Game Over   Score: {self.lastScore}'
            dodgerStatusBox.parentApp = 'dodgerGameMain' if self.failed else 'none'
                
            if self.started:
                if not self.paused and not self.failed:
                    self.createBG()
                    self.bg.update()
                    
                    self.increaseDifficulty()
                    
                    self.createEnemy()
                    self.enemies.update()
                    
                    self.enemyShoot()
                    self.enemyLasers.update()
                    
                    self.explosions.update()
                    
                    self.createPowerUp()
                    self.powerups.update()
                    
                    self.player.sprite.lasers.update()
                
                self.bg.draw(screen)
                self.powerups.draw(screen)
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
            
            dodgerHomeButton.parentApp = 'dodgerGameMain' if (self.failed or self.paused) else 'none'
            
            #player score and health
            pg.draw.rect(screen, BLACK, [0, 0, screen_height, 75])
            
            dodgerPlayerInfoBox.text = f'Shield: {self.health}%    Score: {self.score}    Lives: {self.lives}'
            doubleAmmo = str(self.player.sprite.ammo['doubleBlaster'])
            laserAmmo = str(self.player.sprite.ammo['superLaser'])
            
            dodgerAmmoBox.text = f'Single(1): X    Double(2): {doubleAmmo}    Laser(3): {laserAmmo}'
            dodgerPlayerInfoBox.parentApp = 'dodgerGameMain' if self.started else 'none'
            dodgerAmmoBox.parentApp = 'dodgerGameMain' if self.started else 'none'

class DodgerBG(pg.sprite.Sprite):
    planetImages = {}
    for i, f in enumerate(glob(dodgerFilePath + 'planets/*')):
        img = pg.transform.smoothscale(pg.image.load(f).convert_alpha(), [100, 100])
        img.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
        planetImages[i] = img

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
            self.image = choice(self.__class__.planetImages)

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
    #* class-wide images, only loaded one time(for performance)
    largeShip = pg.image.load(f'{dodgerFilePath}enemyShip_large.png').convert_alpha()
    largeShip = pg.transform.smoothscale(largeShip, [55, 55])
    largeShip.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
    
    mediumShip = pg.image.load(f'{dodgerFilePath}enemyShip_medium.png').convert_alpha()
    mediumShip = pg.transform.smoothscale(mediumShip, [45, 45])
    mediumShip.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
    
    smallShip = pg.image.load(f'{dodgerFilePath}enemyShip_small.png').convert_alpha()
    smallShip = pg.transform.smoothscale(smallShip, [35, 35])
    smallShip.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
    
    enemyShipImages = {
        'small': smallShip,
        'medium': mediumShip,
        'large': largeShip,
    }
    
    def __init__(self, isLaser = False):
        super().__init__()
        self.isLaser = isLaser
        self.size = choice(['small', 'medium', 'large'])
        moveAmount = {
            'small': 5,
            'medium': 3,
            'large': 2
        }
        self.lowestPoint = randint(425, 500)
        self.moveDistance = moveAmount[self.size]
        if not self.isLaser:
            pos = (randint(5, screen_width - 5), -50)
            self.image = self.__class__.enemyShipImages[self.size]
            self.zigZag = choice([True, False])
            self.moveDown = True
            self.moveUp = False
            self.reachedCenter = False
        self.direction = choice(['left', 'right'])
        self.speed = randint(1, 4)
        self.rect = self.image.get_rect(center = (pos))
        self.moveVert = True
        
    def move(self):
        if self.rect.centery >= screen_width / 2:
            self.reachedCenter = True
        
        if self.moveVert:
            self.rect.y += self.moveDistance if self.moveDown else self.moveDistance * -1
            
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

        if self.rect.bottom >= self.lowestPoint:
            self.zigZag = choice([True, False])
            self.moveVert = choice([True, False])
            self.moveDown = False
            self.moveUp = True
            
        if self.rect.top <= 75 and self.reachedCenter:
            self.zigZag = choice([True, False])
            self.moveVert = choice([True, False])
            self.moveDown = True
            self.moveUp = False
        
    def checkBoundaries(self):
        if self.rect.y > screen_height + 25:
            self.kill()
            
    def update(self):
        self.move()
        
class DodgerExplosion(pg.sprite.Sprite):
    #* class-wide images, only loaded one time(for performance)
    redCircleExplosionImages = {}
    for i, f in enumerate(glob(dodgerFilePath + 'explosions/redCircle/*')):
        img = pg.transform.smoothscale(pg.image.load(f).convert_alpha(), [100, 100])
        img.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
        redCircleExplosionImages[i] = img

    blueCircleExplosionImages = {}
    for i, f in enumerate(glob(dodgerFilePath + 'explosions/blueCircle/*')):
        img = pg.transform.smoothscale(pg.image.load(f).convert_alpha(), [100, 100])
        img.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
        blueCircleExplosionImages[i] = img

    gassCircleExplosionImages = {}
    for i, f in enumerate(glob(dodgerFilePath + 'explosions/gasExplosion/*')):
        img = pg.transform.smoothscale(pg.image.load(f).convert_alpha(), [100, 100])
        img.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
        gassCircleExplosionImages[i] = img
        
    explosionTypes = [redCircleExplosionImages, blueCircleExplosionImages, gassCircleExplosionImages]
    
    def __init__(self, rect):
        super().__init__()
        self.imageNum = 0
        self.explosionType = choice(self.__class__.explosionTypes)
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

class DodgerPowerup(pg.sprite.Sprite):
    filePath = dodgerFilePath + 'powerups/'
    
    healthPowerup = pg.image.load(filePath + 'health.png')
    healthPowerup = pg.transform.smoothscale(healthPowerup, [45, 45])
    healthPowerup.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
    
    doubleBlasterPowerup = pg.image.load(filePath + 'doubleBlaster.png')
    doubleBlasterPowerup = pg.transform.smoothscale(doubleBlasterPowerup, [45, 45])
    doubleBlasterPowerup.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
    
    superLaserPowerup = pg.image.load(filePath + 'superLaser.png')
    superLaserPowerup = pg.transform.smoothscale(superLaserPowerup, [45, 45])
    superLaserPowerup.fill((50, 50, 50), special_flags=pg.BLEND_RGB_ADD)
    
    powerupImages = {
        'health': healthPowerup,
        'doubleBlaster': doubleBlasterPowerup,
        'superLaser': superLaserPowerup
    }
    
    def __init__(self):
        super().__init__()
        self.group = choice([
            'health',
            'doubleBlaster',
            'superLaser'
        ])
        self.image = self.__class__.powerupImages[self.group]
        self.rect = self.image.get_rect(center = (randint(5, screen_width - 5), -15))
        
    def destroy(self):
        if self.rect.top > screen_height + 25:
            self.kill()
            
    def move(self):
        self.rect.y += 1
        
    def update(self):
        self.move()
        self.destroy()
    
class DodgerLaser(pg.sprite.Sprite):
    def __init__(self, pos, whoShot = 'player', color = WHITE):
        super().__init__()
        self.image = pg.Surface([5, 10])
        self.image.fill(color)
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
        
        self.firing = False
        self.weapon = 'singleBlaster'
        self.rechargeTime = 100
        
        self.explosion = pg.sprite.GroupSingle()
        self.explosionCreated = False
        
        self.direction = Vector2(0, 0)
        self.speed = 5
        
    def handleGetPowerup(self, powerup: DodgerPowerup):
        group = powerup.group
        if group == 'health':
            dodgerGame.health += 5
        else:
            self.ammo[group] += 15
        
    def shootWeapon(self):
        if self.ammo[self.weapon]:
            self.ammo[self.weapon] -= 1
            if self.weapon == 'doubleBlaster':
                self.lasers.add(DodgerLaser([self.rect.centerx - 10, self.rect.centery], color=RED))
                self.lasers.add(DodgerLaser([self.rect.centerx + 10, self.rect.centery], color=RED))
            elif self.weapon == 'superLaser':
                self.lasers.add(DodgerLaser([self.rect.centerx - 10, self.rect.centery], color=ORANGE))
                self.lasers.add(DodgerLaser([self.rect.centerx - 5, self.rect.centery], color=YELLOW))
                self.lasers.add(DodgerLaser(self.rect.center, color=WHITE))
                self.lasers.add(DodgerLaser([self.rect.centerx + 5, self.rect.centery], color=YELLOW))
                self.lasers.add(DodgerLaser([self.rect.centerx + 10, self.rect.centery], color=ORANGE))
            else:
                self.lasers.add(DodgerLaser(self.rect.center, color=GREEN))
        else:
            self.lasers.add(DodgerLaser(self.rect.center))
            
    def changeWeapon(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.weapon = 'singleBlaster'
            self.rechargeTime = 100
        if keys[pg.K_2]:
            self.weapon = 'doubleBlaster'
            self.rechargeTime = 100
        if keys[pg.K_3]:
            self.weapon = 'superLaser'
            self.rechargeTime = 10
            
        if not self.ammo[self.weapon]:
            self.weapon = 'singleBlaster'
            self.rechargeTime = 100
        
    def checkInput(self):
        keys = pg.key.get_pressed()
        now = pg.time.get_ticks()
        
        if (keys[pg.K_SPACE]) and (now - self.laserTimeout > self.rechargeTime):
            if not dodgerGame.paused:
                self.laserTimeout = now
                if not dodgerGame.failed:
                    self.firing = True
                    self.shootWeapon()
        else:
            self.firing = False
        
        if not dodgerGame.paused and not dodgerGame.failed:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.rect.x -= 5
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
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
        self.ammo['singleBlaster'] += 2 #unlimited ammo for single blaster
        self.checkInput()
        self.changeWeapon()
        self.explode()
        
dodgerGame = DodgerGame()

dodgerPlayerInfoBox = InputBox(0, 0, 150, 50, '', smallDodgerFont, False, inactiveColor=WHITE, showRect=False)

dodgerAmmoBox = InputBox(0, 25, 150, 50, '', smallDodgerFont, False, inactiveColor=WHITE, showRect=False)

dodgerStartBox = InputBox(0, 450, screen_width, 50, 'Press Space to Start', dodgerFont, False, inactiveColor=WHITE, showRect=False, center=True)
dodgerStartRect = dodgerStartBox.rect

dodgerStatusBox = InputBox(0, (dodgerStartRect.top - 100), screen_width, 50, '', dodgerFont, False, inactiveColor=WHITE, showRect=False, center=True)

dodgerHomeButton = Button(0, 0, 100, 50, BLUE, 'Home')
dodgerHomeButton.rect.center = (screen_width / 2, 450)
def dodgerHomeFunct():
    dodgerGame.setup = dodgerGame.running = allApps['dodgerGameMain'] = False
    allApps['homeLoggedIn'] = True
    dodgerHomeButton.parentApp = 'none'
dodgerHomeButton.onClickFunction = dodgerHomeFunct
