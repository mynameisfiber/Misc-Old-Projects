#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Sierpinski Carpet
#	variables : F
#	constants : +
#	start  : F+F+F+F
#	rules  : (F → FF+F+F+F+FF)
#	angle  : 90° 

import turtle, pytools

set = "F+F+F+F"
rules = {"F":"FF+F+F+F+FF"}
for n in range(3):
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
  if move in ("G","F"): 
    turtle.forward(5)
  elif move is "+": 
    turtle.left(90)
  progress.progress()
input ()
