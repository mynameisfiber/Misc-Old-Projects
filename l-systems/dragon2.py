#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Dragon Curve
#	variables : L R
#	constants : + −
#	start  : R
#	rules  : (R → R+L), (L → R−L) 

import turtle, pytools

set = "R"
rules = {"R":"R+L","L":"R-L"}
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
  if move in ("L","R"): 
    turtle.forward(5)
  elif move is "-": 
    turtle.right(90)
  elif move is "+": 
    turtle.left(90)
  progress.progress()
input ()
