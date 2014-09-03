#!/usr/bin/env python


class simulationModel:

    def __init__(self, simOpts):
        """Initialise stream simulation model"""
        self.outputFile= simOpts.outputFile
        self.routeMod= simOpts.routeMod
        self.sessionMod= simOpts.sessionMod
        self.serverMod= simOpts.serverMod
        self.qoeMod= simOpts.qoeMod
        self.netMod= simOpts.netMod
        self.demMod= simOpts.demMod
        self.outputs= simOpts.outputs
        self.dayLen= 24.0*60.0*60.0

    def insertDeparture(self,departList,nextUser):
        """Insert a user into the list of departures at the correct place"""
        for (i,u) in enumerate(departList):
            if nextUser.endTime < u.endTime:
                departList.insert(i,nextUser)
                return
        departList.append(nextUser)

    def simulate(self,days):
        """ Perform simulation """
        # time is in seconds
        endTime= self.dayLen*days
        nextDay= self.dayLen
        time= 0.0
        day= 1
        nextUser= self.demMod.nextArrival(time)
        departList= [nextUser]
        lastTime= 0
        for o in self.outputs:
            o.simStartUpdate()
        while time < endTime:
            if nextUser.startTime < departList[0].endTime:
                #arrival occurs
                time= nextUser.startTime
                self.sessionMod.addUser(nextUser)
                nextUser= self.demMod.nextArrival(time)
                self.insertDeparture(departList,nextUser)
                for o in self.outputs:
                    o.userArrive(time)
            else:
                #departure occurs
                departing= departList.pop(0)
                time= departing.endTime
                self.sessionMod.removeUser(departing)
                for o in self.outputs:
                    o.userDepart(time)

            sessions= self.sessionMod.getSessions()

            #qoe will be a list of tuples -- delay over managed + unmanaged network
            qoe= []
            #cost will be list of tuples -- data in + data across + data out
            cost= []

            #for each session
            for s in sessions:
                # update servers if necessary, assign servers available for a session
                self.serverMod.updateServers(time,s,self.netMod,self.qoeMod, \
                    self.routeMod, self.demMod)
                # For the session, now calculate QoE
                qoe.append(self.qoeMod.calcSessionDelay(s,self.routeMod))
                cost.append(self.netMod.getCostTuple(s,time-lastTime,self.routeMod))

            for o in self.outputs:
                o.simUpdate(sessions,qoe,cost,time,lastTime,day)

            # Update day
            while time > nextDay:
                print "Day",day,"complete"
                for o in self.outputs:
                    o.simDayUpdate(sessions,qoe,cost,time,lastTime,day)
                day+= 1
                nextDay+= self.dayLen
            lastTime= time
            for s in sessions:
                s.changed= False
        for o in self.outputs:
            o.simEndUpdate(sessions,qoe,cost,time,lastTime,day)
