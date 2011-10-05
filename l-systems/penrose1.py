#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Penrose Tiling P3
#	variables:  F 6 7 8 9 [ ]
#	constants:    + −
#	start:  [7]++[7]++[7]++[7]++[7]
#	rules:  6 → 88F++9F----7F[-8F----6F]++
#	        7 → ++8F--9F[---6F--7F]+   
#	        8 → −-6F++7F[+++8F++9F]-   
#	        9 → −--8F++++6F[+9F++++7F]--7F
#	        F → (eliminated at each iteration)
#	angle:  36º

import turtle, Queue, pytools

set = "[7]++[7]++[7]++[7]++[7]"
rules = {"6":"8F++9F----7F[-8F----6F]++", \
         "7":"+8F--9F[---6F--7F]+", \
         "8":"-6F++7F[+++8F++9F]-", \
         "9":"--8F++++6F[+9F++++7F]--7F", \
         "F":""}
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
    turtle.forward(10)
  elif move is "+": 
    turtle.left(36)
  elif move is "-": 
    turtle.right(36)
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
