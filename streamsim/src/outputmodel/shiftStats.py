'''
Created on 14 Dec 2013

'''
import outputModel, sys, math


class shiftStats(outputModel.outputModel):
    ''' Class for output related to how many times new servers picked'''    
    
    DAILY=1
    END=2
    
    def __init__(self):
        '''
        Constructor for shiftStats
        '''
        self.fileName= None
        self.outputTime= shiftStats.END
        self.lastTime= 0.0
        self.initVars()
        
    def initVars(self):
        '''blank variables which track stats'''
        self.changes= 0
        self.sessionMap= {}


    def parseJSON(self,js,fName):
        '''
        Parse extra JSON for this class
        '''
        try:
            outType= js.pop("time")
            if outType == 'daily':
                self.outputTime=shiftStats.DAILY
            elif outType == 'end':
                self.outputTime= shiftStats.END
            else:
                print >> sys.stderr, 'JSON for shiftStats can only' \
                    'take daily|end for key "time" in',fName
                sys.exit()
        except KeyError:
            pass
        super(shiftStats,self).parseJSON(js,fName)

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
            print >> self.fptr, "#day no_sessions changes"
        else:
            self.fptr= sys.stdout



    def simEndUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called at the end of the simulation
        '''
        if self.outputTime == shiftStats.END:
            self.updateInfo(time,sessions, True)
            self.printOutput(day, time)
        
        if self.fileName != None:
            self.fptr.close()


    def simUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called at the end of the simulation
        '''
        self.updateInfo(time,sessions, False)
    
    def updateInfo(self,time,sessions, purgeall):
        #Register new sessions
        for s in sessions:
            try: 
                dc= self.sessionMap[s.sessionNo]
                # Check if data centres are exactly the same
                if dc != s.datacentres:
                    # check if they are reordering
                    if set(dc) != set(s.datacentres):
                        self.changes+= 1
                    self.sessionMap[s.sessionNo]= s.datacentres
            except KeyError:
                self.sessionMap[s.sessionNo]= s.datacentres
        
        

    def simDayUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called once per simulated day
        '''
        if self.outputTime == shiftStats.DAILY:
            self.updateInfo(time,sessions, True)
            self.printOutput(day)
            
    def printOutput(self,day):
        '''
            Actually do the output
        '''
        print >> self.fptr, day,len(self.sessionMap),self.changes
        self.initVars()
        
