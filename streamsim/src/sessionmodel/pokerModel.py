#!/usr/bin/env python

import random
import sys

import sessionModel
import session

class pokerModel (sessionModel.sessionModel):
    """poker model is a model for mapping demand to a session
    where that session is a single table for online poker"""

    def __init__(self):
        """Initialise the poker model"""
        self.spacesessions=[]  #rooms with space (numers)
        self.waitqueue= [] #waiting players
        self.sessionmap= {} # map of room numbers to sessions
        self.roomNo=1
        self.usermap={}  # Map of users to room numbers

    def addToSpaceSession(self,u):
        """Add user to a room with space"""

        spos= random.randrange(len(self.spacesessions))
        sno= self.spacesessions[spos]
        sess=self.sessionmap[sno]
        sess.addUser(u)
        self.usermap[u]= sno
        #print "Room",sno,"now got",sess.noUsers()
        if (sess.noUsers() < self.maxRoom):
            return
        # is room full
        # If full then remove from spacerooms and add to full rooms
        #print "room",sno,"now full"
        self.spacesessions.pop(spos)


    def addToWaitQueue(self,u):
        """Add a user to queue for a room"""
        self.waitqueue.append(u)

        #Can the waiting queue now form a room
        if len(self.waitqueue) < self.minRoom:
            return

        #waiting queue forms room
        newroom= self.roomNo
        self.roomNo+= 1
        #print "new room",newroom
        sess= session.session(newroom)
        for w in self.waitqueue:
            self.usermap[w]= newroom
            sess.addUser(w)
        self.sessionmap[newroom]=sess
        self.waitqueue= []


        #Will the newly formed room be full
        if self.minRoom < self.maxRoom:
            self.spacesessions.append(newroom)

    def addUser(self,u):
        """User arrives in stream"""

        #tot= 0
        #for (_,sess) in self.sessionmap.items():
        #    tot+= sess.noUsers()
        #print "total users in system ",len(self.usermap), " or ", tot
        if len(self.spacesessions) > 0:
            self.addToSpaceSession(u)
        else:
            self.addToWaitQueue(u)


    def flushWaitQueue(self):
        """If there is space in rooms remove users from wait queue"""
        if len(self.waitqueue) == 0:
            return
        if len(self.spacesessions) == 0:
            return
        u= self.waitqueue.pop()
        self.addToSpaceSession(u)
        self.flushWaitQueue()





    def removeUser(self,u):
        """User removed from stream"""
        #print "Removing user ",u,"user map",self.usermap
        try:
            rno= self.usermap.pop(u)
        except KeyError:
            #was user in waiting queue -- if so just remove them
            self.waitqueue.remove(u)
            return
        sess= self.sessionmap.get(rno)
        #remove user from room
        #print "Room ",rno," Had ",sess.noUsers(),
        sess.delUser(u)
        #print  "After ",sess.noUsers()
        #If room was full declare it now has space
        if sess.noUsers() == self.maxRoom -1:

            self.spacesessions.append(rno)
            self.flushWaitQueue()

        if (sess.noUsers() >= self.minRoom):
            return

        # room is closing
        #print "removing users from emptying room"
        self.sessionmap.pop(rno)
        self.spacesessions.remove(rno)
        for u in sess.getUsers():
            self.usermap.pop(u)
            self.addUser(u)

    def getSessions(self):
        """ Return a list where each element is a list of users
        in the same room"""
        sessions= self.sessionmap.values()
        return sessions

    def parseJSON(self,js,fName):
        """ parse the JSON in file fName"""
        try:
            self.minRoom= js.pop('min_room')
            self.maxRoom= js.pop('max_room')
        except:
            print >> sys.stderr, "JSON ",fName," must contain" \
                "min_room and max_room"
            raise ValueError
