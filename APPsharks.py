import pygame as pg
from pygame.math import Vector2
from random import randint, choice
from variables import *
from inputBox import InputBox

boatMapData = [
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWW                                   WWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWW WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW WWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWW GGGGGGGGGGGGG            BBBBBBB   GGGGGGGGGGGGGGGGWWWWWW',
    'WWWWWW GGGGGG P GGG              BBBBBB      GGGGGGGGGGGGGWWWWWW',
    'WWWWWW GGG       G      BBBBBB    BBBBB         GGGGGGGGGGWWWWWW',
    'WWWWWW GGG       G      BBBBBB     GGBBBBB      GGGGGGGGGGWWWWWW',
    'WWWWWW G              BBBBBBBB       GGGGGGGG        GGGGGWWWWWW',
    'WWWWWW GGG                BBBB          GGGGGBBB        GGWWWWWW',
    'WWWWWW                                       BBBB         WWWWWW',
    'WWWWWWWGG                                     BBB         WWWWWW',
    'WWWWWWWGGGGG                        BBBB       BB         WWWWWW',
    'WWWWWWWGGGGGG         GG           BBBBBB      B   BBBBBBBWWWWWW',
    'WWWWWWWGGGG          GGGG         BBBBBBBB          BBBBBBWWWWWW',
    'WWWWWWWGGGG          GGGG         BBBBBBBB          BBBBBBWWWWWW',
    'WWWWWWWGGGG          GGGG         BBBBBBBB          BBBBBBWWWWWW',
    'WWWWWWWGGGG           GG            BBBB               BBBWWWWWW',
    'WWWWWWWGG                                                BWWWWWW',
    'WWWWWWWGG                 GGG                            BWWWWWW',
    'WWWWWWWGG               GGGGBB               GGGGBBB     BWWWWWW',
    'WWWWWWW              GGGGGGGBB            GGGGGBBBBBB     WWWWWW',
    'WWWWWWW           GGGGGGGGBBBBBB         GGGGGGGGGGGBB    WWWWWW',
    'WWWWWWW         GGGGGGGGGGGBBBBBBBB    GGGGGGGGGGBBBBBBBBBWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
]

tileSize = screen_width / 15
bottomOffset = 50
sharkFont = 'smallConsolas'

