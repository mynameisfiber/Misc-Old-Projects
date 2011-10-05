#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Plant 2
#	variables : F
#	constants : + −
#	start  : F
#	rules  : (F → FF-[-F+F+F]+[+F-F-F])
#	angle  : 25° 

import turtle, Queue, pytools

set = "F"
rules = {"F":"FF-[-F+F+F]+[+F-F-F]"}
for n in range(4):
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
  elif move is "-": 
    turtle.left(22.5)
  elif move is "+": 
    turtle.right(22.5)
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
