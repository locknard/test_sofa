# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:32:46 2016

@author: derry
"""

from tools import mapTool as mt

class vehicle:
    vehicId = -1
    seatNum = 5
    custList = []
    latestLoct = mt.Location(-1, -1, -1)
    # latestLoct = mt.location(lat, lng, time)
    nextStop = mt.Location(-1, -1, -1)
    
    def getDestOrder(self):
        """To solve the TSP and return the list of destinations in order.
        """
        return []
    
    def DestNewOrder(self, order):
        """A TSP with time window.
        """
        return []
        
    def getCurrentPos(self, time):
        return None
    
    def getCustOn(self, order):
        print order.custId + "get on"
    
    def getCustOff(self, order):
        print order.custId + "get off"
    
    def custOffTime(self, order):
        """To estimate the getting-off time of the customer.
        """
        return -1
    
    def isUnacceptable(self, order, ratio = 1.5):
        offTime = self.custOffTime(order)
        duration = offTime - order.orderTime
        etc = mt.getEtc(order.origin, order.destin)
        if (duration > ratio * etc):
            return False
        else:
            return True