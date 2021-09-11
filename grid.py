import math
import random
from tkinter.constants import S
from typing import Sized
import pygame
import tkinter as tk
from tkinter import messagebox
import copy

from pygame import color

class cube(object):
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirX = dirnx
        self.dirY = dirny
        self.color = color
    
    def setdir(self, dir):
        self.dirX = dir[0]
        self.dirY = dir[1]

    def move(self):
        self.pos = (self.pos[0] + self.dirX, self.pos[1] + self.dirY) #Changing the row/col position
    
    def draw(self, surface, head=False):
        if head: 
            pygame.draw.rect(surface, (0, 255, 0), (self.pos[0] * spaceBetween,self.pos[1] * spaceBetween,spaceBetween,spaceBetween))
        else: 
            pygame.draw.rect(surface, self.color, (self.pos[0] * spaceBetween,self.pos[1] * spaceBetween,spaceBetween,spaceBetween))

class snake(object):
    body = [] #storing cube objects of the snake
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)

        self.dirX = 0
        self.dirY = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            #Gets the position of the cube, if it finds that the current position is where a turn took place it will turn in that direction
            pos = c.pos
            if pos in self.turns:
                turn = self.turns[pos]
                c.setdir(turn)

                #If the last cube just turned, then delete that turn from dictionary (no longer needed as all cubes have passed it)
                if i == len(self.body) - 1:
                    self.turns.pop(pos)

            c.move()
        
        

    def reset(self, pos):
        pass

    def addCube(self):
        tail = self.body[-1]
        newPos = (tail.pos[0] - tail.dirX, tail.pos[1] - tail.dirY)
        newCube = cube(newPos, tail.dirX, tail.dirY)
        self.body.append(newCube)
        
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0: 
                c.draw(surface, True) #using different color for head
            else: 
                c.draw(surface)


def drawGrid(surface):
    x = 0
    y = 0

    for r in range(rows):
        x += spaceBetween
        y += spaceBetween

        pygame.draw.line(surface, (255,255,255), (x, 0), (x, size)) #vertical line
        pygame.draw.line(surface, (255,255,255), (0, y), (size, y)) #horizontal line
        

def redrawWindow(surface):
    surface.fill((0,0,0)) #fills screen with black
    drawGrid(surface)
    snack.draw(surface)
    s.draw(surface)
    pygame.display.update() #updates the screen

def randomSnack(snake):
    positions = snake.body

    needPos = True
    while needPos:
        x, y = (random.randint(0, rows - 1), random.randint(0, rows - 1))
        for c in snake.body:
            if (x,y) == c.pos:
                break
        else:
            needPos = False

    return (x, y)


def main():
    global size, rows, spaceBetween, s, flag, snack

    size = 400
    rows = 20

    spaceBetween = size // rows

    #Creates window object
    win = pygame.display.set_mode((size, size))

    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(s), color = (255, 255, 0))

    #Creating clock object
    clock = pygame.time.Clock()

    flag = True

    while flag: 
        pygame.time.delay(50) #adds manual delay to prevent from running too fast
        clock.tick(10) #ensures game runs at 10 fps

        s.move()

        if s.head.pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(s), color = (255, 255, 0))

        for c in s.body[1:]:
            if s.head.pos == c.pos:
                flag = False

        if s.head.pos[0] in {-1, 20} or s.head.pos[1] in {-1, 20}:
            flag = False

        redrawWindow(win)

if __name__ == '__main__':
    main()