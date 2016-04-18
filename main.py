# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:20:51 2016

@author: derry
"""

from entities import Order, Vehicle
from tools import mapTool as mt
import pickle as pk
import pandas as pd
import datetime
import sys
import random as rd

print 
print "Program started at",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
START_TIME = 0
END_TIME = 86400
NOT_DEFINED = None
NUM_OF_VEHICLES=20
down=40.06676
up=40.09070
left=116.30787
right=116.37215


## initialization ##
orderDf = NOT_DEFINED
tmp=pk.load(open("sampleDemandPickle","rb"))
tmp['getOnTime']=-1
tmp['getOffTime']=-1
tmp['vehicId']=-1
tmp['orderId']=range(len(tmp))
tmp['o_lat']=tmp[1]
tmp['o_lng']=tmp[2]
tmp['d_lat']=tmp[3]
tmp['d_lng']=tmp[4]
tmp['orderTime']=tmp['time']

tmp=tmp[(tmp['o_lng']<right ) & ( tmp['o_lng']>left ) & ( tmp['o_lat']<up ) & ( tmp['o_lat']>down ) & (tmp['d_lng']<right ) & ( tmp['d_lng']>left ) & ( tmp['d_lat']<up ) & ( tmp['d_lat']>down)]

orderDf=tmp[['orderId','o_lat', 'o_lng', 'd_lat','d_lng','orderTime','getOnTime','getOffTime','vehicId']]
orderDf.index=tmp['orderId']

# columns of orderDf: orderId, o_lat, o_lng, d_lat, d_lng, orderTime,
# getOnTime, getOffTime, vehicId.
orderDf.index = orderDf['orderId']
orderDf['getOnTime'] = orderDf['getOffTime'] = orderDf['vehicId'] = -1
#orderDf['ETA'] = orderDf[['o_lat', 'o_lng', 'd_lat','d_lng']].apply(mt.getEta)
'''
@todo: eta function
'''  
orderDf['ETA']=[-1]*len(orderDf)
print "%d orders loaded."%(len(orderDf))
print orderDf

vehicDf = NOT_DEFINED
vehicDf=pd.DataFrame(columns=[['vehicId','seatNum']])
vehicDf['vehicId']=range(NUM_OF_VEHICLES)
vehicDf['seatNum']=5

# columns of vehicDf: vehicId, seatNum
# Initialize vehicDf by adding columns: initLoct, orderIdList, latestLoct,
# nextStop.
# The form of initLoct, latestLoct, and nextStop:
# {'lat': -1, 'lng': -1, 'time': -1}.
vehicDf.index = vehicDf['vehicId']
vehicDf['orderIdList'] = [[] for _ in range(len(vehicDf))]
vehicDf['latestLoct'] = vehicDf['nextStop'] = [{'lat': rd.uniform(down,up), 'lng': rd.uniform(left,right), 
                            'time': 0} for _ in range(len(vehicDf))]
print "%d vechicles created."%(len(vehicDf))
print vehicDf

eventDf = orderDf.loc[:,['orderId', 'orderTime']]
eventDf.columns = 'orderId', 'time'
eventDf['vehicId'] = -1
eventDf['eventType'] = 'order'
print "%d events added to the eventlist."%(len(eventDf))

# eventDf
# columns: time, orderId, vehicId, eventType
lostOrder = 0

## simulation ##
print
print "Simulation started."

sys.stdout.flush()
while len(eventDf) != 0:
    # the index of next event
    evInx = eventDf['time'].idxmin()
    nextEvent = eventDf.loc[evInx, :]
    
    print "\t handling event %d, event time is %d, event type is '%s'."%(evInx,nextEvent['time'],nextEvent['eventType'])
    
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
            # The vehicle decide to take the new order.
            vehicle.getOrder(order, orderDf, vehicDf, eventDf)
            del order

    ### Event of getting on the vehicle ###
    if (nextEvent['eventType'] == 'getOn'):
        vehicId = nextEvent['vehicId']
        vehicle = Vehicle.Vehicle(vehicId, vehicDf)
        orderId = nextEvent['orderId']
        order = Order.Order(orderId, orderDf)
        vehicle.getCustOn(order, orderDf, vehicDf, eventDf)
        del order
        del vehicle
        
    ### Event of getting on the vehicle ###
    if (nextEvent['eventType'] == 'getOff'):
        vehicId = nextEvent['vehicId']
        vehicle = Vehicle.Vehicle(vehicId, vehicDf)
        orderId = nextEvent['orderId']
        order = Order.Order(orderId, orderDf)
        vehicle.getCustOff(order, orderDf, vehicDf, eventDf)
        del order
        del vehicle
    sys.stdout.flush()