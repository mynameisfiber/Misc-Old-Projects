#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Gorelick Squares
#	variables : F G
#	constants : + −
#	start  : F
#	rules  : (F → GF+F-F-F+FG), (G → Eliminated at each iteration)
#	angle  : 90° 

import turtle, pytools

set = "F"
rules = {"F":"GF+F-F-F+FG"}#, "G":""}
angle = 90
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
  if move in ("G","F"): 
    turtle.forward(5)
  elif move is "+": 
    turtle.left(angle)
  elif move is "-": 
    turtle.right(angle)
  progress.progress()
input ()
