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
# columns of orderDf: custId, o_lat, o_lng, d_lat, d_lng, orderTime
lostOrder = 0
vehicDf = NOT_DEFINED
# columns of vehicDf: vehicId, seatNum

eventDf = orderDf.loc[:,['custId','o_lat','o_lng','d_lat','d_lng','orderTime']]
eventDf['time'] = eventDf['orderTime']
eventDf['orderId'] = eventDf.index
eventDf['vehicId'] = -1
eventDf['eventType'] = 'order'
# eventDf
# columns: custId, o_lat, o_lng, d_lat, d_lng, orderTime, time, 
# orderId, vehicId, eventType

# simulation
while len(eventDf) != 0:
    # the index of next event
    evInx = eventDf['time'].idxmin()
    nextEvent = eventDf.loc[evInx,:]
    
    ### Event of placing an order ###
    if (nextEvent['eventType'] == 'order'):
        order = Order.Order.getOrderBySr(nextEvent)
        vehicle = Order.Order.searchVehicle(order, vehicDf)
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
    if (nextEvent['eventType'] == 'getOn'):
        vehicId = nextEvent['vehicId']
        
        print 'getOn'
    ### Event of getting on the vehicle ###
    if (nextEvent['eventType'] == 'getOff'):
        print 'getOff'