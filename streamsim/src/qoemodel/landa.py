#!/usr/bin/env python

import haversine.haversine.haverdist as haverdist
import qoeModel


class landa(qoeModel.qoeModel):
    """A class which represents user qoe for traffic on a route
    using haversine distance enhanced with routing distance
    corrections"""

    def __init__(self):
        """Empty initialiser"""
        self.slope=0.016
        self.intercept= 22.3
        self.excessDistance = {
        'ASP_ASC': 14232.0976, 'ASC_ASP': 14232.0976,
        'ASP_ASS': 7876.37230, 'ASS_ASP': 7876.37230,
        'EUW_OCE': 17872.5646, 'OCE_EUW': 17872.5646,
        'OCE_AFR': 20412.9155, 'AFR_OCE': 20412.9155,
        'AFR_SAW': 16693.8666, 'SAW_AFR': 16693.8666,
        'SAW_SAE': 7875.22800, 'SAE_SAW': 7875.22800,
        'OCE_SAW': 16087.8041, 'SAW_OCE': 16087.8041,
        'EUE_OCE': 18122.0771, 'OCE_EUE': 18122.0771,
        'ASP_SAE': 19015.1424, 'SAE_ASP': 19015.1424,
        'OCE_ASC': 18463.8317, 'ASC_OCE': 18463.8317,
        'EUW_ASP': 13069.5551, 'ASP_EUW': 13069.5551,
        'EUE_ASP': 13418.5375, 'ASP_EUE': 13418.5375,
        'OCE_ASP': 9883.11950, 'ASP_OCE': 9883.11950}


    def calcPairDelay(self,loc1,loc2):
        """Calculate distance between pair of locations"""
        dist = haverdist(loc1, loc2) + self.excessDistance[loc1.subcontinentalZone + "_" +  loc2.subcontinentalZone]
        time= self.slope * dist + self.intercept
        return time

