# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:20:51 2016

@author: derry
@author: Guangzhi
"""

from heapq import heappop
from entities import Order
from tools import mapTool as mt

# initialization
orderDf = None
lostOrder = 0



order = Order(orderDf.at[1, 'custId'], orderDf.at[1, 'orderTime'],
              mt.Stop(orderDf.at[1, 'o_lat'], orderDf.at[1, 'o_lng']), mt.Stop(orderDf.at[1, 'd_lat'], orderDf.at[1, 'd_lng']))
eventList = [{'time': order.orderTime, 'order': order,
              'vehicle': None, 'event': 'order'}]

# simulation
while eventList:
    nextEvent = heappop(eventList)['event']
    if (nextEvent == 'order'):
        print 'order'
        
    
    if (nextEvent == 'getOn'):
        print 'getOn'
        
    if (nextEvent == 'getOff'):
        print 'getOff'