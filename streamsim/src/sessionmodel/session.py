'''
Created on 27 Oct 2013

@author: Richard G. Clegg richard@richardclegg.org
'''

class session(object):
    '''
    This class represents a session -- a group of users communicating using a video chat room
    '''


    def __init__(self, sessno):
        '''
        Constructor
        '''
        self.sessionNo= sessno
        self.datacentres = []
        self.users=[]
        self.routes=[]
        self.changed=True
        self.cachedQoe=[]
        self.cachedCost=None
        self.prevQoe= []
        self.lastPurgeTime= 0
        self.prevUsers= []
        self.lastSessionPurgeTime= 0

    def __eq__(self, other):
        ''' for simplicity define session equality in terms of session no only'''
        if isinstance(other, self.__class__):
            return self.sessionNo == self.sessionNo
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def addUser(self,user):
        '''Add a user to the session'''
        self.users.append(user)
        self.changed= True

    def delUser(self,user):
        self.users.remove(user)
        self.changed= True

    def setDataCentres (self,dc):
        if dc != self.datacentres:
            self.changed= True
        else:
            self.datacentres= dc

    def addRoute(self, r):
        self.routes.append(r);
        
    def getRoutes(self):
        return self.routes
        
    def setCosts(self,cost):
        self.cachedCost= cost
    
    def getCosts(self):
        if self.changed:
            return None
        return self.cachedCost

    def getUsers(self):
        return self.users

    def noUsers(self):
        return len(self.users)
