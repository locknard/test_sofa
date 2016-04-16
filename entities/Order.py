# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 22:58:52 2016

@author: derry
"""

from tools import mapTool as mt
from main import START_TIME, END_TIME

class Order:
    custId = -1
    orderTime = START_TIME
    # estimated time of arrival, considering the current condition.
    orderEta = END_TIME
    origin = mt.Stop(-1, -1)
    # origin = stop(o_lat, o_lng)
    destin = mt.Stop(-1, -1)
    # Standard estimated time of arrival, only related with OD positions.
    stEta = mt.getEta(origin, destin)
    vehicle = None

    def __init__(self, custId, orderTime, origin, destin, 
                 vehicle = None, orderEta = END_TIME):
        self.custId = custId
        self.orderTime = orderTime
        self.origin = origin
        self.destin = destin
        self.vehicle = None
        self.orderEta = END_TIME

    def getOrderBySr(self, eventSr):
        order = Order(eventSr['custId'], 
                      eventSr['orderTime'],
                      mt.Stop(eventSr['o_lat'], 
                              eventSr['o_lng']), 
                      mt.Stop(eventSr['d_lat'], 
                              eventSr['d_lng']))
        return order

    def searchVehicle(self, vehicList):
        """search the optimum matching vehicle near the customer.
        The variable returned is a vehicle object, 
        which belongs to the vehicle class.
        """
        return None
    
        