class SharkGame:
    def __init__(self):
        self.running = False
        self.created = False
            
    def createGame(self):
        if not self.created:
            self.created = True
            self.worldShift = [0, 0]
            self.activity = 'shooting' # 'shooting' / 'boat'
            self.startTime = pg.time.get_ticks()
            self.mapMoved = False
            self.switchTime = 1000
            
            self.createJaws = False
            
            self.playerPower = 1
            self.jawsHealth = 2000
            self.shells = 0
            self.score = 0
            
            #* shooting stuff
            self.timeShooting = 0
            self.shootingTimer = randint(15, 25) * 1000
            
            self.enemyCreated = pg.time.get_ticks()
            self.enemies = pg.sprite.Group()
            self.explosions = pg.sprite.Group()
            self.mainShark = pg.sprite.GroupSingle()
            self.powerUps = pg.sprite.Group()
            self.playerWater = pg.sprite.GroupSingle(SharkShooterPlayer())
            
            #* boat stuff
            self.timeInBoat = pg.time.get_ticks()
            self.boatTimer = randint(8, 18) * 1000
            
            self.tiles = pg.sprite.Group()
            self.playerBoat = pg.sprite.Group()
            self.setupMap()
            
    def setupMap(self):
        for rowIndex, row in enumerate(boatMapData):
            for colIndex, cell in enumerate(row):
                x = colIndex * tileSize
                y = rowIndex * tileSize
                if cell in 'GWBtblr': # green brown top bottom left right
                    self.tiles.add(SharkMapTile((x, y), tileSize, cell))
                if cell == 'P':
                    self.createPlayer(x, y)
                    
    def createPlayer(self, x, y):
        ogX = x
        size = tileSize / 3
        for i in range(3):
            for k in range(3):
                self.playerBoat.add(SharkBoatPlayer((x, y), size, (k, i)))
                x += size
            y += size
            x = ogX
        
    def checkCollideShooting(self):
        player = self.playerWater.sprite
        for enemy in self.enemies:
            if pg.sprite.spritecollide(enemy, player.lasers, True):
                self.explosions.add(SharkExplosion(enemy.rect.center))
                createPowerup = randint(0, 4)
                if createPowerup == 1:
                    self.powerUps.add(SharkPowerup(enemy.rect.center))
                enemy.kill()
            
    def createEnemy(self):
        now = pg.time.get_ticks()
        if now - self.enemyCreated > 500:
            self.enemyCreated = now
            self.enemies.add(SharkEnemy())
        
    def checkGameMode(self):
        now = pg.time.get_ticks()
        if self.activity == 'shooting':
            self.timeShooting = now
            if self.timeShooting > self.shootingTimer:
                self.boatTimer = (randint(5, 9) * 1000) + now
                self.switchTime = now + 1000
                self.activity = 'boat'
        elif self.activity == 'boat':
            self.timeInBoat = now
            if self.timeInBoat > self.boatTimer:
                self.shootingTimer = (randint(8, 15) * 1000) + now
                self.switchTime = now + 1000
                self.activity = 'shooting'
                self.stopBoat()
                
    def stopBoat(self):
        killAll = [
            self.enemies,
            self.playerWater.sprite.lasers,
            self.mainShark
        ]
        for group in killAll:
            for thing in group:
                thing.kill()
        
    def moveScreen(self):
        if not self.mapMoved:
            self.worldShift = [-280, -200]
            self.mapMoved = True
            self.playerBoat.sprites()[0].autoMove(self.worldShift)
        
        else:
            # get player position and change self.worldShift
            boats = self.playerBoat.sprites()
            
            boatLeft = boats[0].rect.left + 5
            boatRight = boats[2].rect.right - 5
            boatDirX = boats[0].direction.x
            
            boatTop = boats[0].rect.top + 5
            boatBottom = boats[6].rect.bottom - 5
            boatDirY = boats[0].direction.y
            
            for boat in boats:
                if boatLeft < (screen_width / 6) and boatDirX < 0:
                    self.worldShift[0] = boat.ogSpeed[0]
                    boat.vertSpeed = 0
                elif boatRight > screen_width - (screen_width / 6) and boatDirX > 0:
                    self.worldShift[0] = -boat.ogSpeed[0]
                    boat.vertSpeed = 0
                else:
                    self.worldShift[0] = 0
                    boat.vertSpeed = boat.ogSpeed[0]
                    
                if boatTop < (screen_height / 6) and boatDirY < 0:
                    self.worldShift[1] = boat.ogSpeed[1]
                    boat.horSpeed = 0
                elif boatBottom > screen_height - bottomOffset - (screen_height / 6) and boatDirY > 0:
                    self.worldShift[1] = -boat.ogSpeed[1]
                    boat.horSpeed = 0
                else:
                    self.worldShift[1] = 0
                    boat.horSpeed = boat.ogSpeed[1]

    def checkCollideBoat(self):
        allBoats = self.playerBoat.sprites()
        
        topBoats = allBoats[0].getPosition('topCenter')
        bottomBoats = allBoats[0].getPosition('bottomCenter')
        leftBoats = allBoats[0].getPosition('middleLeft')
        rightBoats = allBoats[0].getPosition('middleRight')
        
        for tile in self.tiles.sprites():
            if tile.color in 'GWB':
                for boat in topBoats:
                    if tile.rect.colliderect(boat.rect):
                        boat.setAllPositions(boat.rect.top, 'top')
                        
                for boat in bottomBoats:
                    if tile.rect.colliderect(boat.rect):
                        boat.setAllPositions(boat.rect.bottom, 'bottom')
                    
                for boat in leftBoats:
                    if tile.rect.colliderect(boat.rect):
                        boat.setAllPositions(boat.rect.left, 'left')

                for boat in rightBoats:
                    if tile.rect.colliderect(boat.rect):
                        boat.setAllPositions(boat.rect.right, 'right')
                    
    def run(self):
        if self.running:
            screen.fill(BLUE)
            self.createGame()
            # self.checkGameMode()
            
            if self.activity == 'shooting':
                self.createEnemy()
                self.enemies.update()
                self.explosions.update()
                self.playerWater.sprite.lasers.update()
                self.playerWater.update()
                self.mainShark.update(self.playerWater.sprite.rect.centery)
                self.powerUps.update()
                
                self.checkCollideShooting()
                
                self.enemies.draw(screen)
                self.explosions.draw(screen)
                self.playerWater.sprite.lasers.draw(screen)
                self.playerWater.draw(screen)
                self.mainShark.draw(screen)
                self.powerUps.draw(screen)
                
            elif self.activity == 'boat':
                #gets player pos and move screen accordingly
                self.moveScreen()
                self.tiles.update(self.worldShift)
                self.tiles.draw(screen)
                
                self.checkCollideBoat()
                
                self.playerBoat.update()
                self.playerBoat.draw(screen)
                
            pg.draw.rect(screen, BLACK, (0, (screen_height - bottomOffset), screen_width, bottomOffset))
            sharkDataBox1.text = f'  Score        Shells      Power       Jaws\'s Power'
            sharkDataBox2.text = f'  {self.score}             {self.shells}           {self.playerPower}'
            #* jaws health bar
            jawsHealthW = self.jawsHealth / 13
            pg.draw.rect(screen, ORANGE, (425, 575, jawsHealthW, 15))
                    
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

