import pygame, sys, os, time, string
import numpy as np
from pygame.locals import *


colors = {'white':          (255, 255, 255),
          'black':          (  0,   0,   0),
          'red':            (255, 127, 127),
          'blue':           (127, 127, 255)}

    
def draw_text(text, size, color, surface, position, align=''):
    # function for drawing text on screen
    font = pygame.font.SysFont("consolasms", size)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if align == 'bottomleft':
        textrect.bottomleft = position
    elif align == 'topleft':
        textrect.topleft = position
    elif align == 'bottomright':
        textrect.bottomright = position
    elif align == 'topright':
        textrect.topright = position
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
            
    def handle_event(self, event):
        for element in self.__elements:
            element.handle_event(event)
    
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
    def window(self):
        return self.__window
    
    @window.setter
    def window(self, value):
        self.__window = value
        
    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value
        
    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value
    

class Button(GUIElement):
    def __init__(self, window, pos, size, text='', color='white'):
        GUIElement.__init__(self, window, pos, size)
        self.__text = text
        self.__color = color

    def draw(self):
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(self.__pos, self.__size))
        text_size = self.size[1]*4//5
        draw_text(self.__text, text_size, colors['black'], self.window,\
                  (self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2))
        
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            borders = (self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1])
            if borders[0] <= event.pos[0] <= borders[2] and borders[1] <= event.pos[1] <= borders[3]:
                pass
            
class CheckBox(GUIElement):
    def __init__(self, window, pos, size, text = '', color='white', checked = True):
        GUIElement.__init__(self, window, pos, size)
        self.__text = text
        self.__color = color
        self.__checked = checked
    
    @property
    def checked(self):
        return self.__checked
    
    @checked.setter
    def checked(self, value):
        self.__checked = value
    
    def draw(self):
        pygame.draw.rect(self.__window, (0, 0, 0), pygame.Rect(self.pos, self.size))
        text_size = self.size[1]*4//5
        draw_text(self.__text, text_size, colors['black'], self.window,\
                  (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), 'lb')
        if self.value:
            pygame.draw.line(self.window, colors[self.__color], (self.pos[0] + 5, self.pos[1] + 5),
                             (self.pos[0] + self.size[0] - 5, self.pos[1] + self.size[1] - 5), 5)
            pygame.draw.line(self.window, colors[self.__color], (self.pos[0] + self.size[0] - 5, self.pos[1] + 5),
                             (self.pos[0] + 5, self.pos[1] + self.size[1] - 5), 5)
        
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            borders = (self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1])
            if borders[0] <= event.pos[0] <= borders[2] and borders[1] <= event.pos[1] <= borders[3]:
                self.__checked = not self.__checked
            
        
class TextBox(GUIElement):
    def __init__(self, window, pos, size, prompt_text=''):
        GUIElement.__init__(self, window, pos, size)
        self.__prompt_text = prompt_text
        self.__text = ''
        self.__is_active = False
        
    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, value):
        self.__text = value
        
    @property
    def is_active(self):
        return self.__is_active
    
    @is_active.setter
    def is_active(self, value):
        self.__is_active = value
    
    def draw(self):
        pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(self.pos, self.size))
        pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect((self.pos[0] + 2, self.pos[1] + 2),\
                                                                   (self.size[0] - 4, self.size[1] - 4)))
        text_size = self.size[1]*4//5
        if len(self.__text) != 0:
            draw_text(self.__text, text_size, colors['black'], self.window,\
                      (self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2))
        else:
            draw_text(self.__prompt_text, text_size, colors['black'], self.window,\
                      (self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2))
            
        
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            borders = (self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1])
            if borders[0] <= event.pos[0] <= borders[2] and borders[1] <= event.pos[1] <= borders[3]:
                self.__is_active = True
        if event.type == KEYDOWN:
            if event.unicode in string.ascii_letters + string.digits and len(self.__text) < 16:
                self.__text += event.unicode
            if event.key == K_BACKSPACE and len(self.__text) > 0:
                self.__text = self.__text[:-1]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        