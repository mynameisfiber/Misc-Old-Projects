#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Peano Gosper Curve
#	variables : X Y
#	constants : F + −
#	start  : FX
#	rules  : (X → X+YF++YF-FX--FXFX-YF+)
#          (Y → -FX+YFYF++YF+FX--FX-Y)
#	angle  : 60°

import turtle, pytools

set = "FX"
rules = {"X":"X+YF++YF-FX--FXFX-YF+", \
         "Y":"-FX+YFYF++YF+FX--FX-Y"}
for n in range(4):
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
    turtle.left(60)
  elif move is "+": 
    turtle.right(60)
  progress.progress()
input ()
