#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Sierpinski Triangle
#	variables : A B
#	constants : + −
#	start  : A
#	rules  : (A → B−A−B), (B → A+B+A)
#	angle  : 60° 
#	NOTE: The angle changes sign at each iteration
#	      so that the base of the triangular shapes
#	      are always in the bottom. =/_ represent
#       negative angles of +/-

import turtle, pytools

set = "A"
rules = {"A":["B-A-B","B_A_B"],"B":["A+B+A","A=B=A"], \
         "=":"+","+":"=","-":"_","_":"-"}
for n in range(9):
  newset = ""
  for item in set:
    if item in rules:
      if len(rules[item]) > 1:
        newset += rules[item][n%2]
      else:
        newset += rules[item]
    else:
      newset += item
  set = newset

turtle.speed(0)
turtle.down()
progress = pytools.ProgressBar("Rendering",len(set))
progress.draw()
for i,move in enumerate(set):
  if move in ("A","B"): 
    turtle.forward(5)
  elif move is "+": 
    turtle.left(60)
  elif move is "-": 
    turtle.right(60)
  elif move is "=": 
    turtle.left(-60)
  elif move is "_": 
    turtle.right(-60)
  progress.progress()
input ()