class SharkPowerup(pg.sprite.Sprite):
    colors = {
        'shell': WHITE,
        'star': YELLOW,
        'crab': RED
    }
    
    def __init__(self, pos):
        super().__init__()
        self.group = choice(['shell', 'star', 'crab'])
        self.image = pg.Surface([25, 25])
        self.image.fill(self.__class__.colors[self.group])
        self.rect = self.image.get_rect(center = pos)
        
        self.hitBottom = False
        
        self.startTime = pg.time.get_ticks()
        self.timeOutTime = randint(3, 6) * 1000
        
    def move(self):
        if not self.hitBottom:
            self.rect.y += 3
        
        if self.rect.bottom >= screen_height - bottomOffset:
            self.hitBottom = True
            self.rect.bottom = screen_height - bottomOffset
    
    def checkTimeout(self):
        if self.hitBottom:
            if pg.time.get_ticks() - self.startTime > self.timeOutTime:
                self.kill()
    
    def update(self):
        self.move()
        self.checkTimeout()

class SharkEnemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reachedCenter = False
        self.getGroup()
        
        if self.moveType[0] == 'horizontal':
            if self.moveType[1] == 'left':
                pos = (screen_width + 35, randint(25, screen_height - 15 - bottomOffset))
            if self.moveType[1] == 'right':
                pos = (-35, randint(25, screen_height - 15 - bottomOffset))
                
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
        
