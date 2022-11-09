import pygame as pg
from pygame import Vector2
from random import choice, randint
from variables import *
from inputBox import InputBox
from button import Button

rockExt = 'assets/RPSgame/'
class RockPaperScissors:
    def __init__(self):
        self.running = False
        self.paused = False
        self.started = True
        self.created = False
        self.collideNum = 0
        self.startTime = pg.time.get_ticks()
        
    def createGame(self):
        if not self.created:
            self.created = True
            self.won = [False, 'none']
                
            self.allStuff = pg.sprite.Group()
            for _ in range(45):
                self.allStuff.add(RPScharacter((choice(['rock', 'paper', 'scissor']))))

    def checkCollide(self):
        for thing1 in self.allStuff:
            for thing2 in self.allStuff:
                if thing1 != thing2:
                    collided = pg.sprite.collide_rect(thing1, thing2)
                    if collided:
                        self.doCollide(thing1, thing2)
                                        
    def doCollide(self, thing1, thing2):
        rect1 = thing1.rect
        rect2 = thing2.rect
        
        #* rect 1 top | rect 2 bottom
        if rect1.top <= rect2.bottom:
            if (
                rect1.right <= rect2.right and rect1.left <= rect2.left
            ) or (
                rect1.right >= rect2.right and rect1.left >= rect2.left
            ):
                thing1.direction.y = -(thing1.changeDirection())
                thing2.direction.y = (thing2.changeDirection())

        #* rect 1 right | rect 2 left
        if rect1.right >= rect2.left:
            if (
                rect1.top >= rect2.top and rect1.bottom >= rect2.bottom
            ) or (
                rect1.top <= rect2.top and rect1.bottom <= rect2.bottom
            ):
                thing1.direction.x = -(thing1.changeDirection())
                thing2.direction.x = (thing2.changeDirection())
        
        self.changeGroup(thing1, thing2)
                
    def changeGroup(self, thing1, thing2):
        if pg.time.get_ticks() - self.startTime > 1500:
            if thing1.group == 'rock' and thing2.group == 'scissor':
                thing2.group = 'rock'
            
            if thing1.group == 'paper' and thing2.group == 'rock':
                thing2.group = 'paper'
            
            if thing1.group == 'scissor' and thing2.group == 'paper':
                thing2.group = 'scissor'
            
            if thing1.group == 'rock' and thing2.group == 'paper':
                thing1.group = 'paper'
            
            if thing1.group == 'paper' and thing2.group == 'scissor':
                thing1.group = 'scissor'
            
            if thing1.group == 'scissor' and thing2.group == 'rock':
                thing1.group = 'rock'
                
    def displayNum(self):
        if not self.won[0]:
            rocks = [0, 'rocks']
            papers = [0, 'paper']
            scissors = [0, 'scissors']
            
            for thing in self.allStuff:
                if thing.group == 'rock':
                    rocks[0] += 1
                if thing.group == 'paper':
                    papers[0] += 1
                if thing.group == 'scissor':
                    scissors[0] += 1
            
            for num in [rocks, papers, scissors]:
                if num[0] == 45:
                    self.won = [True, f'{num[1]}']
            
            RPSinfoBox.text = f'Rock: {rocks[0]} Paper: {papers[0]} Scissor: {scissors[0]}'

    def run(self):
        if self.running:
            screen.fill(WHITE)
            self.createGame()
            if self.won[0]:
                RPShomeButton.parentApp = 'rpsMain'
                RPSinfoBox.text = f'Winner: {self.won[1]}'
            if self.started:
                if not self.paused:
                    # self.rocks.update()
                    # self.papers.update()
                    # self.scissors.update()
                    
                    self.allStuff.update()
                    
                    self.checkCollide()
                    
                    self.displayNum()
                
                self.allStuff.draw(screen)
                # self.rocks.draw(screen)
                # self.papers.draw(screen)
                # self.scissors.draw(screen)
            
class RPScharacter(pg.sprite.Sprite):
    rockImage = pg.transform.smoothscale(pg.image.load(rockExt + 'rock.png').convert_alpha(), [30, 30])
    paperImage = pg.transform.smoothscale(pg.image.load(rockExt + 'paper.png').convert_alpha(), [30, 30])
    scissorImage = pg.transform.smoothscale(pg.image.load(rockExt + 'scissor.png').convert_alpha(), [30, 30])
    
    allImages = {
        'rock': rockImage,
        'paper': paperImage,
        'scissor': scissorImage
    }
    
    def __init__(
        self,
        group
    ):
        super().__init__()
        self.colors = {
            'rock': GREY,
            'paper': BLUE,
            'scissor': RED,
        }
        self.group = group
        self.image = self.__class__.allImages[self.group]
        self.rect = self.image.get_rect(topleft = (randint(5, screen_width - 150), randint(5, screen_height - 150)))
        self.direction = Vector2(-(self.changeDirection()), self.changeDirection())
        self.lastPos = self.rect.center
        
    def move(self):
        self.image = self.__class__.allImages[self.group]
        self.rect.center += self.direction
        
        if self.rect.bottom >= screen_height:
            self.direction.y = -(self.changeDirection())
        if self.rect.top <= 0:
            self.direction.y = (self.changeDirection())
        
        if self.rect.right >= screen_width:
            self.direction.x = -(self.changeDirection())
        if self.rect.left <= 0:
            self.direction.x = (self.changeDirection())
            
    def changeDirection(self):
        return randint(1, 2)
    
    def update(self):
        self.move()

rockPaperScissors = RockPaperScissors()

RPSinfoBox = InputBox(0, 0, screen_width, 50, '', changeable=False, inactiveColor=BLACK, parentApp='rpsMain', showRect=False)

RPShomeButton = Button(0, 0, 100, 50, BLUE, 'Home')
RPShomeButton.rect.center = (screen_width / 2, 525)
def RPShomeFunct():
    rockPaperScissors.started = rockPaperScissors.running = rockPaperScissors.created = False
    allApps['rpsMain'] = False
    allApps['homeLoggedIn'] = True
    RPShomeButton.parentApp = 'none'
RPShomeButton.onClickFunction = RPShomeFunct
