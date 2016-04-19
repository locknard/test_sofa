# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:20:51 2016

@author: derry
"""

from entities.methods import *
from tools import mapTool as mt
import pickle as pk
import pandas as pd
import datetime
import sys
import random as rd
import scipy.spatial.distance as distance
import numpy as np


print 
print "Program started at",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


NOT_DEFINED = None
orderDf = NOT_DEFINED
vehicDf = NOT_DEFINED
eventDf = NOT_DEFINED

START_TIME = 0
END_TIME = 86400

NUM_OF_VEHICLES=3
down=40.06676
up=40.09070
left=116.30787
right=116.37215

## initialization ##
stationDf=pd.read_csv(open("stations","r"),sep='\t',header=0)
tmp=mt.convert_to_meter(stationDf[['lat','lng']], 40.0)

stationDf['x']=tmp.iloc[:,0]
stationDf['y']=tmp.iloc[:,1]

stationDf['stationId']=stationDf['stationId'].astype(int)
stationDf.index=stationDf['stationId']
print "%d stations loaded."%(len(stationDf))


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

tmp=mt.convert_to_meter(orderDf[['o_lat','o_lng']], 40.0)

orderDf['ox']=tmp.iloc[:,0]
orderDf['oy']=tmp.iloc[:,1]

tmp=mt.convert_to_meter(orderDf[['d_lat','d_lng']], 40.0)

orderDf['dx']=tmp.iloc[:,0]
orderDf['dy']=tmp.iloc[:,1]

# columns of orderDf: orderId, o_lat, o_lng, d_lat, d_lng, orderTime,
# getOnTime, getOffTime, vehicId.
orderDf.index = orderDf['orderId']
orderDf['getOnTime'] = orderDf['getOffTime'] = orderDf['vehicId'] = -1
dis=distance.cdist(orderDf[['ox','oy']], stationDf[['x','y']], 'cityblock')
minIndex=np.argmin(dis,1)
orderDf['os']= minIndex+1


dis=distance.cdist(orderDf[['dx','dy']], stationDf[['x','y']], 'cityblock')
minIndex=np.argmin(dis,1)
orderDf['ds']= minIndex+1
orderDf[['os','ds']]=orderDf[['os','ds']].astype(int)
#orderDf['os']=orderDf['os'].apply(int)
#orderDf['ds']=orderDf['ds'].apply(int)
orderDf['ETA'] = orderDf.apply(mt.getEta,axis=1)

'''
code below modified the  time of the order 82530 so that these 2 orders are in adjacent time.
'''
orderDf.loc[8253,'orderTime']=1627
print "%d orders loaded."%(len(orderDf))


left=min([np.min(orderDf['ox']),np.min(orderDf['dx'])])
right=max([np.max(orderDf['ox']),np.max(orderDf['dx'])])
down=min([np.min(orderDf['oy']),np.min(orderDf['dy'])])
up=max([np.max(orderDf['oy']),np.max(orderDf['dy'])])

vehicDf=pd.DataFrame(columns=[['vehicId','seatNum']])
vehicDf['vehicId']=range(NUM_OF_VEHICLES)
vehicDf['seatNum']=5
vehicDf['seatRemains']=5
vehicDf.index = vehicDf['vehicId']
vehicDf['orderIdList'] = [[] for _ in range(len(vehicDf))]
vehicDf['stationIdList'] = [[] for _ in range(len(vehicDf))]
vehicDf['x']=[rd.uniform(left,right) for _ in range(len(vehicDf))]
vehicDf['y']=[rd.uniform(down,up) for _ in range(len(vehicDf))]
vehicDf['time']=0
vehicDf['nextStop'] =0
print "%d vechicles created."%(len(vehicDf))
#print vehicDf


# eventDf
# columns: time, orderId, vehicId, eventType

eventDf = orderDf.loc[:,['orderId', 'orderTime']]
eventDf.columns = 'eventId', 'time'
eventDf['eventId']=eventDf['eventId']*10
eventDf.index=eventDf['eventId']
eventDf['vehicId'] = -1
eventDf['eventType'] = 'order'

print "%d events added to the eventlist."%(len(eventDf))



def processPrint(edf,vdf):
    print
    print '-----------------------eventDF-----------------------'
    print edf
    print '-----------------------vehicleDF-----------------------'
    print vdf
    print '-----------------------DF end-----------------------'
    print

## simulation ##
print
print "Simulation started."
processPrint(eventDf, vehicDf)
sys.stdout.flush()

lostOrder = 0
while len(eventDf) != 0:
    # the index of next event
    
    evInx = eventDf['time'].idxmin()
    nextEvent = eventDf.loc[evInx, :]
    vehicDf=updateVehiclePos(nextEvent['time'], vehicDf)

    print "\t handling event %d, event time is %d, event type is '%s'."%(evInx,nextEvent['time'],nextEvent['eventType'])
    
    ### Event of placing an order ###
    if (nextEvent['eventType'] == 'order'):
        eventId = nextEvent['eventId']
        # crtOrderDf (current order df) is a dataframe
        # crtOrderDf = orderDf[(orderDf.index == orderId)]
        vehicleId = searchVeh(eventId,orderDf,vehicDf)
        
        if (vehicleId == None):
            lostOrder += 1
            print "\t\t didn't find appropriate vehicle, this order is marked as lost."
        else:
            # The vehicle decide to take the new order.
            print "\t\t vehicle with id %d is chosen."%(vehicleId)
            (orderDf,vehicDf,eventDf)=addOrder(eventId, vehicleId,orderDf,vehicDf,eventDf,stationDf)

    ### Event of getting on the vehicle ###
    if (nextEvent['eventType'] == 'getOn'):
        eventId = nextEvent['eventId']
        vehicId=nextEvent['vehicId']
        vehicDf=getOff(eventId, vehicId,orderDf,vehicDf,eventDf,stationDf)
        
        
    ### Event of getting on the vehicle ###
    if (nextEvent['eventType'] == 'getOff'):
        eventId = nextEvent['eventId']
        vehicId=nextEvent['vehicId']
        vehicDf=getOn(eventId, vehicId,orderDf,vehicDf,eventDf,stationDf)
        
    eventDf=eventDf.drop(evInx)
    print "\t\t event %d completed."%(evInx)
    processPrint(eventDf, vehicDf)
    sys.stdout.flush()