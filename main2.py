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
import matplotlib.pyplot as plt
from matplotlib.lines import fillStyles


def processPrint(edf,vdf):
    print
    print '-----------------------eventDF-----------------------'
    print edf
    print '-----------------------vehicleDF-----------------------'
    print vdf
    print '-----------------------DF end-----------------------'
    print
    
def generatePNG(eid):
    global left,right,up,down
    global orderDf,eventDf,stationDf,vehicDf
    time=eventDf.loc[eid,'time']
    fig=plt.figure(1,figsize=(15,10),frameon=False)
    #plt.axis([left, right, down, up])
    ax=fig.add_subplot(111,aspect=1)
    ax.set_xticks([])
    ax.set_yticks([]) 
    ax.axis('off')
    
    #vehicle location
    vx=vehicDf.loc[:,'x']
    vy=vehicDf.loc[:,'y']
    
    
    #vehicle id and vehicle seats remaining
    vid=vehicDf.loc[:,'vehicId'].apply(int)
    vseats=vehicDf.loc[:,'seatRemains'].apply(int)
    myTxt=[str(vid[i])+":"+str(vseats[i]) for i in range(len(vid))]
    
    #plot vehicle location, id and seat remaining
    ax.scatter(vx,vy,marker='s',s=200,facecolor='b',linewidth=0)
    for i in range(len(vid)):
        ax.annotate(myTxt[i], xy=(vx[i],vy[i]),xytext=(vx[i]-60,vy[i]-120))
        
    #plot stations 
    ax.scatter(stationDf.loc[:,'x'],stationDf.loc[:,'y'],s=60,marker='.',facecolor='b',alpha=0.3)
    
    #vehicle next stop
    movingVeh=vehicDf[vehicDf['nextStop']>0]
    nextx=stationDf.loc[movingVeh['nextStop'],'x']
    nextx.index=movingVeh.index
    nexty=stationDf.loc[movingVeh['nextStop'],'y']
    nexty.index=movingVeh.index
    for i in nextx.index:
        ax.arrow(vx[i],vy[i],nextx[i]-vx[i],0,head_length=1,head_width=1)
        ax.arrow(nextx[i],vy[i],0,nexty[i]-vy[i],head_length=70,head_width=50)
    
    #waiting order
    orderEvent=eventDf.loc[eventDf['eventType']!='getOff']
    waitingOrder=list((orderEvent['eventId']/10).apply(int))
    waitingx=orderDf.loc[waitingOrder,'ox']
    waitingy=orderDf.loc[waitingOrder,'oy']
    sid=orderDf.loc[waitingOrder,'os']
    sx=stationDf.loc[sid,'x']
    sy=stationDf.loc[sid,'y']
    ax.scatter(waitingx,waitingy,marker='^',s=100,facecolor='r',linewidth=0)
    for i in range(len(waitingx)):
        ax.arrow(waitingx.iloc[i],waitingy.iloc[i],sx.iloc[i]-waitingx.iloc[i],sy.iloc[i]-waitingy.iloc[i],head_length=1,head_width=1)
    
    #order dest
    orderEvent=eventDf.loc[eventDf['eventType']=='getOff']
    waitingOrder=list((orderEvent['eventId']/10).apply(int))
    waitingx=orderDf.loc[waitingOrder,'dx']
    waitingy=orderDf.loc[waitingOrder,'dy']
    sid=orderDf.loc[waitingOrder,'ds']
    sx=stationDf.loc[sid,'x']
    sy=stationDf.loc[sid,'y']
    ax.scatter(waitingx,waitingy,marker='v',s=100,facecolor='g',linewidth=0) 
    for i in range(len(waitingx)):
        ax.arrow(waitingx.iloc[i],waitingy.iloc[i],sx.iloc[i]-waitingx.iloc[i],sy.iloc[i]-waitingy.iloc[i],head_length=1,head_width=1)
    
    
    ax.set_title("time: %d, event type: %s"%(time,eventDf.loc[eid,'eventType']))
    fig.savefig("png/"+str(int(time))+"_"+str(eid)+".png",dpi=90,format='png')
    plt.close('all')
    

print 
print "Program started at",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


NOT_DEFINED = None
orderDf = NOT_DEFINED
vehicDf = NOT_DEFINED
eventDf = NOT_DEFINED

START_TIME = 0
END_TIME = 86400

NUM_OF_VEHICLES=3
_down=40.06676
_up=40.09070
_left=116.30787
_right=116.37215

## initialization ##
stationDf=pd.read_csv(open("stations","r"),sep='\t',header=0)
tmp=mt.convert_to_meter(stationDf[['lat','lng']], 40.0)

