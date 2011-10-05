#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Hilbert Curve
#	variables : X Y
#	constants : F + −
#	start  : X
#	rules  : (X → -YF+XFX+FY-)
#          (Y → +XF-YFY-FX+)
#	angle  : 90°

import turtle, pytools

set = "X"
rules = {"X":"-YF+XFX+FY-", \
         "Y":"+XF-YFY-FX+"}
for n in range(5):
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
