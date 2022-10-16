import pygame as pg
import sys

from variables import *

levelMap1 = [
    '                                                                              ',
    '                                                                              ',
    '       XX    XXX       XX    XXX       XX    XXX       XX    XXX       XX    X',
    '       XX              XX              XX              XX              XX     ',
    '   PXX XXXX         XX XXXX         XX XXXX         XX XXXX         XX XXXX   ',
    '  XX   XXXX       XX   XXXX       XX   XXXX       XX   XXXX       XX   XXXX   ',
    'XXXX   XX    X  XXXX   XX    X  XXXX   XX    X  XXXX   XX    X  XXXX   XX    X',
    'XXXX        XX  XXXX        XX  XXXX        XX  XXXX        XX  XXXX        XX',
    'XXXXXX    XXXX  XXXXXX    XXXX  XXXXXX    XXXX  XXXXXX    XXXX  XXXXXX    XXXX',
    'XXXXXXXXXXXXXX  XXXXXXXXXXXXXX  XXXXXXXXXXXXXX  XXXXXXXXXXXXXX  XXXXXXXXXXXXXX',
    '       XX      X       XX    XXX       XX    XXX       XX    XXX       XX    X',
    '       XX     X        XX              XX              XX              XX     ',
    '   XX XXXX  X      XX XXXX         XX XXXX         XX XXXX         XX XXXX   ',
    '  XX   XXXX X     XX   XXXX       XX   XXXX       XX   XXXX       XX   XXXX   ',
    'XXXX   XX    X  XXXX   XX    X  XXXX   XX    X  XXXX   XX    X  XXXX   XX    X',
    'XXXX        XX  XXXX        XX  XXXX        XX  XXXX        XX  XXXX        XX',
    'XXXXXX    XXXX  XXXXXX    XXXX  XXXXXX    XXXX  XXXXXX    XXXX  XXXXXX    XXXX',
    'XXXXXXXXXXXXXX  XXXXXXXXXXXXXX  XXXXXXXXXXXXXX  XXXXXXXXXXXXXX  XXXXXXXXXXXXXX',
]
tileSize = 30

class Game:
    def __init__(self):
        self.running = False
        
    def run(self):
        # if self.running:
        level.run()

class Tile(pg.sprite.Sprite):
    instances = []
    def __init__(self, position, size):
        super().__init__()
        self.__class__.instances.append(self)
        self.image = pg.Surface((size, size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft = position)
        
    def update(self, xShift):
        self.rect.x += xShift
        
class Player(pg.sprite.Sprite):
    instances = []
    def __init__(self, pos):
        super().__init__()
        self.__class__.instances.append(self)
        self.image = pg.Surface((tileSize / 2, tileSize))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft = pos)
        
        #* movement stuff
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 4
        self.ogSpeed = self.speed
        self.gravity = 0.2
        self.jumpSpeed = -5
        self.jumped = False
        
    def getInput(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_RIGHT]:
            self.direction.x = 1
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
            
        if keys[pg.K_SPACE]:
            self.jump()
            
    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        if not self.jumped:
            self.jumped = True
            self.direction.y = self.jumpSpeed
            
    def update(self):
        self.getInput()
        self.applyGravity()
        
class Level():
    def __init__(self, levelData, displaySurf):
        self.displaySurf = displaySurf
        self.setUpLevel(levelData)
        
        self.worldShift = 0
        
    def setUpLevel(self, layout):
        self.tiles = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()
        
        for rowIndex, row in enumerate(layout):
            for colIndex, cell in enumerate(row):
                x = colIndex * tileSize
                y = rowIndex * tileSize
                if cell == 'X':
                    tile = Tile((x, y), tileSize)
                    self.tiles.add(tile)
                if cell == 'P':
                    playerSprite = Player((x, y))
                    self.player.add(playerSprite)
                    
    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x
    
        if playerX < (screen_width / 6) and directionX < 0:
            self.worldShift = player.ogSpeed
            # player.rect.left = (screen_width / 6)
            player.speed = 0
        elif playerX > screen_width - (screen_width / 6) and directionX > 0:
            self.worldShift = -player.ogSpeed
            # player.rect.right = screen_width - (screen_width / 6)
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 3
            
    def horizMoveCollision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    
    def vertMoveCollision(self):
        player = self.player.sprite
        player.applyGravity()
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                #* top collisition
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                #* bottom collision
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.jumped = False
                    player.direction.y = 0
        
    def run(self):
        #! tiles stuff
        self.tiles.update(self.worldShift)
        self.tiles.draw(screen)
        self.scrollX()
        
        #! player stuff
        self.player.update()
        self.vertMoveCollision()
        self.horizMoveCollision()
        self.player.draw(screen)

#!game
game = Game()

#!level
level = Level(levelMap1, screen)
        