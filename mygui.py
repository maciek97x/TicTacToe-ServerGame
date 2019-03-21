import pygame, sys, os, time
import numpy as np
from pygame.locals import *


colors = {'white':          (255, 255, 255),
          'black':          (  0,   0,   0),
          'red':            (255, 127, 127),
          'blue':           (127, 127, 255),
          'plot_poly':      ( 63,  63, 255),
          'plot_spline':    ( 63, 255,  63),
          'plot_spline_S':  ( 63, 255, 255),
          'points':         (  0,   0, 255),
          'grid':           (191, 191, 255),
          'main_bg':        (255, 255, 255),
          'bg':             (191, 191, 255),
          'help':           (255,  63,  63)}

def drawText(text, size, color, surface, position, allign=''):
    # function for drawing text on screen
    font = pygame.font.SysFont("consolasms", size)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if allign == 'lb':
        textrect.bottomleft = position
    elif allign == 'lt':
        textrect.topleft = position
    else:
        textrect.center = position
    surface.blit(textobj, textrect)

class Button:
    # box for reading clicks on screen
    def __init__(self, window, pos, size, type='none', color='white'):
        self.window = window
        self.pos = pos
        self.size = size
        self.type = type
        self.color = color

    def draw(self):
        pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(self.pos, self.size))
        if self.type == 'plus':
            pygame.draw.line(self.window, colors[self.color], (self.pos[0] + 5, self.pos[1] + self.size[1]/2),
                             (self.pos[0] + self.size[0] - 5, self.pos[1] + self.size[1]/2), 5)
            pygame.draw.line(self.window, colors[self.color], (self.pos[0] + self.size[0]/2, self.pos[1] + 5),
                             (self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1] - 5), 5)
        elif self.type == 'cross':
            pygame.draw.line(self.window, colors[self.color], (self.pos[0] + 5, self.pos[1] + 5),
                             (self.pos[0] + self.size[0] - 5, self.pos[1] + self.size[1] - 5), 5)
            pygame.draw.line(self.window, colors[self.color], (self.pos[0] + self.size[0] - 5, self.pos[1] + 5),
                             (self.pos[0] + 5, self.pos[1] + self.size[1] - 5), 5)
        elif self.type == '>':
            pygame.draw.line(self.window, colors[self.color], (self.pos[0] + self.size[0]/2 - 5, self.pos[1] + 5),
                             (self.pos[0] + self.size[0] - 5, self.pos[1] + self.size[1]/2), 5)
            pygame.draw.line(self.window, colors[self.color], (self.pos[0] + self.size[0]/2 - 5, self.pos[1] + self.size[1] - 5),
                             (self.pos[0] + self.size[0] - 5, self.pos[1] + self.size[1]/2), 5)
        elif self.type == '<':
            pygame.draw.line(self.window, colors[self.color], (self.pos[0] + self.size[0]/2 + 5, self.pos[1] + 5),
                             (self.pos[0] + 5, self.pos[1] + self.size[1]/2), 5)
            pygame.draw.line(self.window, colors[self.color], (self.pos[0] + self.size[0]/2 + 5, self.pos[1] + self.size[1] - 5),
                             (self.pos[0] + 5, self.pos[1] + self.size[1]/2), 5)
        
    def click(self, event):
        borders = (self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1])
        if borders[0] <= event.pos[0] <= borders[2] and borders[1] <= event.pos[1] <= borders[3]:
            return True
        return False
    
    def changePos(self, x, y):
        self.pos = (x, y)
            
class CheckBox:
    # box for reading clicks on screen
    def __init__(self, pos, size, label = '', color='white', checked = True):
        self.pos = pos
        self.size = size
        self.label = label
        self.color = color
        self.checked = checked
    
    def getValue(self):
        return self.value
    
    def draw(self):
        pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(self.pos, self.size))
        drawText(self.label, self.size[0], colors['black'], self.window, (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), 'lb')
        if self.value:
            pygame.draw.line(self.window, colors[self.color], (self.pos[0] + 5, self.pos[1] + 5),
                             (self.pos[0] + self.size[0] - 5, self.pos[1] + self.size[1] - 5), 5)
            pygame.draw.line(self.window, colors[self.color], (self.pos[0] + self.size[0] - 5, self.pos[1] + 5),
                             (self.pos[0] + 5, self.pos[1] + self.size[1] - 5), 5)
        
    def click(self, event):
        borders = (self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1])
        if borders[0] <= event.pos[0] <= borders[2] and borders[1] <= event.pos[1] <= borders[3]:
            self.checked = not self.checked
            
    def changePos(self, x, y):
        self.pos = (x, y)