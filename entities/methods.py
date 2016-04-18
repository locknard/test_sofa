'''
Created on 20160418

@author: Guangzhi
'''


from tools import mapTool as mt
import itertools
#odf:'orderId','o_lat', 'o_lng', 'd_lat','d_lng','orderTime','getOnTime','getOffTime','vehicId','ox','oy','dx','dy','os','ds'
#odf.index=orderId
#vdf:'vehicId','seatNum','seatRemains','orderIdList','stationIdList','x','y','time','nextStop'
#vdf.index=vehicId
#edf:'orderId','time','vehicId','eventType'
#edf.index= (automatic)
#sdf:'stationId','lng','lat','x','y'
#sdf.index= (automatic)


def updateVehiclePos(time,vdf):
    #based on the event time, update the positions of vehicles.
    pass

def searchVeh(oid,odf,vdf):
    #search for the appropriate vehicle, return the id of the vehicle.
    return vdf.iloc[0,:]['vehicId']

def getRoute(x,y,startTime,slist,sdf):
    #start from (x,y), traverse all the stations in slist.
    speed=10.0
    permu=itertools.permutations(slist,len(slist))
    minTime=99999999
    for seq in permu:
        dis=0
        curx=x
        cury=y
        curTime=startTime
        tmp=[]
        for s in seq:
            nextx=sdf.loc[s,'x']
            nexty=sdf.loc[s,'y']
            dis=dis+abs(nextx-curx)+abs(nexty-cury)
            curTime=curTime+dis/speed
            tmp.append((curTime,s))
            curx=nextx
            cury=nexty
        
        if curTime<minTime:
            result=list(tmp)
            minTime=curTime
    print "\t\t Optimal Route: ",
    for i in result:
        print i[1],
    print
    
    return result
        
    

def addOrder(oid,vid,odf,vdf,edf,sdf):
    #add order to vehicle.
    print '\t\t adding order %d to vehicle %d.'%(oid,vid)
    odf.loc[oid,'vehicId']=vid
    vdf.loc[vid,'orderIdList'].append(oid)
    vdf.loc[vid,'stationIdList'].append(int(odf.loc[oid,'os']))
    vdf.loc[vid,'stationIdList'].append(int(odf.loc[oid,'ds']))
    
    #update the number of available seats
    vdf.loc[vid,'seatRemains']=vdf.loc[vid,'seatRemains']-1
    print '\t\t no. of available seats remains is:  %d.'%(vdf.loc[vid,'seatRemains'])
    
    #replan the route.
    slist=vdf.loc[vid,'stationIdList']
    print '\t\t the order list for this vehicle is now: ', vdf.loc[vid,'orderIdList']
    print '\t\t the station list for this vehicle is now: ', slist
    route=getRoute(vdf.loc[vid,'x'], vdf.loc[vid,'y'],vdf.loc[vid,'time'], slist, sdf)
    '''
    route format: [(time1, location1), (time2, location2), ...]
    '''

    #add a get on event.
    
    #add the get off events for this order.
    #modify the get on and get off events for other orders in this vehicle.
    pass

def getOn(oid,vid,odf,vdf,edf):
    #delete the station from stationIdList
    
    pass
    

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