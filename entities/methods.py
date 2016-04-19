'''
Created on 20160418

@author: Guangzhi
'''


from tools import mapTool as mt
import itertools
import pandas as pd
'''
odf:'orderId','o_lat', 'o_lng', 'd_lat','d_lng','orderTime','getOnTime','getOffTime','vehicId','ox','oy','dx','dy','os','ds'
odf.index=orderId
vdf:'vehicId','seatNum','seatRemains','orderIdList','onStationIdList','offStationIdList','pairStationIdList','x','y','time','nextStop'
vdf.index=vehicId
edf:'eventId','time','vehicId','eventType'
edf.index= eventId (eventId ends with 
    0: order event
    1: getOn event
    2: getOff event
    3: passengerWait event
    4: vehicleWait event
sdf:'stationId','lng','lat','x','y'
sdf.index= (automatic)
'''

def updateVehiclePos(time,vdf):
    #based on the event time, update the positions of vehicles.
    
    return vdf

def searchVeh(oid,odf,vdf):
    #search for the appropriate vehicle, return the id of the vehicle.
    return vdf.iloc[0,:]['vehicId']

def getRoute(x,y,startTime,onlist,offlist,pairlist,sdf):
    #start from (x,y), traverse all the stations in slist.
    #Algorithm: test all the permutations. This method works even if two passengers get on/off at the same station
    speed=10.0
    allList=onlist+offlist
    allList=list(set(allList))
    permu=itertools.permutations(allList,len(allList))
    minTime=99999999
    for seq in permu:
        dis=0
        curx=x
        cury=y
        curTime=startTime
        tmp=[]
        
        #test if this permutation satisfies that a customer will get on before get off.
        legal=True
        for pair in pairlist:
            os=pair[0]
            ds=pair[1]
            if seq.index(os)>seq.index(ds):
                legal=False
        
        if not legal:
            break
        
        #calc the cost for this sequence
        for s in seq:
            nextx=sdf.loc[s,'x']
            nexty=sdf.loc[s,'y']
            dis=dis+abs(nextx-curx)+abs(nexty-cury)
            curTime=curTime+dis/speed
            tmp.append((curTime,s))
            curx=nextx
            cury=nexty
        
        #find the sequence with least cost.
        if curTime<minTime:
            result=list(tmp)
            minTime=curTime
    print "\t\t optimal Route: ",
    for i in result:
        print i[1],
    print
    
    return result
        
    

def addOrder(eid,vid,odf,vdf,edf,sdf):
    #add order to vehicle.
    oid=int(eid/10)
    getOnStation=int(odf.loc[oid,'os'])
    getOffStation=int(odf.loc[oid,'ds'])
    orderBeforeThisAddition=list(vdf.loc[vid,'orderIdList'])
    currentTime=edf.loc[eid,'time']
    
    print '\t\t adding order %d to vehicle %d.'%(oid,vid)
    odf.loc[oid,'vehicId']=vid
    vdf.loc[vid,'orderIdList'].append(oid)
    vdf.loc[vid,'onStationIdList'].append(getOnStation)
    vdf.loc[vid,'offStationIdList'].append(getOffStation)
    #use the pair station list to make sure that a get on event happens before the get off event.
    vdf.loc[vid,'pairStationIdList'].append((getOnStation,getOffStation))
    
    #update the number of available seats
    vdf.loc[vid,'seatRemains']=vdf.loc[vid,'seatRemains']-1
    print '\t\t no. of available seats remains is:  %d.'%(vdf.loc[vid,'seatRemains'])
    
    #replan the route.
    onlist=vdf.loc[vid,'onStationIdList']
    offlist=vdf.loc[vid,'offStationIdList']
    pairList=vdf.loc[vid,'pairStationIdList']
    print '\t\t the order list for this vehicle is now: ', vdf.loc[vid,'orderIdList']
    print '\t\t the get on station list for this vehicle is now: ', onlist
    print '\t\t the get off station list for this vehicle is now: ', offlist
    route=getRoute(vdf.loc[vid,'x'], vdf.loc[vid,'y'],currentTime, onlist,offlist,pairList, sdf)
    '''
    route format: [(time1, location1), (time2, location2), ...]
    '''
    vdf.set_value(vid,'route',route)
    
    #add this vechicle Id the the order event
    edf.loc[oid*10,'vehicId']=vid
    #add a get on event.
    getOnTime=0
    for i in route:
        if i[1]==getOnStation:
            getOnTime=i[0]
            break;
    print '\t\t order %d will get on from station %d at %.1f.'%(oid,getOnStation,getOnTime)
    edf=edf.append(pd.DataFrame([[oid*10+1,getOnTime,vid,'getOn']],index=[oid*10+1],columns=['eventId','time','vehicId','eventType']))
    
    #add the get off events for this order.
    getOffTime=0
    for i in route:
        if i[1]==getOffStation:
            getOffTime=i[0]
            break;
    print '\t\t order %d will get off from station %d at %.1f.'%(oid,getOffStation,getOffTime)
    edf=edf.append(pd.DataFrame([[oid*10+2,getOffTime,vid,'getOff']],index=[oid*10+2],columns=['eventId','time','vehicId','eventType']))

    
    #modify the get on and get off events for other orders in this vehicle.
    
    for order in orderBeforeThisAddition:
        thisGetOnStation=int(odf.loc[order,'os'])
        thisGetOffStation=int(odf.loc[order,'ds'])
        for i in route:
            if i[1]==thisGetOnStation:
                print '\t\t getOn event time corresponding to order %d have changed from %.1f to %.1f.'%(order,edf.loc[order*10+1,'time'],i[0])
                edf.loc[order*10+1,'time']=i[0]
                
    #update next stop
    vdf.loc[vid,'nextStop']=route[0][1]
    return (odf,vdf,edf)

