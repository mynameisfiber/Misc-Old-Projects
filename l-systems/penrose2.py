#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made by Michael Gorelick (mynameisfiber@gmail.com)
# Copyleft 2009

# Penrose Tiling
#	variables:  W X Y Z F
#	constants:    + −
#	start:  ++ZF----XF-YF----WF
#	rules:  W → YF++ZF----XF[-YF----WF]++
#	        X → +YF--ZF[---WF--XF]+
#	        Y → -WF++XF[+++YF++ZF]-
#	        Z → --YF++++WF[+ZF++++XF]--XF
#	        1 → (eliminated at each iteration)
#	angle:  36º

import turtle, Queue, pytools

set = "++ZF----XF-YF----WF"
rules = {"W":"YF++ZF----XF[-YF----WF]++", \
         "X":"+YF--ZF[---WF--XF]+", \
         "Y":"-WF++XF[+++YF++ZF]-", \
         "Z":"--YF++++WF[+ZF++++XF]--XF", \
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
