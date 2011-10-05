#!/usr/bin/python

from PyGameHelper import PyGameHelper
import pygame
import numpy

class Square(PyGameHelper):
  def __init__(self,resolution,fps):
    self.coor = numpy.array([50.0,50.0,100.0,100.0])
    self.dcoor = numpy.array([0.1,1.0])
    
    #Set buffer to zero so sound starts right away
    pygame.mixer.init(22050,16,2,0)
    self.sounds = self.preloadsounds({"blip":"data/blip.wav"})
    
    PyGameHelper.__init__(self,resolution,fps)
    
  def preloadsounds(self, sounds):
    loadedsounds = {}
    for name in sounds:
      loadedsounds.update({name:pygame.mixer.Sound(sounds[name])})
    return loadedsounds
    
  def sound(self,item):
    if item in self.sounds:
      self.sounds[item].play()

  def keydown(self, event):
    if event.key == pygame.K_UP:
      self.dcoor[1] -= .5
    elif event.key == pygame.K_DOWN:
      self.dcoor[1] += .5
    elif event.key == pygame.K_LEFT:
      self.dcoor[0] -= .5
    elif event.key == pygame.K_RIGHT:
      self.dcoor[0] += .5
    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
      self.quit()
    print self.dcoor

  def draw(self):
    pygame.draw.rect(self.canvas, (100,100,100), self.coor)
    
  def update(self):
    resolution = self.canvas.get_size()
    self.background = (255,255,255)
    if not 0 < self.coor[0]+self.dcoor[0] < resolution[0]-self.coor[2]:
      self.dcoor[0] *= -1
      self.sound("blip")
    elif not 0 < self.coor[1]+self.dcoor[1] < resolution[1]-self.coor[3]:
      self.dcoor[1] *= -1
      self.sound("blip")
    self.coor[0:2] += self.dcoor
    
if __name__ == "__main__":
  Square((800,600),30)
