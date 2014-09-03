'''
Created on 14 Dec 2013

'''
import outputModel, sys, math


class qosPdf(outputModel.outputModel):
    ''' Class for output related to qos aggregated over session'''    
    
    BASIC= 1
    QUINTILE= 2
    DECILE= 3
    PDF= 4
    
    DAILY=1
    END=2
    
    def __init__(self):
        '''
        Constructor for qosPdf
        '''
        self.fileName= None
        self.rttmax=1000000.0 #rtt in micro seconds
        self.granularity=1000
        self.outputTime= qosPdf.END
        self.init_vars()

        
    def init_vars(self):
        
        self.managed= [0.0]*self.granularity
        self.unmanaged= [0.0]*self.granularity
        self.total= 0.0
       
        self.manperc= 0.0


    def parseJSON(self,js,fName):
        '''
        Parse extra JSON for this class
        '''
        try:
            outType= js.pop("style")
        except KeyError:
            print >> sys.stderr, 'JSON for qosPdf must contain' \
                '"style" which is "basic|quintile|decile|pdf" in',fName
            sys.exit()
        if outType == 'basic':
            self.outType= qosPdf.BASIC
        elif outType == 'quintile':
            self.outType= qosPdf.QUINTILE
        elif outType == 'decile':
            self.outType= qosPdf.DECILE
        elif outType == 'pdf':
            self.outType= qosPdf.PDF
        else:
            print >> sys.stderr, 'JSON for qosPdf must contain' \
                '"style" which is "basic|quintile|decile|pdf" in',fName
            sys.exit()
        try:
            outType= js.pop("time")
            if outType == 'daily':
                self.outputTime=qosPdf.DAILY
            elif outType == 'end':
                self.outputTime= qosPdf.END
            else:
                print >> sys.stderr, 'JSON for qosPdf can only' \
                    'take daily|end for key "time" in',fName
                sys.exit()
        except KeyError:
            pass
        super(qosPdf,self).parseJSON(js,fName)

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
            if self.outType == qosPdf.PDF:
                print >> self.fptr,"#Day perc_managed mean_managed std_dev_managed PDF_managed",
                print >> self.fptr,"Day mean_unmanaged std_dev_unmanaged PDF_unmanaged"
            else:
                print >> self.fptr, "#Day perc_managed mean_managed std_dev_managed \
                    mean_unmanaged std_dev_unmanaged",
            if self.outType == qosPdf.BASIC:
                print >> self.fptr
            elif self.outType == qosPdf.QUINTILE:
                print >> self.fptr, "1_q_man 2_q_man 3_q_man 4_q_man 5_q_man", \
                    "1_q_uman 2_q_uman 3_q_uman 4_q_uman 5_q_uman"
            elif self.outType == qosPdf.DECILE:
                for i in range(10):
                    print >> self.fptr, str(i)+"q_man",
                for i in range(10):
                    print >> self.fptr, str(i)+"q_man",
                print >> self.fptr
        else:
            self.fptr= sys.stdout



    def simEndUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called at the end of the simulation
        '''
        if self.outputTime == qosPdf.END:
            self.updateQoe(time,sessions, True)
            self.printOutput(day)
        
        if self.fileName != None:
            self.fptr.close()


    def simUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called at the end of the simulation
        '''
        self.updateQoe(time,sessions, False)
    
    def updateQoe(self,time,sessions, purgeall):
        #Register that we have spent appropriate times in various
        #parts of managed and unmanaged
        #using a purging system to efficinetly only update qoe when it changes
        for s in sessions:
            if s.changed == False and purgeall == False:
                continue
            for d in s.prevQoe:
                if d[1] > 0:
                    self.manperc+= time-s.lastPurgeTime
                #print d
                loc= int(d[0]*self.granularity/self.rttmax)
                if loc >= self.granularity:
                    print >> sys.stderr, "RTT larger than rttmax in qosPdf", \
                    "RTT",d[0],"max",self.rttmax
                    sys.exit()
                self.unmanaged[loc]+= time-s.lastPurgeTime
                loc= int(d[1]*self.granularity/self.rttmax)
                if loc >= self.granularity:
                    print >> sys.stderr, "RTT larger than rttmax in qosPdf", \
                        "RTT",d[1],"max",self.rttmax
                    sys.exit()
                self.managed[loc]+= time-s.lastPurgeTime
                self.total+= time-s.lastPurgeTime             
            s.lastPurgeTime= time
    
        
            

    def simDayUpdate(self,sessions,qoe,cost,time,lastTime,day):
        '''
            Called once per simulated day
        '''
        if self.outputTime == qosPdf.DAILY:
            self.updateQoe(time,sessions, True)
            self.printOutput(day)
            
    def printOutput(self,day):
        '''
            Actually do the output
        '''
        
        #Converting weights in bins to mean and stddev
        convert= float(self.rttmax)/self.granularity
        mansum= 0.0
        unmansum= 0.0
        mansqsum= 0.0
        unmansqsum= 0.0 
        for i in range(self.granularity):
            mansum+= self.managed[i]*i
            unmansum+= self.unmanaged[i]*i
            mansqsum+= self.managed[i]*i*i
            unmansqsum+= self.unmanaged[i]*i*i
        
        mansum*=convert
        mansqsum*=convert*convert
        unmansum*=convert
        unmansqsum*=convert*convert
        if self.total == 0.0:
            manmean= 0.0
            unmanmean= 0.0
            mansd= 0.0
            unmansd= 0.0
            manangedperc= 0.0
        else:
            manmean= mansum/self.total
            unmanmean= unmansum/self.total
            mansd= math.sqrt(mansqsum/self.total - manmean*manmean)
            unmansd= math.sqrt(unmansqsum/self.total - unmanmean*unmanmean)
            managedperc= self.manperc/self.total
        if self.outType == qosPdf.PDF:
            print >> self.fptr, day, managedperc, manmean,mansd,
            tot= 0.0
            for i in range(self.granularity):
                tot+= self.managed[i]
                print >> self.fptr, tot/self.total,
            print >> self.fptr, unmanmean,unmansd,
            tot= 0.0
            for i in range(self.granularity):
                tot+= self.unmanaged[i]
                print >> self.fptr, tot/self.total,
            print >> self.fptr
            return
        print >> self.fptr, day, managedperc, manmean,mansd,unmanmean,unmansd,
        if self.outType == qosPdf.BASIC:
            print >> self.fptr
            return
        if self.outType == qosPdf.QUINTILE:
            count= 5
        else:
            count= 10
        #Add sensible default if there are no samples somehow
        if (self.total == 0.0):
            for i in range(count):
                print >> self.fptr, "0.0 0.0",
            return
        j=1.0/count
        delta= 0.00001 # crudely account for rounding errors
        tot= 0.0
        for i in range(self.granularity):
            tot+= self.managed[i]
            while (tot/self.total >= j-delta):
                print >> self.fptr, float(i)*self.rttmax/self.granularity,
                j+= 1.0/count
        while j <= 1.0-delta:
            print >> self.fptr, self.rttmax,
            j+= 1.0/count
        j=1.0/count
        tot= 0.0
        for i in range(self.granularity):
            tot+= self.unmanaged[i]
            while (tot/self.total >= j-delta):
                print >> self.fptr, float(i)*self.rttmax/self.granularity,
                j+= 1.0/count
        while j <= 1.0-delta:
            print >> self.fptr, self.rttmax,
            j+= 1.0/count
        print >> self.fptr
        self.init_vars()
