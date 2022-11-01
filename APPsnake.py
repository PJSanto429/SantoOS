import pygame as pg
from pygame.math import Vector2
from random import randint, choice
from button import Button
from variables import *
from inputBox import InputBox

cellSize = 25
cellNum = (screen_width / cellSize)

class SnakeGame:
    def __init__(self):
        self.running = False
        self.paused = False
        self.failed = False
        
        self.pauseTime = pg.time.get_ticks()
        self.score = 0
        
        self.snake = Snake()
        self.fruit = Fruit()

    def start(self):
        self.paused = True
        snakeHomeButton.parentApp = snakeStatusBox.parentApp = 'snakeGameMain'
        snakeStatusBox.text = 'Press Space to Start'

    def drawGrid(self):
        color = VERYDARKGREY
        for row in range(int(cellNum)):
            if row % 2 == 0:
                for col in range(int(cellNum)):
                    if col % 2 == 0:
                        xPos = row * cellSize
                        yPos = col * cellSize
                        rect = pg.Rect(xPos, yPos, cellSize, cellSize)
                        pg.draw.rect(screen, color, rect)
            else:
                for col in range(int(cellNum)):
                    if col % 2 != 0:
                        xPos = row * cellSize
                        yPos = col * cellSize
                        rect = pg.Rect(xPos, yPos, cellSize, cellSize)
                        pg.draw.rect(screen, color, rect)

    def checkCollision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.newBlock = True
            self.fruit.randomPos()
            
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomPos()
        
    def run(self):
        if self.running:
            #screen.fill(choice(allColors)) #! crazy mode
            screen.fill(BLACK)
            self.drawGrid()
            self.checkCollision()
            self.fruit.update()
            self.snake.update()
    
class Snake:
    def __init__(self):
        self.reset()
        self.newBlock = False
        self.moveTime = pg.time.get_ticks()
        self.headDrawn = False
        
    def getColor(self):
        noColors = [BLACK, VERYDARKGREY, DARKGREY, GREY, RED]
        self.headColor = choice(allColors)
        while self.headColor in noColors:
            self.headColor = choice(allColors)
        self.color = choice(allColors)
        while self.color in noColors or self.color == self.headColor:
            self.color = choice(allColors)
        
    def reset(self):
        self.getColor()
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)
        
    def draw(self):
        for block in self.body:
            if not self.headDrawn:
                self.headDrawn = True
                color = self.headColor
            else:
                color = self.color
            xPos = int(block.x * cellSize)
            yPos = int(block.y * cellSize)
            rect = pg.Rect(xPos, yPos, cellSize, cellSize)
            pg.draw.rect(screen, color, rect)
        self.headDrawn = False
            
    def move(self):
        if (pg.time.get_ticks() - self.moveTime) >= 100 and not snakeGame.paused and not self.direction == Vector2(0, 0):
            self.moveTime = pg.time.get_ticks()
            if self.newBlock:
                self.newBlock = False
                snakeGame.score += 1
                snakeScoreBox.text = f'{snakeGame.score}'
                bodyCopy = self.body[:]
            else:
                bodyCopy = self.body[:-1]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy
            
    def getInput(self):
        keys = pg.key.get_pressed()
        if not snakeGame.paused and not snakeGame.failed:
            if keys[pg.K_UP] and self.direction != Vector2(0, 1):
                self.direction = Vector2(0, -1)
            if keys[pg.K_DOWN] and self.direction != Vector2(0, -1):
                self.direction = Vector2(0, 1)
            if keys[pg.K_LEFT] and self.direction != Vector2(1, 0):
                self.direction = Vector2(-1, 0)
            if keys[pg.K_RIGHT] and self.direction != Vector2(-1, 0):
                self.direction = Vector2(1, 0)
            
        if keys[pg.K_SPACE] or keys[pg.K_ESCAPE]:
            if pg.time.get_ticks() - snakeGame.pauseTime > 500:
                snakeGame.pauseTime = pg.time.get_ticks()
                if snakeGame.paused:
                    snakeGame.paused = False
                    snakeHomeButton.parentApp = snakeStatusBox.parentApp = 'none'
                elif not snakeGame.paused:
                    snakeGame.paused = True
                    snakeHomeButton.parentApp = snakeStatusBox.parentApp = 'snakeGameMain'
                    snakeStatusBox.text = 'Game Paused'
                if snakeGame.failed:
                    snakeGame.failed = False
        
    def checkFailure(self):
        if not 0 <= self.body[0].x < cellNum:
            snakeGame.failed = True
        if not 0 <= self.body[0].y < cellNum:
            snakeGame.failed = True
            
        for part in self.body[1:]:
            if part == self.body[0]:
                snakeGame.failed = True
        
        if snakeGame.failed:
            self.gameOver()

    def gameOver(self):
        snakeStatusBox.parentApp, snakeStatusBox.text = ['snakeGameMain', 'Game Over']
        snakeHomeButton.parentApp = 'snakeGameMain'
        snakeScoreBox.text = '0'
        snakeGame.score = 0
        snakeGame.paused = True
        snakeGame.failed = False
        self.reset()
        
    def update(self):
        self.getInput()
        self.checkFailure()
        self.draw()
        self.move()
        
class Fruit:
    def __init__(self):
        self.randomPos()
        
    def randomPos(self):
        self.x = randint(1, cellNum - 2)
        self.y = randint(1, cellNum - 2)
        self.pos = Vector2(self.x, self.y)
    
    def draw(self):
        xPos = int(self.x * cellSize)
        yPos = int(self.y * cellSize)
        self.rect = pg.Rect(xPos, yPos, cellSize, cellSize)
        pg.draw.rect(screen, RED, self.rect)
        
    def update(self):
        self.draw()

snakeGame = SnakeGame()

snakeStatusBox = InputBox(0, 0, screen_width, 100, '')
snakeStatusBox.rect.centery = screen_height / 2

snakeScoreBox = InputBox(0, 0, screen_width, 50, f'{snakeGame.score}')

snakeStatusBox.changable = snakeScoreBox.changable = False
snakeStatusBox.showRect = snakeScoreBox.showRect = False
snakeStatusBox.center = snakeScoreBox.center = True
snakeStatusBox.inactiveColor = snakeScoreBox.inactiveColor = WHITE
snakeScoreBox.parentApp = 'snakeGameMain'

snakeHomeButton = Button(0, 0, 100, 50, BLUE, 'Home')
snakeHomeButton.rect.center = (screen_width / 2, (screen_height / 2) + 200)
def snakeHomeFunct():
    snakeGame.paused = snakeGame.running = False
    snakeGame.snake.reset()
    snakeHomeButton.parentApp = snakeStatusBox.parentApp = 'none'
    snakeGame.score = 0
    snakeScoreBox.text = '0'
    allApps['homeLoggedIn'] = True
    allApps['snakeGameMain'] = False
snakeHomeButton.onClickFunction = snakeHomeFunct
