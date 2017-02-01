#!/usr/bin/python3
'''
Possible distances: 100, 200, 400, 800, 1500, Mile, 5k, 10k, HM, Mar
'''

import numpy as np
import lmc
from getpass import getuser

fields = ('Distance 1', 'Performance 1', 'Distance 2', 'Performance 2',\
             'Distance 3', 'Performance 3','Distance to Predict', 'Predicted Performance')

USER = getuser()

def portal_to_prediction(x,data,tbc):
    conf = {}
    conf['gender'] = 'Male'
    conf['percentiles'] = [0,25]
    conf['no_events_tried'] = 3
    conf['outlier_threshold'] = 0.05
    x = np.log(x)
    y = np.zeros((x.shape[0]+1,x.shape[1]))
    y[:-1,:] = x
    y[-1,:] = np.log(data)
    tobecompleted = np.zeros(y.shape)
    tobecompleted[-1,:] = tbc
    method_conf = {}
    if USER=='duncanblythe':
        method_conf['distances'] = np.load('/Users/duncanblythe/work/repo/running_calculator/distances.npy')
    else:
        method_conf['distances'] = np.load('/home/blythed/running_calculator/distances.npy')
    method_conf['alg_iterations'] = 5000
    method_conf['r'] = 3
    predicted = lmc.lmc(y,tobecompleted,method_conf)
    prediction = np.exp(predicted[-1,np.where(tbc)[0][0]])
    error = prediction*0.0302
    return prediction, error

def portal_to_prediction_tns(x,data,tbc):
    conf = {}
    conf['gender'] = 'Male'
    conf['percentiles'] = [0,25]
    conf['no_events_tried'] = 3
    conf['outlier_threshold'] = 0.05
    x = np.log(x)
    y = np.zeros((x.shape[0]+1,x.shape[1]))
    y[:-1,:] = x
    tobecompleted = np.zeros(y.shape)
    method_conf = {}
    if USER=='duncanblythe':
        method_conf['distances'] = np.load('/Users/duncanblythe/work/repo/running_calculator/distances.npy')
    else:
        method_conf['distances'] = np.load('/home/blythed/running_calculator/distances.npy')
    method_conf['alg_iterations'] = 5000
    method_conf['r'] = 3

    prediction = data

    while sum(tbc)>0:
        y[-1,:] = np.log(prediction)
        nn = get_closest_tbc(prediction,tbc,method_conf['distances'])
        print method_conf['distances'][nn]
        tobecompleted[-1,:] = np.zeros(10)
        tobecompleted[-1,:][nn] = 1
        predicted = lmc.lmc(y,tobecompleted,method_conf)
        prediction = np.exp(predicted[-1,:])
        tbc[nn] = 0
    error = prediction*0.0302
    return prediction, error

def convert_to_seconds(time):
    hms = time.split(':')
    if len(hms)==1:
        return float(hms[0])
    elif len(hms)==2:
        return float(hms[0])*60+float(hms[1])
    elif len(hms)==3:
        return float(hms[0])*(60*60)+float(hms[1])*60+float(hms[2])
    else:
        raise ValueError

def convert_to_time(seconds):
    hours = int(seconds)/3600
    minutes = int(seconds)/60-hours*60
    seconds = seconds-minutes*60-hours*(60*60)
    return '%g:%02d:%05.2f' % (int(hours), int(minutes), float(seconds))

def get_closest_tbc(data,tbc,dd):
    tbc = np.where(tbc)[0]
    print tbc
    print dd
    dd = np.log(dd)
    ok_ix = np.where(np.logical_not(np.isnan(data)))[0]
    dev = []
    for i in range(len(tbc)):
        dev.append(np.min(np.abs(dd[ok_ix]-dd[tbc[i]])))
    return tbc[np.argmin(dev)]

if __name__ == '__main__':
    dd = np.load('../distances.npy')
    data = np.zeros(10)*np.nan
    data[0] = 11.1
    data[1] = 22.2
    x = np.load('../male.npy')
    tbc = np.zeros(10)
    tbc[2:] = 1
    prediction, bla = portal_to_prediction_tns(x,data,tbc)
    print [dd[i]/prediction[i] for i in range(10)]

