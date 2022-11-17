import pygame as pg
from pygame.math import Vector2
from random import randint, choice
from variables import *
from inputBox import InputBox

boatMapData = [
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWGGGGGGGGGGGGG                      GGGGGGGGGGGGGGGGWWWWWW',
    'WWWWWWWGGGGGG P GGG                          GGGGGGGGGGGGGWWWWWW',
    'WWWWWWWGGG       G      BBBBBB                  GGGGGGGGGGWWWWWW',
    'WWWWWWWGGG       G      BBBBBB                  GGGGGGGGGGWWWWWW',
    'WWWWWWWG              BBBBBBBB                       GGGGGWWWWWW',
    'WWWWWWWGGG                BBBB                          GGWWWWWW',
    'WWWWWWW                                                   WWWWWW',
    'WWWWWWWGG                                                 WWWWWW',
    'WWWWWWWGGGGG                        BBBB                  WWWWWW',
    'WWWWWWWGGGGGG         GG           BBBBBB          BBBBBBBWWWWWW',
    'WWWWWWWGGGG          GGGG         BBBBBBBB          BBBBBBWWWWWW',
    'WWWWWWWGGGG          GGGG         BBBBBBBB          BBBBBBWWWWWW',
    'WWWWWWWGGGG          GGGG         BBBBBBBB          BBBBBBWWWWWW',
    'WWWWWWWGGGG           GG            BBBB               BBBWWWWWW',
    'WWWWWWWGG                                                BWWWWWW',
    'WWWWWWWGG                 GGG                            BWWWWWW',
    'WWWWWWWGG               GGGGBB                           BWWWWWW',
    'WWWWWWW              GGGGGGGBB                            WWWWWW',
    'WWWWWWW           GGGGGGGGBBBBBB                          WWWWWW',
    'WWWWWWW         GGGGGGGGGGGBBBBBBBB                       WWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',]
boatMapData = [
    '     WW  ',
    '     WW P'
]


tileSize = screen_width / 15

class SharkGame:
    def __init__(self):
        self.running = False
        self.created = False
            
    def createGame(self):
        if not self.created:
            self.created = True
            self.score = 0
            self.worldShift = [0, 0]
            self.activity = 'shooting' # 'shooting' / 'boat'
            self.startTime = pg.time.get_ticks()
            self.mapMoved = True
            
            #* shooting stuff
            self.enemyCreated = pg.time.get_ticks()
            self.enemies = pg.sprite.Group()
            self.explosions = pg.sprite.Group()
            self.playerWater = pg.sprite.GroupSingle(SharkShooterPlayer())
            self.playerBoat = pg.sprite.GroupSingle()
            
            #* boat stuff
            self.tiles = pg.sprite.Group()
            self.setupMap()
            
    def setupMap(self):
        for rowIndex, row in enumerate(boatMapData):
            for colIndex, cell in enumerate(row):
                x = colIndex * tileSize
                y = rowIndex * tileSize
                if cell in 'GWBtblr': # green brown top bottom left right
                    self.tiles.add(SharkMapTile((x, y), tileSize, cell))
                if cell == 'P':
                    self.playerBoat.add(SharkBoatPlayer((x, y), tileSize))
            
    def checkCollideShooting(self):
        player = self.playerWater.sprite
        
        for enemy in self.enemies:
            if pg.sprite.spritecollide(enemy, player.lasers, True):
                self.explosions.add(SharkExplosion(enemy.rect.center))
                enemy.kill()
                self.score += randint(2, 5)
            
    def createEnemy(self):
        now = pg.time.get_ticks()
        if now - self.enemyCreated > 500:
            self.enemyCreated = now
            self.enemies.add(SharkEnemy())
        
    def moveScreen(self):
        if not self.mapMoved:
            self.worldShift = [-280, -200]
            self.mapMoved = True
            self.playerBoat.sprite.autoMove(self.worldShift)
        
        else:
            #get player position and change self.worldShift
            boat = self.playerBoat.sprite
            
            boatX = boat.rect.centerx
            boatDirX = boat.direction.x
            
            boatY = boat.rect.centery
            boatDirY = boat.direction.y
            
            if boatX < (screen_width / 6) and boatDirX < 0:
                self.worldShift[0] = boat.ogSpeed[0]
                boat.vertSpeed = 0
            elif boatX > screen_width - (screen_width / 6) and boatDirX > 0:
                self.worldShift[0] = -boat.ogSpeed[0]
                boat.vertSpeed = 0
            else:
                self.worldShift[0] = 0
                boat.vertSpeed = boat.ogSpeed[0]
                
            if boatY < (screen_height / 6) and boatDirY < 0:
                self.worldShift[1] = boat.ogSpeed[1]
                boat.horSpeed = 0
            elif boatY > screen_height - (screen_height / 6) and boatDirY > 0:
                self.worldShift[1] = -boat.ogSpeed[1]
                boat.horSpeed = 0
            else:
                self.worldShift[1] = 0
                boat.horSpeed = boat.ogSpeed[1]
                
    def checkCollideBoat(self):
        boat = self.playerBoat.sprite
        
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(boat.rect):
                if (
                    boat.rect.right in range(tile.rect.left, tile.rect.right)
                ) or (
                    boat.rect.left in range(tile.rect.left, tile.rect.right)
                ):
                    if boat.direction.y > 0 :
                        boat.rect.bottom = tile.rect.top - 2
                        print('boat bottom to tile top')
                    if boat.direction.y < 0 :
                        boat.rect.top = tile.rect.bottom + 2
                        print('boat top to tile bottom')

        for tile in self.tiles.sprites(): # for what is life if not the passion of the heart
            if tile.rect.colliderect(boat.rect):
                if (
                    boat.rect.top in range(tile.rect.top, tile.rect.bottom,)
                ) or (
                    boat.rect.bottom in range(tile.rect.top, tile.rect.bottom,)
                ):
                    # if boat.direction.y == 0:
                    if boat.direction.x > 0:
                        boat.rect.right = tile.rect.left - 2
                        print('boat right to tile left')
                    if boat.direction.x < 0:
                        boat.rect.left = tile.rect.right + 2
                        print('boat left to tile right')
                    
    def findPlayer(self):
        #add stuff in here to find the player
        #? if player.rect.center not on screen:
            #? move screenx => center - player centerx
            #? same for y
        pass

    def run(self):
        if self.running:
            screen.fill(BLUE)
            self.createGame()
            
            if self.activity == 'shooting':
                self.createEnemy()
                self.enemies.update()
                self.explosions.update()
                self.playerWater.sprite.lasers.update()
                self.playerWater.update()
                
                self.checkCollideShooting()
                
                self.enemies.draw(screen)
                self.explosions.draw(screen)
                self.playerWater.sprite.lasers.draw(screen)
                self.playerWater.draw(screen)
                
                sharkScoreBox.text = f'{self.score}'
                
            elif self.activity == 'boat':
                #gets player pos and move screen accordingly
                self.moveScreen()
                self.tiles.update(self.worldShift)
                self.tiles.draw(screen)
                self.checkCollideBoat()
                self.playerBoat.update()
                self.playerBoat.draw(screen)
                pg.draw.line(screen, RED, ((screen_width / 6), 0), ((screen_width / 6), 600), 2)
                pg.draw.line(screen, RED, (screen_width - (screen_width / 6), 0), (screen_width - (screen_width / 6), 600), 2)
                pg.draw.line(screen, RED, (0, (screen_height / 6)), (600, (screen_width / 6)), 2)
                pg.draw.line(screen, RED, (0, screen_width - (screen_height / 6)), (600, screen_width - (screen_width / 6)), 2)
                    
