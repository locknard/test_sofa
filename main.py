# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:20:51 2016

@author: derry
"""

from entities import Order

START_TIME = 0
END_TIME = 86400
NOT_DEFINED = None

# initialization
orderDf = NOT_DEFINED
lostOrder = 0
vehicList = []
# eventDf
# columns: custId, o_lat, o_lng, d_lat, d_lng, orderTime, time, 
# orderId, vehicId, eventType
eventDf = orderDf.loc[:,['custId','o_lat','o_lng','d_lat','d_lng','orderTime']]
eventDf['time'] = eventDf['orderTime']
eventDf['orderId'] = eventDf.index
eventDf['vehicId'] = -1
eventDf['eventType'] = 'order'

# simulation
while len(eventDf) != 0:
    # the index of next event
    evInx = eventDf['time'].idxmin()
    nextEvent = eventDf.loc[evInx,:]
    
    ### Event of placing an order ###
    if (eventDf.at[evInx,'eventType'] == 'order'):
        order = Order.Order.getOrderBySr(nextEvent)
        vehicle = Order.Order.searchVehicle(order, vehicList)
        if (vehicle == None):
            lostOrder += 1
            del order
        else:
            order = vehicle.getOrder(order)
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

    ### Event of getting on the vehicle ###
    if (nextEvent == 'getOn'):
        order = nextEvent[1]
        print 'getOn'
    ### Event of getting on the vehicle ###
    if (nextEvent == 'getOff'):
        print 'getOff'