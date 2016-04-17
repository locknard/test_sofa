# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:20:51 2016

@author: derry
"""

from entities import Order, Vehicle
from tools import mapTool as mt

START_TIME = 0
END_TIME = 86400
NOT_DEFINED = None

## initialization ##
orderDf = NOT_DEFINED
# columns of orderDf: orderId, o_lat, o_lng, d_lat, d_lng, orderTime,
# getOnTime, getOffTime, vehicId.
orderDf.index = orderDf['orderId']
orderDf['getOnTime'] = orderDf['getOffTime'] = orderDf['vehicId'] = -1
orderDf['ETA'] = orderDf[['o_lat', 'o_lng', 'd_lat','d_lng']].apply(mt.getEta)  


vehicDf = NOT_DEFINED
# columns of vehicDf: vehicId, seatNum
# Initialize vehicDf by adding columns: initLoct, orderIdList, latestLoct,
# nextStop.
# The form of initLoct, latestLoct, and nextStop:
# {'lat': -1, 'lng': -1, 'time': -1}.
vehicDf.index = vehicDf['vehicId']
vehicDf['orderIdList'] = [[] for _ in range(len(vehicDf))]
vehicDf['latestLoct'] = vehicDf['nextStop'] = [{'lat': -1, 'lng': -1, 
                            'time': -1} for _ in range(len(vehicDf))]

eventDf = orderDf.loc[:,['orderId', 'orderTime']]
eventDf.columns = 'orderId', 'time'
eventDf['vehicId'] = -1
eventDf['eventType'] = 'order'
# eventDf
# columns: time, orderId, vehicId, eventType
lostOrder = 0

## simulation ##
while len(eventDf) != 0:
    # the index of next event
    evInx = eventDf['time'].idxmin()
    nextEvent = eventDf.loc[evInx, :]
    
    ### Event of placing an order ###
    if (nextEvent['eventType'] == 'order'):
        orderId = nextEvent['orderId']
        # crtOrderDf (current order df) is a dataframe
        # crtOrderDf = orderDf[(orderDf.index == orderId)]
        order = Order.Order(orderId, orderDf)
        vehicle = order.searchVehicle(vehicDf)
        if (vehicle == None):
            lostOrder += 1
            del order
        else:
            vehicle.getOrder(order, orderDf, vehicDf, eventDf)
            del order

    ### Event of getting on the vehicle ###
    if (nextEvent['eventType'] == 'getOn'):
        vehicId = nextEvent['vehicId']
        vehicle = Vehicle.Vehicle(vehicId, vehicDf)
        orderId = nextEvent['orderId']
        order = Order.Order(orderId, orderDf)
        # vehicDf[(vehicDf.vehicId == vehicId)]
        vehicle.getCustOn(order, orderDf, vehicDf, eventDf)
        del order
        del vehicle
        
    ### Event of getting on the vehicle ###
    if (nextEvent['eventType'] == 'getOff'):
        print 'getOff'