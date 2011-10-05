#!/usr/bin/python

from PyGameHelper import PyGameHelper
import pygame
import numpy
from numpy import arange as range

class Player:
  def __init__(self,score=0,lives=3):
    self.score = score
    self.lives = lives
    self.multiplyer = 1
    
  def todict(self):
    return {"score":self.score, "lives":self.lives, "livesstr":"I"*self.lives}


    
class Arknoid(PyGameHelper):
  def __init__(self,resolution,fps=60):
    self.ball = pygame.Rect([resolution[0]*.5,resolution[1]*.6,5.0,5.0])
    self.dball = numpy.array((2,2.75))
    self.paddle = pygame.Rect((resolution[0]*.5,resolution[1]*.9,resolution[0]*.25,resolution[1]*.01))
    self.paddley = resolution[1]*.9
    self.bricks = self.createlevel(resolution)
    self.hud = [("Score: %(score)0.10d","top-right"),("Lives: %(livesstr)s","top-left")]
    self.player = Player(score=0, lives=3)
    
    self.togglesound = False
    PyGameHelper.__init__(self,resolution,fps, sounds={"blip":"data/blip.wav", "bang":"data/bang.wav"})
      
  def createlevel(self,resolution,w=50,h=10,b=5):
    bricks = []
    for x in range(resolution[0]*.2,resolution[0]*.8,w+b):
      for y in range(resolution[1]*.2, resolution[1]*.4,h+b): 
        bricks.append(pygame.Rect((x,y,w,h)))
    return bricks
        
  def mousemove(self,event):
    self.paddle.center = (event.pos[0], self.paddley)

  def keydown(self, event):
    if event.key == pygame.K_UP:
      self.dball[1] -= .5
    elif event.key == pygame.K_DOWN:
      self.dball[1] += .5
    elif event.key == pygame.K_LEFT:
      self.dball[0] -= .5
    elif event.key == pygame.K_RIGHT:
      self.dball[0] += .5
    elif event.key == pygame.K_m:
      self.togglesound = not self.togglesound
      print "Sound is " + ("ON" if self.togglesound else "OFF")
    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
      self.quit()

  def draw(self):
    [self.text(item[0]%self.player.todict(),item[1]) for item in self.hud]
    if self.player.multiplyer > 2: self.text("!!MULTIPLYER @ %dX!!"%self.player.multiplyer,"top-middle",24)
    pygame.draw.rect(self.canvas, (100,100,100), self.ball)
    pygame.draw.rect(self.canvas, (50,50,50), self.paddle)
    [pygame.draw.rect(self.canvas, (125,125,125), x) for x in self.bricks]
    
  def update(self):
    resolution = self.canvas.get_size()
    sound = None
    if not 0 < self.ball.left+self.dball[0] < resolution[0]-self.ball.w:
      self.dball[0] *= -1
      sound = "blip"
    elif 0 > self.ball.top+self.dball[1]:
      self.dball[1] *= -1
      sound = "blip"
    elif self.ball.top + self.dball[1] > self.paddle.bottom + self.paddle.h:
      print "You Lose"
      self.quit()    
    elif self.paddle.colliderect(self.ball):
      sound = "blip"
      self.player.multiplyer = 1
      self.dball += .5 * abs(self.dball) / self.dball
      self.dball[0] += (2.95*(self.ball.centerx - self.paddle.centerx)/self.paddle.w)**3
      self.dball[1] *= -1
    else:
      cid = self.ball.move(self.dball).collidelist(self.bricks)
      if cid != -1:
        if self.player.score % 1000 == 0 :
          self.paddle.width -= self.paddle.width*0.05
        cbrick = self.bricks[cid]
        self.player.score += 100*self.player.multiplyer
        self.player.multiplyer += 1
        sound = "bang"
        if (cbrick.top < self.ball.bottom or cbrick.bottom > self.ball.top) and not (cbrick.left < self.ball.right and cbrick.right > self.ball.left):
          self.dball[0] *= -1
        else:
          self.dball[1] *= -1
        self.bricks.pop(cid)
    if self.togglesound: self.playsound(sound)
    self.ball.move_ip(self.dball)
    
    
if __name__ == "__main__":
  Arknoid((1024,768))
