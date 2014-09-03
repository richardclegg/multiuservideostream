'''
Created on 24 Nov 2013

'''

import outputModel, sys

class basicDaily(outputModel.outputModel):
    '''
    Class outputs simplest results for a really very basic model
    '''



    def __init__(self):
        '''
        Constructor for
        '''
        self.fileName= None
        self.totUsers= 0
        self.lastUsers= 0
        self.total= 0
        self.outType= 0

    def parseJSON(self,js,fName):
        '''
        Parse extra JSON for this class
        '''
            
        super(basicDaily,self).parseJSON(js,fName)

    def userArrive(self,time):
        '''
        Arrival of user
        '''
        self.totUsers+= 1

    def userDepart(self,time):
        '''
        Departure of user
        '''

    def simStartUpdate(self):
        '''
            Called at the start of the simulation
        '''
        if self.fileName != None:
            try:
                self.fptr= open(self.fileName,"w")
            except IOError:
                print >> sys.stderr, "Cannot open",self.fileName," to write"
                sys.exit()
            print >> self.fptr, "#Day tot_users day_users"
        else:
            self.fptr= sys.stdout



    def simEndUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called at the end of the simulation
        '''
        if self.fileName != None:
            self.fptr.close()


    def simUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called at the end of the simulation
        '''

    def simDayUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called once per simulated day
        '''
        print >> self.fptr,day,self.totUsers, self.totUsers - self.lastUsers
        self.lastUsers= self.totUsers
