'''
Created on 20160418

@author: Guangzhi
'''


from tools import mapTool as mt


def searchVeh(oid,odf,vdf):
    return vdf.iloc[0,:]['vehicId']

def addOrder(oid,vid,odf,vdf,edf):
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