def getOn(eid,vid,odf,vdf,edf,sdf):
    #delete the getOn station from stationIdList
    #if two or more passenger get on/off at the same station, just delete one station from the stationIdList
    oid=int(eid/10)
    getOnStation=int(odf.loc[oid,'os'])
    getOffStation=int(odf.loc[oid,'ds'])
    vdf.loc[vid,'onStationIdList'].remove(getOnStation)
    
    #remove the pair since the passenger is already onboard.
    vdf.loc[vid,'pairStationIdList'].remove((getOnStation,getOffStation))
    
    #remove the station from the route
    del vdf.loc[vid,'route'][0]
    
    #set the next station
    vdf.loc[vid,'nextStop']=vdf.loc[vid,'route'][0][1]
    return vdf

def getOff(eid,vid,odf,vdf,edf,sdf):
    #delete the getOff station from stationIdList
    #one more available seat
    oid=int(eid/10)
    getOffStation=int(odf.loc[oid,'ds'])
    vdf.loc[vid,'offStationIdList'].remove(getOffStation)
    vdf.loc[vid,'seatRemains']=vdf.loc[vid,'seatRemains']+1
    #remove the station from the route
    del vdf.loc[vid,'route'][0]
    
    #set the next station
    if len(vdf.loc[vid,'route'])>0:
        vdf.loc[vid,'nextStop']=vdf.loc[vid,'route'][0][1]
    else:
        vdf.loc[vid,'nextStop']=-1
    return vdf
    

def getOrdById(self, orderId):
    """
    """
    for o in self.orderList:
        if o.orderId == orderId:
            return o
    return None

def getDestOrder(self):
    """To solve the TSP and return the list of destinations with 
    ETAs in order. The form of the list returned is 
    [(time1, location1), (time2, location2), ...]
    """
    return [(1,1)]

def DestNewOrder(self, order):
    """A TSP with time window.
    """
    return []
    
def getCurrentPos(self, time):
    return None

def getOrder(self, order, vehileId, vehicDf, eventDf):
    """When the vehicle decides to take the order,
    it needs to replan its route, while the ETAs 
    of the customers on the vehicle are changed. 
    Simultaneously, the getOnTime and the of the new customer
    are also firmed and the order event is deleted from eventDf.
    """
    # This piece of code has not been finished yet.
    # Update the get-off events related to the vehicle.
    # Notice that vectorization is feasible for this piece of code.
    # ixList is the list of coresponding event index 
    ixList = eventDf[(eventDf['eventType'] == 'getOff') & 
            (eventDf['vehicId'] == self.vehicId)].index
    eventDf.loc[ixList, 'vehicId'] = self.vehicId
    # add the customer to the vehicle's orderList
    
    
    for ix in ixList:
        # update the occurrence time of the related get-off events
        # vehicle.custList[order].getOfftime has been updated
        # in vehicle.getOrder # eventDf.loc[ix, :]
        orderId = eventDf.loc[ix, 'orderId']
        eventDf.loc[ix, 'getOffTime'] = self.getOrdById(orderId)

    # arrange the get-on event of the new customer
    getOnEvent = [order.custId, order.o_lat, order.o_lng, 
     order.d_lat, order.d_lng, order.orderTime, 
     order.getOnTime, order.orderId, order.vehicId, 'getOn']
    eventDf.loc[len(eventDf)] = getOnEvent
    # replan the route.
    
    # delete the order event from eventDf.
    

def getCustOn(self, order, orderDf, vehicDf, eventDf):
    """To return the order with updated ETA and vehicle.
    """
    self.custList.append(order)
    self.seatOccup += 1
    order.vehicle = self
    for cust in self.custList:
        cust.getOffTime = self.custOffTime(cust)

    
    vehicDf[vehicDf.index == 
            self.vehicId].orderIdList[self.vehicId].append(order.orderId)
    vehicDf.loc[self.vehicId, 'seatOccup'] += 1
    vehicDf[vehicDf.index ==
          self.vehicId].latestLoct[self.vehicId]['lat'] = order.origin.lat
    vehicDf[vehicDf.index ==
          self.vehicId].latestLoct[self.vehicId]['lng'] = order.origin.lng
    vehicDf[vehicDf.index ==
          self.vehicId].latestLoct[self.vehicId]['time'] = order.getOnTime

    # Arrange the get-off event


def getCustOff(self, order):
    print order.custId + "get off"

def custOffTime(self, order):
    """To estimate the getting-off time of the customer.
    """
    return -1

def isUnacceptable(self, order, ratio = 1.5):
    offTime = self.custOffTime(order)
    duration = offTime - order.orderTime
    eta = mt.getEta(order.origin, order.destin)
    if (duration > ratio * eta):
        return False
    else:
        return True