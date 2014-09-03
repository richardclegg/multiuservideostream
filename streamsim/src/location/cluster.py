#!/usr/bin/env python

import locationProvider

import location

class cluster(locationProvider.locationProvider):
    ''' class represents a cluster of users'''
    
    clusterCount= 0
    
    def __init__(self, location):
        locationProvider.locationProvider.__init__(self,location)
        self.users= []
        self.clusterNo= cluster.clusterCount
        self.weight= 1.0
        cluster.clusterCount+= 1
        
    def __hash__(self):
        return hash(self.clusterNo)
        
    def __eq__(self, clus):
        
        if not (isinstance(clus, cluster)):
            return False
        if self.clusterNo == clus.clusterNo:
            return True
        return False
        
    def __ne__(self, clus):
        return not self.__eq__(clus)
        
    def __lt__(self, clus):
        if not (isinstance(clus, cluster)):
            return False
        if self.weight < clus.weight:
            return True
        return False
        
    def __gt__(self, clus):
        if not (isinstance(clus, cluster)):
            return False
        if self.weight > clus.weight:
            return True
        return False
        
    @staticmethod
    def clusterFromUser(user):
        c= cluster(user.getLocation())
        c.users=[user]
        c.weight=1.0
        return c
        
    @staticmethod
    def clusterFromDemand(dem):
        c= cluster(dem.getLocation())
        c.weight=dem.rate
        c.users=[]
        return c
        
    def getUsers(self):
        return self.users

    def getNoUsers(self):
        return len(self.users)
        
    def getNo(self):
        return self.clusterNo
        
    def getWeight(self):
        return self.weight
            
    @staticmethod
    def mergeClusters(clusterList):
    
        loclist= map(cluster.getLocation,clusterList)
        weights= map(cluster.getNo,clusterList)
        loc= location.location.weightedMergeLocations(loclist,weights)
        userlist= sum(map(cluster.getUsers,clusterList),[])
        c= cluster(loc)
        c.users=userlist
        c.weight= sum(weights)
        return c
        
    @staticmethod
    def mergeTwoClusters(c1,c2):
        loc= location.location.mergeTwoLocations(c1.getLocation(),c2.getLocation(),
            c1.weight,c2.weight)
        c=cluster(loc)
        c.users= c1.users+c2.users
        c.weight= c1.weight+c2.weight
        return c

            
    @staticmethod
    def clusterDemandLocs(locs, nclust, qoeModel):
        clusters= {}
        cluster.clustercount= 0
        for (i,l) in enumerate(locs):
            clusters[i]= cluster.clusterFromDemand(l)
        return cluster.doClustering(clusters,nclust, qoeModel,True)
            


    @staticmethod
    def eliminateAndMergeClusters(clusters,i,j,distMatrix,qoeModel,weight=False):
        #print "Merging",i,j,distMatrix[i][j]
        newc= cluster.mergeTwoClusters(clusters[i],clusters[j])
        newc.clusterNo= j
        clusters.pop(i)
        clusters.pop(j)
        clusters[j]= newc
        for i in clusters:
            if i == j:
                continue
            c= clusters[i]
            d=qoeModel.calcPairDelayNoCache(newc.getLocation(), \
                        c.getLocation())
            if weight:
                d*= newc.weight*c.weight
            if (i < j):
                distMatrix[i][j]= d
            else:
                distMatrix[j][i]= d
            
        

    @staticmethod
    def clusterUsers(users,nclust,qoeModel):
        clusters= {}
        cluster.clustercount= 0
        nusers=len(users)
        for (i,u) in enumerate(users):
            clusters[i]= cluster.clusterFromUser(u)
        return cluster.doClustering(clusters,nclust,qoeModel)
    
    @staticmethod
    def doClustering(clusters, nclust, qoeModel,weight=False):
        
        clen= len(clusters)
        
        if clen  <= nclust:
            return clusters.values()
            
        distMatrix = [[0.0 for x in xrange(clen)] for y in xrange(clen)]
        minDist= None
        for j in clusters:
            for i in xrange(j):
                c1= clusters[i]
                c2= clusters[j]
                d= qoeModel.calcPairDelay(c1.getLocation(), \
                        c2.getLocation())
                if weight:
                    d*= c1.weight*c2.weight
                distMatrix[i][j]= d
                if minDist == None or d < minDist:
                    minC1= i
                    minC2= j
                    minDist= d
        #print "Merging",clusters[minC1].clusterNo+1,clusters[minC2].clusterNo+1, "dist",minDist
        cluster.eliminateAndMergeClusters(clusters,minC1,minC2,distMatrix, qoeModel,weight)
        while len(clusters) > nclust:
            minDist= None
            for i in clusters:
                for j in clusters:
                    if i >= j: 
                        continue
                    d= distMatrix[i][j]
                    if minDist == None or d < minDist:
                        minC1= i
                        minC2= j
                        minDist= d
            #print "Merging",clusters[minC1].clusterNo+1,clusters[minC2].clusterNo+1, "dist",minDist
            cluster.eliminateAndMergeClusters(clusters,minC1,minC2,distMatrix,qoeModel,weight)
        c= list(clusters.values())
        del clusters
        return c

