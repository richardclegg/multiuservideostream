#!/usr/bin/env python

import locationProvider


class user(locationProvider.locationProvider):
    """Class representing a user at a given location"""
    usercount= 1
    def __init__(self, loc, starttime,endtime):
        locationProvider.locationProvider.__init__(self,loc)
        self.userno= user.usercount
        user.usercount+= 1
        self.startTime= starttime
        self.endTime= endtime
    
    def getUserNo(self):
        return self.userno
