#!/usr/bin/python

import pygame
from pygame.locals import *

class PyGameHelper:
  def __init__(self,resolution,fps=30,background=(255,255,255),sounds=True):
    pygame.init()
    
    self.canvas = pygame.display.set_mode(resolution)
    self.resolution = resolution
    self.background = background
    
    self.setfps(fps)
    self.clock = pygame.time.Clock()
    
    pygame.font.init()
    
    if sounds:
      self.soundenabled = True
      pygame.mixer.init(44100,16,2,512)
      if type(sounds).__name__ == "dict":
        self.sounds = self.preloadsounds(sounds)
    else:
      self.soundenabled = False
    
    self.run()
    
  def run(self):
    startframe = endframe = 0
    while True:
      #Prep Canvas
      self.canvas.fill(self.background)
      #Update Variables & Draw
      self.update()
      self.draw()
      self.events()
      #Refresh Screen
      pygame.display.flip()
      #Check FPS
      actualmspf = self.clock.tick(self.fps)
      if actualmspf < self.mspf:
        print "We are working slower than given FPS (@%ffps)"%(1000.0/actualmspf)
        
  def text(self,string,pos,size=24,color=(0,0,0)):
    font = pygame.font.Font(None,size)
    text = font.render(string,1,color)
    textpos = text.get_rect()
    if type(pos).__name__ == "str":
      if pos == "center":
        textpos.center = (self.resolution[0]/2,self.resolution[1]/2)
      else:
        if pos.count("top-"):
          textpos.top = 0
        elif pos.count("middle-"):
          textpos.centery = self.resolution[1]/2
        elif pos.count("bottom-"):
          textpos.bottom = self.resolution[1]
        if pos.count("-left"):
          textpos.left = 0
        elif pos.count("-middle"):
          textpos.centerx = self.resolution[0]/2
        elif pos.count("-right"):
          textpos.right = self.resolution[0]
    else:
      textpos.center = pos
    self.canvas.blit(text, textpos)
    return (text, textpos)
        
  def setfps(self,fps):
    self.fps = fps
    self.mspf = 1000.0/fps
    
  def preloadsounds(self, sounds):
    loadedsounds = {}
    for name in sounds:
      loadedsounds.update({name:pygame.mixer.Sound(sounds[name])})
    return loadedsounds
    
  def playsound(self,item):
    if item in self.sounds:
      self.sounds[item].play()
        
  def events(self):
    for event in pygame.event.get():
      if event.type == KEYUP:
        self.keyup(event)
      elif event.type == KEYDOWN:
        self.keydown(event)
      elif event.type == MOUSEMOTION:
        self.mousemove(event)
      elif event.type == QUIT:
        self.quit()
        
  def quit(self):
    print "Exiting"
    pygame.font.quit()
    if self.soundenabled:
      pygame.mixer.quit()
    pygame.quit()
    exit()
    
  def mousemove(self,event):
    pass
        
  def keyup(self,event):
    pass
  
  def keydown(self,event):
    pass
      
  def update(self):
    pass
  
  def draw(self):
    pass