class SharkJaws(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([275, 100])
        self.image.fill(BLACK)
        self.getPos()
        self.rect = self.image.get_rect(center = (self.moveInfo[0], (screen_height / 2)))
        
        self.reachedCenter = False
        
    def getPos(self):
        self.direction = choice(['left', 'right'])
        startPlaces = {
            'left': [(screen_width + 150), -2],
            'right': [-150, 2]
        }
        self.moveInfo = startPlaces[self.direction]
        
    def move(self, playerYPos):
        self.rect.x += self.moveInfo[1]

        if playerYPos > self.rect.y:
            self.rect.y += 1
        elif playerYPos < self.rect.y:
            self.rect.y -= 1
            
        if not self.reachedCenter:
            if self.direction == 'left':
                if self.rect.centerx < screen_width / 2:
                    self.reachedCenter = True
                if self.rect.right < -10:
                    self.kill()
            if self.direction == 'right':
                if self.rect.centerx > screen_width / 2:
                    self.reachedCenter = True
                if self.rect.left > screen_width + 10:
                    self.kill()
        
    def update(self, playerYPos):
        self.move(playerYPos)
        
class SharkBoatPlayer(pg.sprite.Sprite):
    instances = []
    places = {
        (0, 0): 'topLeft',
        (1, 0): 'topCenter',
        (2, 0): 'topRight',
        (0, 1): 'middleLeft',
        (1, 1): 'middleCenter',
        (2, 1): 'middleRight',
        (0, 2): 'bottomLeft',
        (1, 2): 'bottomCenter',
        (2, 2): 'bottomRight'
    }
    
    def __init__(self, pos, size, place):
        super().__init__()
        self.size = size
        self.__class__.instances.append(self)
        self.image = pg.Surface([self.size, self.size])
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft = pos)
        
        self.coord = place
        self.revCoords = [2, 1, 0]
        self.place = self.__class__.places[self.coord]
        
        #*moving stuff
        self.direction = Vector2(0, 0)
        self.horSpeed = 3
        self.vertSpeed = 3
        self.canUp = self.canDown = self.canLeft = self.canRight = True
        self.ogSpeed = (self.horSpeed, self.vertSpeed)
        
    def getPosition(self, place):
        for boat in self.__class__.instances:
            if place == boat.place:
                return [boat]
            
    def setAllPositions(self, pos, place):
        if place == 'top':
            self.setPositionYTop(pos)
        if place == 'bottom':
            self.setPositionYBottom(pos)
        if place == 'left':
            self.setPositionXLeft(pos)
        if place == 'right':
            self.setPositionXRight(pos)
            
    def setPositionXLeft(self, posX):
        for boat in self.__class__.instances:
            coordX = boat.coord[0]
            boat.canLeft = False
            boat.rect.left = posX + (self.size * coordX)
    
    def setPositionXRight(self, posX):
        for boat in self.__class__.instances:
            boat.canRight = False
            coordX = boat.coord[0]
            boat.rect.right = posX - (self.size * self.revCoords[coordX])
        
    def setPositionYTop(self, posY):
        for boat in self.__class__.instances:
            coordY = boat.coord[1]
            boat.canUp = False
            boat.rect.top = posY + (self.size * coordY)
    
    def setPositionYBottom(self, posY):
        height = 0
        for num, boat in enumerate(reversed(self.__class__.instances)):
            boat.canDown = False
            boat.rect.bottom = posY - (self.size * height)
            if not (num + 1) % 3:
                height += 1

    def autoMove(self, worldShift):
        for boat in self.__class__.instances:
            boat.rect.x += worldShift[0]
            boat.rect.y += worldShift[1]
    
    def getInput(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.canLeft:
            self.direction.x = -1
        elif keys[pg.K_RIGHT] and self.canRight:
            self.direction.x = 1
        else:
            self.direction.x = 0
            
        if keys[pg.K_UP] and self.canUp:
            self.direction.y = -1
        elif keys[pg.K_DOWN] and self.canDown:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        self.rect.x += self.direction.x * self.vertSpeed
        self.rect.y += self.direction.y * self.horSpeed
        self.canUp = self.canDown = self.canLeft = self.canRight = True
    
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
        self.rect.bottom = screen_height - bottomOffset if self.rect.bottom > screen_width - bottomOffset else self.rect.bottom
    
    def update(self):
        self.getInput()
            
sharkGame = SharkGame()

sharkDataBox1 = InputBox(0, (screen_height - 50), screen_width, 25, '', sharkFont, changeable=False, inactiveColor=WHITE, parentApp='sharkGameMain', showRect=False)
sharkDataRectRect = sharkDataBox1.rect

sharkDataBox2 = InputBox(0, sharkDataRectRect.bottom, screen_width, 50, '', sharkFont, changeable=False, inactiveColor=WHITE, parentApp='sharkGameMain', showRect=False)

# sharkStatusBox = InputBox(0, (screen_width / 2), screen_width, 50, '', changeable=False, inactiveColor=BLACK, showRect=False, center=True)

# sharkTimeBox = InputBox(0, 0, 250, 50, '', changeable=False, inactiveColor=BLACK, parentApp='sharkGameMain', showRect=False)
