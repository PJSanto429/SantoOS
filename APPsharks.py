import pygame as pg
from random import randint, choice
from variables import *

class SharkGame:
    def __init__(self):
        self.running = False
        self.created = False
            
    def createGame(self):
        if not self.created:
            self.created = True
            
            self.enemyCreated = pg.time.get_ticks()
            self.enemies = pg.sprite.Group()
            
            self.player = pg.sprite.GroupSingle(SharkPlayer())
            
    def checkCollide(self):
        pass
            
    def createEnemy(self):
        now = pg.time.get_ticks()
        if now - self.enemyCreated > 500:
            self.enemyCreated = now
            self.enemies.add(SharkEnemy())
        
    def run(self):
        if self.running:
            screen.fill(BLUE)
            self.createGame()
            
            self.createEnemy()
            self.enemies.update()
            self.enemies.draw(screen)
            
            self.checkCollide()
            
            self.player.sprite.lasers.update()
            self.player.sprite.lasers.draw(screen)

            self.player.update()
            self.player.draw(screen)

class SharkLaser(pg.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pg.Surface([10, 5])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = pos)
        self.direction = direction
        self.speed = 10
    
    def move(self):
        self.rect.centerx += self.speed if self.direction == 'right' else -self.speed
        
        if self.rect.centerx not in range(-20, screen_width + 20):
            self.kill()
            
    def update(self):
        self.move()
        
class SharkEnemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reachedCenter = False
        self.getGroup()
        
        if self.moveType[0] == 'horizontal':
            if self.moveType[1] == 'left':
                pos = (screen_width + 35, randint(25, screen_height - 15))
            if self.moveType[1] == 'right':
                pos = (-35, randint(25, screen_height - 15))
                
        if self.moveType[0] == 'vertical':
            pos = (randint(15, screen_width - 15), screen_height + 45)
            
        self.rect = self.image.get_rect(center = (pos))
        
    def getGroup(self):
        group = randint(0, 100)
        # group = 55
        if group in range(0, 65):
            self.group = 'stingray'
            self.speed = 5
            self.moveType = ['horizontal', choice(['left', 'right'])]
            self.image = pg.Surface([35, 20])
            self.image.fill(ORANGE)
        elif group in range(65, 90):
            self.group = 'jellyfish'
            self.speed = 3
            self.moveType = ['vertical', 'up']
            self.image = pg.Surface([25, 25])
            self.image.fill(GREY)
        else:
            self.group = 'shark'

            self.speed = 3
            self.moveType = ['horizontal', choice(['left', 'right'])]
            self.image = pg.Surface([50, 25])
            self.image.fill(BLACK)
            
    def move(self):
        moveType, moveDir = self.moveType
        #* horizontal moving
        if moveType == 'horizontal':
            #* moving
            if moveDir == 'left':
                self.rect.centerx -= self.speed
                if self.rect.centerx <= screen_width / 2:
                    self.reachedCenter = True
            elif moveDir == 'right':
                self.rect.centerx += self.speed
                if self.rect.centerx >= screen_width / 2:
                    self.reachedCenter = True
            
            #* checking boundaries
            if self.reachedCenter:
                if moveDir == 'left':
                    if self.rect.right <= -15:
                        self.kill()
                if moveDir == 'right':
                    if self.rect.left >= screen_width + 15:
                        self.kill()
                        
        elif moveType == 'vertical':
            if moveDir == 'up':
                self.rect.y -= self.speed
                if self.rect.top <= 45:
                    self.moveType[1] = 'down'
                    
            if moveDir == 'down':
                self.rect.y += self.speed
                if self.rect.top >= screen_height + 15:
                    self.kill()
            
    def update(self):
        self.move()
            
class SharkPlayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([50, 25])
        self.image.fill(RED)
        self.rect = self.image.get_rect(center = (300, 300))
        self.direction = 'left'
        
        self.lasers = pg.sprite.Group()
        self.laserTimer = 0
        
    def getInput(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.laserTimer > 250:
                self.laserTimer = now
                self.lasers.add(SharkLaser(self.rect.center, self.direction))
        
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.direction = 'left'
            self.rect.centerx -= 5
        
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.direction = 'right'
            self.rect.centerx += 5
            
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.rect.centery -= 3
        
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.rect.centery += 3
            
        self.rect.left = 0 if self.rect.left < 0 else self.rect.left
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        
        self.rect.right = screen_width if self.rect.right > screen_width else self.rect.right
        self.rect.bottom = screen_height if self.rect.bottom > screen_width else self.rect.bottom
    
    def update(self):
        self.getInput()
            
sharkGame = SharkGame()