# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 22:58:52 2016

@author: derry
"""

from tools import mapTool as mt
from main import START_TIME, END_TIME

class Order:
    orderId = -1
    custId = -1
    orderTime = START_TIME
    # estimated time of arrival, considering the current condition.
    getOnTime = END_TIME
    getOffTime = END_TIME
    origin = mt.Stop(-1, -1)
    # origin = stop(o_lat, o_lng)
    destin = mt.Stop(-1, -1)
    # Standard estimated time of arrival, only related with OD positions.
    stEta = mt.getEta(origin, destin)
    vehicle = None

    def __init__(self, orderId, custId, orderTime, origin, destin, 
                 vehicle = None, getOnTime = END_TIME, getOffTime = END_TIME):
        self.orderId = orderId
        self.custId = custId
        self.orderTime = orderTime
        self.origin = origin
        self.destin = destin
        self.vehicle = vehicle
        self.getOnTime = getOnTime
        self.getOffTime = getOffTime

    def getOrderBySr(self, eventSr):
        order = Order(eventSr['orderId'], 
                      eventSr['custId'], 
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
    
        