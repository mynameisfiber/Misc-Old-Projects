#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Plant 1
#	variables : X F
#	constants : + −
#	start  : X
#	rules  : (X → F-[[X]+X]+F[+FX]-X), (F → FF)
#	angle  : 25° 

import turtle, Queue, pytools, random

set = "F"
rules = {"F":"GF-F+F+F-FG","-":"G+G+G+G","+":""}
angle=90
for n in range(5):
  newset = ""
  for item in set:
    if item in rules:
      newset += rules[item]
    else:
      newset += item
  set = newset

state = Queue.LifoQueue()
turtle.speed(0)
turtle.down()
progress = pytools.ProgressBar("Rendering",len(set))
progress.draw()
for i,move in enumerate(set):
  if move is "F": 
    turtle.forward(5)
  elif move is "f":
    turtle.up()
    turtle.forward(5)
    turtle.down()
  elif move is "-": 
    turtle.left(angle)
  elif move is "+": 
    turtle.right(angle)
  elif move is "R":
    turtle.left(random.randint(-5,5))
  elif move is "[":
    state.put([turtle.pos(),turtle.heading()])
  elif move is "]":
    turtle.up()
    savedstate = state.get()
    turtle.setpos(savedstate[0])
    turtle.seth(savedstate[1])
    turtle.down()
  progress.progress()
input ()
