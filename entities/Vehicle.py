# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:32:46 2016

@author: derry
"""

from tools import mapTool as mt

class Vehicle:

    def __init__(self, vehicId, vehicDf):
        self.vehicId = vehicId
        self.seatNum = vehicDf[vehicDf.index == 
                                 vehicId].seatNum[vehicId]
        l_lat = vehicDf[vehicDf.index == vehicId].latestLoct[vehicId]['lat']
        l_lng = vehicDf[vehicDf.index == vehicId].latestLoct[vehicId]['lng']
        l_time = vehicDf[vehicDf.index == vehicId].latestLoct[vehicId]['time']
        self.latestLoct = mt.Location(l_lat, l_lng, l_time)
        n_lat = vehicDf[vehicDf.index == vehicId].nextStop[vehicId]['lat']
        n_lng = vehicDf[vehicDf.index == vehicId].nextStop[vehicId]['lng']
        n_time = vehicDf[vehicDf.index == vehicId].nextStop[vehicId]['time']
        self.nextStop = mt.Location(n_lat, n_lng, n_time)
        self.seatOccup = vehicDf[vehicDf.index == 
                                 vehicId].seatOccup[vehicId]       

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
    
    def getOrder(self, order, orderDf, vehicDf, eventDf):
        """When the vehicle decides to get the order,
        it needs to replan its route, while the ETAs 
        of the customers on the vehicle are changed. 
        Simultaneously, the getOnTime and the of the new customer
        are also firmed and the order event is deleted from eventDf.
        """
        # This piece of code has not been finished yet.
        # update the get-off events related to the vehicle.
        # Notice that vectorization is feasible for this piece of code.
        # ixList is the list of coresponding event index 
        ixList = eventDf[(eventDf['eventType'] == 'getOff') & 
                (eventDf['vehicId'] == vehicle.vehicId)].index
        eventDf.loc[ixList, 'vehicId'] = vehicle.vehicId

        for ix in ixList:
            # update the occurrence time of the related get-off events
            # vehicle.custList[order].getOfftime has been updated
            # in vehicle.getOrder # eventDf.loc[ix, :]
            orderId = eventDf.loc[ix, 'orderId']
            eventDf.loc[ix, 'getOffTime'] = vehicle.getOrdById(orderId)

        # arrange the get-on event of the new customer
        getOnEvent = [order.custId, order.o_lat, order.o_lng, 
         order.d_lat, order.d_lng, order.orderTime, 
         order.getOnTime, order.orderId, order.vehicId, 'getOn']
        eventDf.loc[len(eventDf)] = getOnEvent
        # delete the order event from eventDf.
        
    
    def getCustOn(self, order, orderDf, vehicDf, eventDf):
        """To return the order with updated ETA and vehicle.
        """
        self.custList.append(order)
        self.seatOccup += 1
        order.vehicle = self
        for cust in self.custList:
            cust.getOffTime = self.custOffTime(cust)

        # add the customer to the vehicle's orderList
        vehicDf[vehicDf.index == 
                self.vehicId].orderIdList[self.vehicId].append(order.orderId)
        vehicDf.loc[self.vehicId, 'seatOccup'] += 1
        vehicDf[vehicDf.index ==
              self.vehicId].latestLoct[self.vehicId]['lat'] = order.origin.lat
        vehicDf[vehicDf.index ==
              self.vehicId].latestLoct[self.vehicId]['lng'] = order.origin.lng
        vehicDf[vehicDf.index ==
              self.vehicId].latestLoct[self.vehicId]['time'] = order.getOnTime

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