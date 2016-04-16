# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:20:51 2016

@author: derry
"""

from entities import Order

START_TIME = 0
END_TIME = 86400

# initialization
orderDf = None
lostOrder = 0
vehicList = []
eventDf = orderDf.loc[:,['custId','o_lat','o_lng','d_lat','d_lng','orderTime']]
eventDf['time'] = eventDf['orderTime']
eventDf['vehicId'] = -1
eventDf['eventType'] = 'order'

# simulation
while len(eventDf) != 0:
    # the index of next event
    evInx = eventDf['time'].idxmin()
    nextEvent = eventDf.loc[evInx,:]
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
            eventDf[(eventDf['eventType'] == 'getOff') & 
                    (eventDf['vehicId'] == vehicle.vehicId)]
            
            for i in range(len(eventList)):
                if ((eventList[i][2] == "getOff") and
                    (eventList[i][1].vehicle == vehicle)):
                    eventList[i][0] == order.orderEta
                    eventList[i][1] == order
                    event = eventList[i]
                    # maintain eventList
                    hq._siftdown(eventList, 0, i)
                    if (event == eventList[i]):
                        hq._siftup(eventList, i)
            # arrange the get-off event of the new customer         
            hq.heappush(eventList, (order.orderEta, order, "getOff"))


    if (nextEvent == 'getOn'):
        order = nextEvent[1]
        print 'getOn'
        
    if (nextEvent == 'getOff'):
        print 'getOff'