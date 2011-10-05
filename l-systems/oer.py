#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# OER
#	variables : f
#	constants : F + −
#	start  : F+F+F+F
#	rules  : (F → F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF)
#          (Y → -ffffff)
#	angle  : 60°

import turtle, pytools

set = "FX"
rules = {"F":"F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF", \
         "f":"ffffff"}
for n in range(3):
  newset = ""
  for item in set:
    if item in rules:
      newset += rules[item]
    else:
      newset += item
  set = newset

set = set + "+" + set + "+" + set + "+" + set

turtle.speed(0)
turtle.down()
progress = pytools.ProgressBar("Rendering",len(set))
progress.draw()
for i,move in enumerate(set):
  if move is "F": 
    turtle.forward(4)
  elif move is "f":
    turtle.up()
    turtle.forward(5)
    turtle.down()
  elif move is "-": 
    turtle.left(91)
  elif move is "+": 
    turtle.right(91)
  progress.progress()
input ()
