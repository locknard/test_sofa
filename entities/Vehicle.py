# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:32:46 2016

@author: derry
"""

from tools import mapTool as mt

class vehicle:
    vehicId = -1
    seatNum = 5
    seatOccup = 0
    custList = []
    latestLoct = mt.Location(-1, -1, -1)
    # latestLoct = mt.location(lat, lng, time)
    nextStop = mt.Location(-1, -1, -1)
    
    def getDestOrder(self):
        """To solve the TSP and return the list of destinations with 
        ETAs in order. The form of the list returned is 
        [(time1, location1), (time2, location2), ...]
        """
        return [(1,1)]
    
    def DestNewOrder(self, order):
        """A TSP with time window.
        """
        return []
        
    def getCurrentPos(self, time):
        return None
    
    def getOrder(self, order):
        return order
    
    def getCustOn(self, order):
        """To return the order with updated eta and vehicle.
        """
        self.custList.append(order)
        self.seatOccup += 1
        order.vehicle = self
        for cust in self.custList:
            cust.orderEta = self.custOffTime(cust)
        # replan the route
        
        return order
    
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