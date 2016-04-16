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
    orderList = []
    latestLoct = mt.Location(-1.0, -1.0, -1.0)
    # latestLoct = mt.location(lat, lng, time)
    nextStop = mt.Location(-1.0, -1.0, -1.0)
    
    def getOrdById(self, orderId):
        """
        """
        for o in self.orderList:
            if o.orderId == orderId:
                return o
        return None
    
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
        """When the vehicle decides to get the order,
        it needs to replan its route, while the ETAs 
        of the customers on the vehicle are changed. 
        Simultaneously, the getOnTime and the of the new customer
        are also firmed. Thus the new order with 
        """
        return order
    
    def getCustOn(self, order):
        """To return the order with updated ETA and vehicle.
        """
        self.custList.append(order)
        self.seatOccup += 1
        order.vehicle = self
        for cust in self.custList:
            cust.getOffTime = self.custOffTime(cust)
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
        eta = mt.getEta(order.origin, order.destin)
        if (duration > ratio * eta):
            return False
        else:
            return True