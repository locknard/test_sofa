# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 22:58:52 2016

@author: derry
"""

from tools import mapTool as mt

class Order:

    def __init__(self, orderId, orderDf):
        self.orderId = orderId
        self.orderTime = orderDf[orderDf.index == 
                                 orderId].orderTime[orderId]
        o_lat = orderDf[orderDf.index == 
                                 orderId].o_lat[orderId]
        o_lng = orderDf[orderDf.index == 
                                 orderId].o_lng[orderId]
        self.origin = mt.Stop(o_lat, o_lng)
        d_lat = orderDf[orderDf.index == 
                                 orderId].d_lat[orderId]
        d_lng = orderDf[orderDf.index == 
                                 orderId].d_lng[orderId]        
        self.destin = mt.Stop(d_lat, d_lng)
        self.vehicle = orderDf[orderDf.index == 
                                 orderId].vehicle[orderId]
        self.getOnTime = orderDf[orderDf.index == 
                                 orderId].getOnTime[orderId]
        self.getOffTime = orderDf[orderDf.index == 
                                 orderId].getOffTime[orderId]

    def searchVehicle(self, vehicList):
        """search the optimum matching vehicle near the customer.
        The variable returned is a vehicle object, 
        which belongs to the vehicle class.
        """
        return None
    
        