stationDf['x']=tmp.iloc[:,0]
stationDf['y']=tmp.iloc[:,1]
left=np.min(stationDf['x'])
right=np.max(stationDf['x'])
down=np.min(stationDf['y'])
up=np.max(stationDf['y'])

stationDf['x']=stationDf['x']-left
stationDf['y']=stationDf['y']-down


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

tmp=tmp[(tmp['o_lng']<_right ) & ( tmp['o_lng']>_left ) & ( tmp['o_lat']<_up ) & ( tmp['o_lat']>_down ) & (tmp['d_lng']<_right ) & ( tmp['d_lng']>_left ) & ( tmp['d_lat']<_up ) & ( tmp['d_lat']>_down)]


orderDf=tmp[['orderId','o_lat', 'o_lng', 'd_lat','d_lng','orderTime','getOnTime','getOffTime','vehicId']]

tmp=mt.convert_to_meter(orderDf[['o_lat','o_lng']], 40.0)

orderDf['ox']=tmp.iloc[:,0]
orderDf['oy']=tmp.iloc[:,1]

tmp=mt.convert_to_meter(orderDf[['d_lat','d_lng']], 40.0)

orderDf['dx']=tmp.iloc[:,0]
orderDf['dy']=tmp.iloc[:,1]

orderDf['ox']=orderDf['ox']-left
orderDf['dx']=orderDf['dx']-left
orderDf['oy']=orderDf['oy']-down
orderDf['dy']=orderDf['dy']-down

orderDf.index = orderDf['orderId']

#********************************************************************************************************
'''
code below modified the  time of the order 82530 so that these 2 orders are in adjacent time.
'''
orderDf.loc[8253,'orderTime']=1627
orderDf.loc[8253,'ox']=orderDf.loc[8253,'ox']+3100
orderDf.loc[8253,'oy']=orderDf.loc[8253,'oy']+400
orderDf.loc[8253,'dx']=orderDf.loc[8253,'dx']+4000
orderDf.loc[8253,'dy']=orderDf.loc[8253,'dy']+1300
#********************************************************************************************************


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

startTime=np.min(orderDf['orderTime'])
print "%d orders loaded."%(len(orderDf))




vehicDf=pd.DataFrame(columns=[['vehicId','seatNum']])
vehicDf['vehicId']=range(NUM_OF_VEHICLES)
vehicDf['seatNum']=5
vehicDf['seatRemains']=5
vehicDf.index = vehicDf['vehicId']
vehicDf['orderIdList'] = [[] for _ in range(len(vehicDf))]
vehicDf['onStationIdList'] = [[] for _ in range(len(vehicDf))]
vehicDf['offStationIdList'] = [[] for _ in range(len(vehicDf))]
vehicDf['pairStationIdList'] = [[] for _ in range(len(vehicDf))]
vehicDf['route'] = [[] for _ in range(len(vehicDf))]
#===============================================================================
# vehicDf['x']=[rd.uniform(left,right) for _ in range(len(vehicDf))]
# vehicDf['y']=[rd.uniform(down,up) for _ in range(len(vehicDf))]
#===============================================================================
left=np.min(stationDf['x'])
right=np.max(stationDf['x'])
down=np.min(stationDf['y'])
up=np.max(stationDf['y'])
vehicDf['x']=[(left+right)/2.0 for _ in range(len(vehicDf))]
vehicDf['y']=[(down+up)/2.0 for _ in range(len(vehicDf))]
vehicDf['time']=startTime
vehicDf['nextStop'] =-1
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

## simulation ##
print
print "Simulation started."
#processPrint(eventDf, vehicDf)
sys.stdout.flush()

lostOrder = 0
while len(eventDf) != 0:
    # the index of next event
    
    evInx = eventDf['time'].idxmin()
    nextEvent = eventDf.loc[evInx, :]
    vehicDf=updateVehiclePos(nextEvent['time'], vehicDf,stationDf)
    
    print '\t Vehicle position updated.'

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
        vehicDf=getOn(eventId, vehicId,orderDf,vehicDf,eventDf,stationDf)
        
        
    ### Event of getting on the vehicle ###
    if (nextEvent['eventType'] == 'getOff'):
        eventId = nextEvent['eventId']
        vehicId=nextEvent['vehicId']
        vehicDf=getOff(eventId, vehicId,orderDf,vehicDf,eventDf,stationDf)
    generatePNG(evInx)
    eventDf=eventDf.drop(evInx)
    print "\t\t event %d completed."%(evInx)
    #processPrint(eventDf, vehicDf)
    sys.stdout.flush()
    

print "Completed."