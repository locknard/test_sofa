# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:27:06 2016

@author: derry
"""

import numpy as np

class Stop:
    
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

class Location:
    
    def __init__(self, lat, lng, time):
        self.lat = lat
        self.lng = lng
        self.time = time

def convert_to_meter(X, lat):
    radius = 6371000.0
    alpha = np.pi*radius/180.0
    Y = X.copy()
    Y.iloc[:, 0] = X.iloc[:, 1] * alpha * np.cos(lat*np.pi/180.0)  #lng
    Y.iloc[:, 1] = X.iloc[:, 0] * alpha                            #lat
    return Y

def convert_to_latlng(Y, lat):
    radius = 6371000.0
    alpha = np.pi*radius/180.0
    X = Y.copy()
    X.iloc[:, 1] = Y.iloc[:, 0] / (alpha * np.cos(lat*np.pi/180.0))
    X.iloc[:, 0] = Y.iloc[:, 1] / alpha
    return X

def getEta(o_lat, o_lng, d_lat, d_lng):
    return None

def getAngle(OD_1, OD_2):
    return None

def getRouteLen(stopList):
    return -1
    
def getAllPosition(vehicDf, time):
    return vehicDf
