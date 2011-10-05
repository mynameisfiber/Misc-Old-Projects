#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Sierpinski Triangle
#	variables : F G
#	constants : + −
#	start  : F−G−G
#	rules  : (F → F−G+F+G−F), (G → GG)
#	angle  : 120° 

import turtle, pytools

set = "F-G-G"
rules = {"F":"F-G+F+G-F","G":"GG"}
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
  if move in ("G","F"): 
    turtle.forward(5)
  elif move is "+": 
    turtle.left(120)
  elif move is "-": 
    turtle.right(120)
  progress.progress()
input ()
