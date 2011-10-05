#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Dragon Curve
#	variables : X Y
#	constants : F + −
#	start  : FX
#	rules  : (X → X+YF), (Y → FX-Y)
#	angle  : 90°

import turtle, pytools

set = "FX"
rules = {"X":"X+YF","Y":"FX-Y"}
for n in range(10):
  newset = ""
  for item in set:
    if item in rules:
      newset += rules[item]
    else:
      newset += item
  set = newset

turtle.speed(0)
turtle.down()
progress = pytools.ProgressBar("Rendering",len(set))
progress.draw()
for i,move in enumerate(set):
  if move is "F": 
    turtle.forward(5)
  elif move is "-": 
    turtle.left(90)
  elif move is "+": 
    turtle.right(90)
  progress.progress()
input ()
