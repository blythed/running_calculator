import numpy as np
from calculator.models import Athlete
import sys
sys.path.append('/Users/duncanblythe/work/repo/running/python_code/')
import load_data

if __name__=='__main__':
    conf = {}
    conf['no_events_tried'] = 3
    conf['percentiles'] = [0,25]
    conf['gender'] = 'Male'
    conf['outlier_threshold'] = 0.05
    x = load_data.get_data(conf)
    x[np.isnan(x)]=0
    for i in range(x.shape[0]):
        print i
        a = Athlete()
        a.best100 = x[i,0]
        a.best200 = x[i,1]
        a.best400 = x[i,2]
        a.best800 = x[i,3]
        a.best1500 = x[i,4]
        a.bestMile = x[i,5]
        a.best5k = x[i,6]
        a.best10k = x[i,7]
        a.bestHM = x[i,8]
        a.bestMar = x[i,9]
        a.save()
    conf = {}
    conf['no_events_tried'] = 3
    conf['percentiles'] = [0,25]
    conf['gender'] = 'Female'
    conf['outlier_threshold'] = 0.05
    x = load_data.get_data(conf)
    x[np.isnan(x)]=0
    for i in range(x.shape[0]):
        print i
        a = Athlete()
        a.best100 = x[i,0]
        a.best200 = x[i,1]
        a.best400 = x[i,2]
        a.best800 = x[i,3]
        a.best1500 = x[i,4]
        a.bestMile = x[i,5]
        a.best5k = x[i,6]
        a.best10k = x[i,7]
        a.bestHM = x[i,8]
        a.bestMar = x[i,9]
        a.save()
