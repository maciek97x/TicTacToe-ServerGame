import pygame, sys, os, time
import numpy as np
from pygame.locals import *


colors = {'white':          (255, 255, 255),
          'black':          (  0,   0,   0),
          'red':            (255, 127, 127),
          'blue':           (127, 127, 255)}

def terminate():
    pygame.quit()
    sys.exit()
    
def draw_text(text, size, color, surface, position, allign=''):
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

class GUI:
    def __init__(self, window):
        self.__window = window
        self.__elements = []
    
    def draw(self):
        for element in self.__elements:
            element.draw()
            
    def handle_click(self, event):
        for element in self.__elements:
            element.handle_click(event)
    
    def add(self, element):
        if isinstance(element, GUIElement):
            self.__elements.append(element)
        else:
            raise TypeError
            
class GUIElement:
    def __init__(self, window, pos, size):
        self.__window = window
        self.__pos = pos
        self.__size = size
        
    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos):
        self.__pos = pos
        
    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size
    

class Button(GUIElement):
    def __init__(self, window, pos, size, text='', color='white'):
        GUIElement.__init__(self, window, pos, size)
        self.__text = text
        self.__color = color

    def draw(self):
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(self.__pos, self.__size))
        draw_text(self.__text, self.__size[0], colors['black'], self.__window,\
                  (self.__pos[0] + self.__size[0], self.__pos[1] + self.__size[1]), 'lb')
        
    def handle_click(self, event):
        borders = (self.__pos[0], self.__pos[1], self.__pos[0] + self.__size[0], self.__pos[1] + self.__size[1])
        if borders[0] <= event.__pos[0] <= borders[2] and borders[1] <= event.__pos[1] <= borders[3]:
            pass
            
class CheckBox(GUIElement):
    def __init__(self, window, pos, size, text = '', color='white', checked = True):
        GUIElement.__init__(self, window, pos, size)
        self.__text = text
        self.__color = color
        self.__checked = checked
    
    @property
    def is_checked(self):
        return self.__checked
    
    @checked.setter
    def checked(self, checked):
        self.__checked = checked
    
    def draw(self):
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(self.__pos, self.__size))
        draw_text(self.__text, self.__size[0], colors['black'], self.__window,\
                  (self.__pos[0] + self.__size[0], self.__pos[1] + self.__size[1]), 'lb')
        if self.value:
            pygame.draw.line(self.__window, colors[self.__color], (self.__pos[0] + 5, self.__pos[1] + 5),
                             (self.__pos[0] + self.__size[0] - 5, self.__pos[1] + self.__size[1] - 5), 5)
            pygame.draw.line(self.__window, colors[self.__color], (self.__pos[0] + self.__size[0] - 5, self.__pos[1] + 5),
                             (self.__pos[0] + 5, self.__pos[1] + self.__size[1] - 5), 5)
        
    def handle_click(self, event):
        borders = (self.__pos[0], self.__pos[1], self.__pos[0] + self.__size[0], self.__pos[1] + self.__size[1])
        if borders[0] <= event.__pos[0] <= borders[2] and borders[1] <= event.__pos[1] <= borders[3]:
            self.__checked = not self.__checked
            
        
class TextBox:
    def __init__(self, window, pos, size, prompt_text=''):
        GUIElement.__init__(self, window, pos, size)
        self.__prompt_text = prompt_text
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        