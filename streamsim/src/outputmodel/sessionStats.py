'''
Created on 14 Dec 2013

'''
import outputModel, sys, math


class sessionStats(outputModel.outputModel):
    ''' Class for output related to qos aggregated over session'''    
    
    DAILY=1
    END=2
    
    def __init__(self):
        '''
        Constructor for sessionStats
        '''
        self.fileName= None
        self.outputTime= sessionStats.END
        self.lastTime= 0.0
        self.maxSessNo= 0.0
        self.maxSessUsers= 0.0
        self.sumSessNo= 0.0
        self.sum2SessNo= 0.0
        self.sumSessUsers= 0.0
        self.sum2SessUsers= 0.0
        self.lastCheck= 0


    def parseJSON(self,js,fName):
        '''
        Parse extra JSON for this class
        '''
        try:
            outType= js.pop("time")
            if outType == 'daily':
                self.outputTime=sessionStats.DAILY
            elif outType == 'end':
                self.outputTime= sessionStats.END
            else:
                print >> sys.stderr, 'JSON for sessionStats can only' \
                    'take daily|end for key "time" in',fName
                sys.exit()
        except KeyError:
            pass
        super(sessionStats,self).parseJSON(js,fName)

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
            print >> self.fptr, "#day mean_no_sessions sd_no_sessions max_no_session mean_session_size sd_session_size max_session_size"
        else:
            self.fptr= sys.stdout



    def simEndUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called at the end of the simulation
        '''
        if self.outputTime == sessionStats.END:
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
        #Register that we have spent appropriate times
        #with various session lengths
        sno= len(sessions)
        self.sumSessNo+= sno*(time-self.lastCheck)
        self.sum2SessNo+= sno*sno*(time-self.lastCheck)*(time-self.lastCheck)
        self.maxSessNo= max(self.maxSessNo,sno)
        self.lastCheck= time
        for s in sessions:
            if s.changed == False and purgeall == False:
                continue
            slen= len(s.prevUsers)
            self.maxSessUsers= max(slen,self.maxSessUsers)
            self.sumSessUsers+= slen*(time-s.lastSessionPurgeTime)
            self.sum2SessUsers+= slen*slen*(time-s.lastSessionPurgeTime)*(time-s.lastSessionPurgeTime)
            s.prevUsers= s.users         
            s.lastSessionPurgeTime= time
        

    def simDayUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called once per simulated day
        '''
        if self.outputTime == sessionStats.DAILY:
            self.updateInfo(time,sessions, True)
            self.printOutput(day,time)
            
    def printOutput(self,day,time):
        '''
            Actually do the output
        '''
        td= time-self.lastTime
        
        meanSess= self.sumSessNo/td
        maxSess= self.maxSessNo
        mean2Sess= (self.sum2SessNo)/td
        sdSess= math.sqrt(mean2Sess - meanSess*meanSess)
        meanUsers= (self.sumSessUsers/meanSess)/td
        maxUsers= self.maxSessUsers
        mean2Users= (self.sum2SessUsers/meanSess)/td
        sdUsers= math.sqrt(mean2Users-meanUsers*meanUsers)
        print >> self.fptr, day, meanSess, sdSess, maxSess, meanUsers, \
            sdUsers, maxUsers
        self.lastTime= time
        self.maxSessNo= 0.0
        self.maxSessUsers= 0.0
        self.sumSessNo= 0.0
        self.sum2SessNo= 0.0
        self.sumSessUsers= 0.0
        self.sum2SessUsers= 0.0
        
