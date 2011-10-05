#!/usr/bin/python
# Copyleft Michael G.
from __future__ import division

'''A tool to allow for remote control of a machine with twitter'''

__author__ = 'Michael G <mynameisfiber@gmail.com>'
__version__ = '0.1'

from sys import stdout
import threading, time, twitter, re, ConfigParser, subprocess

configfile = 'twitcontrol.conf'

class TwitThread(threading.Thread):
  def __init__(self,actions,twitter,command):
    threading.Thread.__init__(self)
    self._stop = threading.Event()  #Set the hook for self.stop()
    self.actions = actions
    self.twitter = twitter
    self.commandstruct = command
    self.process = None

  def run(self):
    '''Finds what action is linked to the inputed command'''
    command = self.commandstruct['text']
    for name,contents in self.actions.iteritems():
      found = contents['match'].match(command)
      if found:
        self.name = name
        print "%s: %s: Starting"%(time.ctime(),name)
        self.doCommand(found,command,contents)
        return None
      elif command.lower() == "stop %s"%name.lower():
        self.name = "killthread-%s"%name
        for thread in threading.enumerate():
          if thread.name.lower() == name.lower():
            print "%s: Killing %s"%(time.ctime(),name)
            thread.stop()
        return None

  def doCommand(self,match,command,action):
    '''Runs the command given by the config file for the given input'''
    if action["output"] == "start":
      self.message("%s: Started"%self.name)
    print "Running command: %s"%(action["command"]%match.groupdict())
    self.process = subprocess.Popen(action["command"]%match.groupdict(),\
      stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #We use the following hack because Popen.wait() or Popen.interact() lock
    #the process so we cannot kill it if another thread sends a self.stop()
    while self.process.poll() == None:
      time.sleep(1)
    if action["output"] == "end":
      self.message("%s: Done"%self.name)
    if self.process.returncode != 0:
      err = self.formatstd(self.process.stderr)
      print "%s: %s: Error: %s"%(time.ctime(),self.name,err)
      if action["output"] == "output":
        self.message("%s: Error: %s"%(self.name,err))
    else:
      suc = self.formatstd(self.process.stdout)
      print "%s: %s: Success: %s"%(time.ctime(),self.name,suc)
      if action["output"] == "output":
        self.message("%s: Success: %s"%(self.name,suc))

  def formatstd(self,fd,maxsize=120):
    '''Extracts and formats data from a datastream'''
    return ", ".join([x.strip() for x in fd.readlines()])[:maxsize]

  def message(self,msg):
    '''Sends a tweet to the command sender truncated to 140 characters'''
    self.twitter.PostDirectMessage(self.commandstruct['sender_id'],msg[:140])

  def stop(self):
    '''Stops the current thread and terminates any open processes'''
    print "%s: %s: Thread Killed"%(time.ctime(),self.name)
    self.process.terminate()
    self._stop.set()

  def stopped(self):
    return self._stop.isSet()


class TwitControl:
  def __init__(self,actions,user,passwd,recieveID,timeout=5):
    self.actions = actions
    self.twitter = twitter.Api(username=user,password=passwd)
    self.recieveID = recieveID
    self.timeout = timeout
    self.twitter.SetCache(None)

  def getMessages(self):
    '''Gets all directed messages from twitter from a given user'''
    return [x.AsDict() for x in self.twitter.GetDirectMessages() \
    if x.GetSenderId() == self.recieveID]

  def start(self):
    '''Checks for new messages and commands the threads'''
    commands = self.getMessages()
    commandid = commands[0]['id']
    while True:
      commands = self.getMessages()
      if commands[0]['id'] != commandid:
        for command in commands:
          if command['id'] == commandid:
            break
          print "%s: MASTER: Found Command: %s"%(time.ctime(),command['text'])
          TwitThread(self.actions,self.twitter,command).start()
        commandid = commands[0]['id']
      time.sleep(self.timeout)

if __name__ == '__main__':
  configfd = ConfigParser.RawConfigParser()
  configfd.read(configfile)
  print "Reading config: %s" % configfile

  username  = configfd.get('Connection', 'username')
  password  = configfd.get('Connection', 'password')
  recieveID = configfd.getint('Connection', 'recieveID')
  if configfd.has_option('Connection', 'timeout'):
    timeout = configfd.getint('Connection', 'timeout')
  else:
    timeout = 5

  actions = {}
  for section in configfd.sections():
    if section == 'Connection':
      continue
    action = {}
    action['match']   = re.compile(configfd.get(section,'match'))
    action['command'] = configfd.get(section,'command')
    action['output']  = configfd.get(section,'output')
    actions.update({section:action})
  print "Loaded modules: %s"%", ".join(actions.keys())

  print "Listening to user: %s"%username
  control = TwitControl(actions,username,password,recieveID,timeout)
  control.start()
