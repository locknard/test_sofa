# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 22:58:52 2016

@author: derry
"""
from tools import mapTool as mt

START_TIME = 0

class Order:
    custId = -1
    orderTime = START_TIME
    origin = mt.Stop(-1, -1)
    # origin = stop(o_lat, o_lng)
    destin = mt.Stop(-1, -1)
    
    def __init__(self, custId, orderTime, origin, destin):
        self.custId = custId
        self.orderTime = orderTime
        self.origin = origin
        self.destin = destin
    
    def searchVehicle(self):
        """search the optimum matching vehicle near the customer.
        The variable returned is a vehicle object, 
        which belongs to the vehicle class.
        """
        return None
    
        