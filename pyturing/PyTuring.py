#!/usr/bin/python

class PyTuring:
  def __init__(self,tape,delta,state="q0",index=0,deltaargs=[]):
    self.tape = tape
    self.delta = delta
    self.deltaargs = deltaargs
    self.index = index
    self.state = state

  def readChar(self,index=None):
    index = index if index else self.index
    return self.tape[self.index] if len(self.tape)>index else '_'

  def writeChar(self, char, index=None):
    assert(len(char) == 1)
    index = index if index else self.index
    #hax because strings are immutable
    tmptape = list(self.tape)
    tmptape[index] = char
    self.tape = ''.join(tmptape)

  def move(self, direction, amount=1):
    self.index += amount * (1 if direction == "R" else -1)
    if self.index < 0:
      self.index = 0
    while self.index >= len(self.tape):
      self.tape += "_"

  def step(self,delta=None):
    delta = delta if delta else self.delta #Line added to aid in overloading transition function
    try:
      self.state, wchar, move = delta(self.state, self.readChar(),*self.deltaargs)
    except IndexError:
      raise Exception("Invalid Character at control head: %s"%self.readChar())
    self.writeChar(wchar)
    self.move(move)
    #The following trims excess null spaces
    self.tape = self.tape[:self.index+1] + self.tape[self.index+1:].rstrip("_")

  def __iter__(self):
    while not self.state in ("qA","qR"):
      yield self
      self.step()
    yield self

  def __str__(self):
    return "%s %s %s"%(self.tape[:self.index],self.state,self.tape[self.index:])

if __name__ == "__main__":
  tape = "abac"
  def delta(state, char):
    transition = [[("qaf","X","R"),("qbf","X","R"),("qaf","X","R"),("qR","X","R"),("qA","_","L")],
                  [("qaf","a","R"),("qaf","b","R"),("qaf","c","R"),("qR","X","R"),("qwa","_","L")],
                  [("qbf","a","R"),("qbf","b","R"),("qbf","c","R"),("qR","X","R"),("qwb","_","L")],
                  [("qcf","a","R"),("qcf","b","R"),("qcf","c","R"),("qR","X","R"),("qwb","_","L")],
                  [("qab","a","L"),("qbb","a","L"),("qcb","a","L"),("qR","X","R"),("qR","_","L")],
                  [("qab","b","L"),("qbb","b","L"),("qcb","b","L"),("qR","X","R"),("qR","_","L")],
                  [("qab","c","L"),("qbb","c","L"),("qcb","c","L"),("qR","X","R"),("qR","_","L")],
                  [("qab","a","L"),("qab","b","L"),("qab","c","L"),("qA","a","L"),("qR","_","L")],
                  [("qbb","a","L"),("qbb","b","L"),("qbb","c","L"),("qA","b","L"),("qR","_","L")],
                  [("qcb","a","L"),("qcb","b","L"),("qcb","c","L"),("qA","c","L"),("qR","_","L")]]
    transform = {"q0":0,"qaf":1,"qbf":2,"qcf":3,"qwa":4,"qwb":5,"qwc":6,"qab":7,"qbb":8,"qcb":9,
                 "a":0,"b":1,"c":2,"X":3,"_":4}
    return transition[transform[state]][transform[char]]
#    transition = [ [("q1","a","R") , ("q0","b","R") , ("qR","_","R") , ("qA","_","R")],
#                   [("qa","1","R") , ("qb","1","R") , ("qR","1","R") , ("qA","a","R")],
#                   [("qa","a","R") , ("qb","a","R") , ("qR","a","R") , ("q2","a","L")],
#                   [("qa","b","R") , ("qb","b","R") , ("qR","b","R") , ("q2","b","L")],
#                   [("q2","a","L") , ("q2","b","L") , ("q0","a","R") , ("qR", "_","R")] ]
#    transform = {"a":0,"b":1,"1":2,"_":3, "q0":0, "q1":1, "qa":2, "qb":3, "q2":4}
#    return transition[transform[state]][transform[char]]
  M = PyTuring(tape, delta)
  for state in M:
    print state

