'''
Created on 24 Nov 2013

'''

import sys

class outputModel(object):
    '''
    This model describes output -- it is a virtual module which should never be implemented
    '''


    def __init__(self):
        '''
        Constructor for generic output model
        '''
        print >> sys.stderr, "This generic class should never be constructed"
        sys.exit()

    def parseJSON(self,js,fName):
        '''
        Parse extra JSON for this class
        '''
        try:
            fname= js.pop("file")
            self.fileName= fname
        except KeyError:
            pass

    def userArrive(self,time):
        '''
        Arrival of user
        '''

    def userDepart(self,time):
        '''
        Departure of user
        '''

    def simStartUpdate(self):
        '''
            Called at the start of the simulation
        '''

    def simEndUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called at the end of the simulation
        '''

    def simUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called at the end of the simulation
        '''

    def simDayUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called once per simulated day
        '''