class SharkMapTile(pg.sprite.Sprite):
    colors = {
        'G': GREEN,
        'B': BROWN,
        'W': DARKGREY
    }
    def __init__(self, pos, size, color):
        super().__init__()
        self.image = pg.Surface([size, size])
        self.color = color
        if self.color in 'GBW':
            self.image.fill(self.__class__.colors[self.color])
        # else:
        #     self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft = pos)
        
    def move(self, shift):
        self.rect.x += shift[0]
        self.rect.y += shift[1]
    
    def update(self, shift):
        self.move(shift)
            
class SharkExplosion(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pg.Surface([10, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect(center = self.pos)
        
        self.startTime = pg.time.get_ticks()
        self.onScreenTime = 250
        
    def resize(self):
        scale = pg.transform.scale
        self.image = scale(self.image, [self.rect.width + 3, self.rect.height + 3])
        self.image.fill(RED)
        self.rect = self.image.get_rect(center = self.pos)
        
    def checkTimeout(self):
        if pg.time.get_ticks() - self.startTime > self.onScreenTime:
            self.kill()
        
    def update(self):
        self.resize()
        self.checkTimeout()

class SharkLaser(pg.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pg.Surface([10, 5])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = pos)
        self.direction = direction
        self.speed = 12
    
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
            self.speed = 3
            self.moveType = ['horizontal', choice(['left', 'right'])]
            self.image = pg.Surface([35, 20])
            self.image.fill(ORANGE)
        elif group in range(65, 90):
            self.group = 'jellyfish'
            self.speed = 2
            self.moveType = ['vertical', 'up']
            self.image = pg.Surface([25, 25])
            self.image.fill(GREY)
        else:
            self.group = 'shark'
            self.speed = 2
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
        
class SharkBoatPlayer(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pg.Surface([size, size])
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft = pos)
        
        #*moving stuff
        self.direction = Vector2(0, 0)
        self.horSpeed = 3
        self.vertSpeed = 3
        self.ogSpeed = (self.horSpeed, self.vertSpeed)
        
    def autoMove(self, worldShift):
        self.rect.x += worldShift[0]
        self.rect.y += worldShift[1]
    
    def getInput(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.direction.x = -1
        elif keys[pg.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
            
        if keys[pg.K_UP]:
            self.direction.y = -1
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        self.rect.x += self.direction.x * self.vertSpeed
        self.rect.y += self.direction.y * self.horSpeed
    
    def update(self):
        self.getInput()
            
class SharkShooterPlayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([50, 25])
        self.image.fill(DARKGREY)
        self.rect = self.image.get_rect(center = (300, 300))
        self.direction = 'left'
        
        self.lasers = pg.sprite.Group()
        self.laserTimeout = 175
        self.laserTimer = 0
        
    def getInput(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.laserTimer > self.laserTimeout:
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

sharkScoreBox = InputBox(0, 5, screen_width, 50, '', changeable=False, inactiveColor=BLACK, parentApp='sharkGameMain', showRect=False, center=True)
