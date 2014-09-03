'''
Created on 14 Dec 2013

'''

import outputModel, sys

class outputCost(outputModel.outputModel):
    ''' Class outputs basic cost information '''

    def __init__(self):
        '''
        Constructor for cost model
        '''        
        self.fileName= None
        self.fptr= None
        self.totCost= 0.0
        self.day=1
        self.inCost= 0.0
        self.betweenCost= 0.0
        self.outCost= 0.0
        self.cpuCost= 0.0

    def parseJSON(self,js,fName):
        '''
        Parse extra JSON for this class
        '''
        super(outputCost,self).parseJSON(js,fName)

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
        if self.fileName != None:
            try:
                self.fptr= open(self.fileName,"w")
            except IOError:
                print >> sys.stderr, "Cannot open",self.fileName," to write"
                sys.exit()
            print >> self.fptr, "#Day cost_in cost_between cost_out cost_cpu tot"
        else:
            self.fptr= sys.stdout



    def simEndUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called at the end of the simulation
        '''
        self.simUpdate(sessions, qoe, cost, time, lastTime, day+1)
        if self.fileName != None:
            self.fptr.close()


    def simUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called every time the simulation updates
        '''
        
        # Add costs for all sessions
        for c in cost:
            self.inCost+= c[0]
            self.betweenCost+= c[1]
            self.outCost+= c[2]
            self.cpuCost+= c[3]
        
        
        
        

    def simDayUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called once per simulated day
        '''
        print >> self.fptr, day, self.inCost, self.betweenCost, \
            self.outCost, self.cpuCost, self.inCost+self.betweenCost+ \
                self.outCost+ self.cpuCost
        self.inCost= 0
        self.betweenCost=0
        self.outCost= 0
        self.cpuCost=0
