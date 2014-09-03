#!/usr/bin/env python


class qoeModel(object):
    """An abstract class which represents user qoe for traffic
    on a route"""

    def __init__(self):
        """Initialisation"""
        #cache is a dictionary for location pairs
        self.cache={}

    def parseJSON(self,js,fName):
        """Parse any JSON used by this particular QoE Model"""
        pass

    def fromCache(self,loc1,loc2):
        try:
            dist= self.cache[(loc1,loc2)]
            return dist
        except KeyError:
            return None

    def toCache(self,loc1,loc2,dist):
        self.cache[(loc1,loc2)]= dist

    def cacheSize(self):
        return len(self.cache)

    def calcPairDelay(self,loc1,loc2):
        """Calculate distance between pair of locations"""

        return 0.0

    def calcRouteDelay(self,route):

        """Calculate distance along a route returning total and managed
        distance -- assume route first and last hop unmanaged"""
        tot= 0.0
        totManage= 0.0
        for i in range(len(route)-1):
            delay=self.calcPairDelay(route[i].getLocation(), \
                route[i+1].getLocation())
            tot+= delay
            if i > 0 and i < len(route)-2:
                totManage+=delay
        return (tot,totManage)

    def calcSessionDelay(self, session, routeMod):
        """Calculate delay from a session -- the sessions passed is a
        list of routes"""
        if session.changed == False:
            return session.cachedQoe
        servers= session.datacentres
        
        
        #Recalculate routes for session
        symmetric= routeMod.symmetric()
        if symmetric:
            noRoutes= ((session.noUsers()*(session.noUsers()-1))/2)
        else:
            noRoutes= (session.noUsers()*(session.noUsers()-1))
        qoe=list(xrange(noRoutes))
        session.routes=list(xrange(noRoutes))
        k= 0
        
        for (i,user1) in enumerate(session.getUsers()):
            for (j,user2) in enumerate(session.getUsers()):
                if i == j:
                    continue
                if symmetric and i < j:
                    continue
                route= routeMod.getRoute(servers,user1,user2,self)
                session.routes[k]=route
                (t,m)= self.calcRouteDelay(route)
                qoe[k]=(t,m)
                k+=1
        session.prevQoe= session.cachedQoe
        session.cachedQoe= qoe
        return qoe

    def calcAllSessionDelay(self, sessions, routeMod):
        """Calculate delay from a list of sessions -- the sessions passed is a
        list of routes"""
        delay=[]
        for s in sessions:
            delay.append(self.calcSessionDelay(s,routeMod))
        return delay
