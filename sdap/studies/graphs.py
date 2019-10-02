import os
import json
from datetime import datetime

import numpy as np
import pandas as pd
import uuid
import shutil
import time

# Get requested values from file
def getValue(study, selectedvalues):
    dIndex = cPickle.load(open((study.file.path + ".pickle"))
    fList = open((study.file.path, "r")
    result = {}
    for val in selectedvalues :
        if str(val) in dIndex:
            iPosition = dIndex[str(val)]
            fList.seek(iPosition)
            result[str(val)] = fList.readline().decode().rstrip().split('\t')[1:]
        else:
            result[str(val)] = []
    return result

# Get classes from pickle file
def getClass(study):
    dIndex = cPickle.load(open(study.file.path + ".pickle"))
    result = []
    for index in dIndex :
        if "Class" in index :
            result.append(index)
    return result

def bw_nrd0(x):
    x = [float(i) for i in x]
    if len(x) < 2:
        raise(Exception("need at least 2 data points"))
    hi = np.std(x, ddof=1)
    q75, q25 = np.percentile(x, [75 ,25])
    iqr = q75 - q25
    lo = min(hi, iqr/1.34)
    if not ((lo == hi) or (lo == abs(x[0])) or (lo == 1)):
        lo = 1
    return 0.9 * lo *len(x)**-0.2

def get_graph_data(studies, selected_class=None, selected_genes=[]):

    # TODO: Genes + class

    result = {'charts':[],'warning':[],'time':''}
    start_time = time.time()
    for study in studies:
        chart = {}
        chart['classes'] = getClass(study)
        if not selected_class:
            selected_class = chart['classes'][0]
        groups = getValue(study, [selected_class])
        groups = np.array(groups[selected_class])
        _, idx = np.unique(groups, return_index=True)
        uniq_groups = groups[np.sort(idx)[::-1]]
        # Maybe we should have done this at the previous step
        samples = getValue(study,['Sample'])
        samples = np.array(samples['Sample'])

        if genes:
            # Later
            pass

        else:
            chart = {}
            x = np.array(getValues(study, ['X'])['X'])
            y = np.array(getValue(study, ['Y'])['Y'])
            chart['config']={'displaylogo':False,'modeBarButtonsToRemove':['toImage','zoom2d','pan2d','lasso2d','resetScale2d']}
            chart['data']=[]
            chart['description'] = ""
            chart['name'] = "Classification by: %s" % (selected_class)
            chart['selected'] = selected_class
            chart['dir'] = stud
            chart['layout'] = { 'width':1180,
                                'height':800,
                                'yaxis':{'autorange': True,'showgrid': False,'showticklabels': False,'zeroline': True,'showline': False, 'autotick': True},
                                'xaxis':{'showticklabels': False,'autorange': True,'showgrid': False,'zeroline': True,'showline': False,'autotick': True},
                                'autoexpand': True,
                                'showlegend': False,
                                'legend': {'yanchor':'bottom','orientation':'h','traceorder':'reversed'},
                                'title':'',
                                'hovermode':'closest'
                              }
            chart['gene'] = ""
            chart['msg'] = []
            for cond in uniq_groups :
                val_x= x[np.where(groups == str(cond))[0]]
                val_y= y[np.where(groups == cond)[0]]
                text = samples[np.where(groups == cond)[0]]
                data_chart = {}
                data_chart['x'] = []
                data_chart['x'].extend(val_x)
                data_chart['y'] = []
                data_chart['y'].extend(val_y)
                if len(data_chart['x']) == 0 and len(data_chart['y']) == 0 :
                    chart['layout']['title'] = "No available data for %s" % (selected_class)
                data_chart['name'] = cond
                data_chart['text'] = []
                data_chart['text'].extend(text)
                data_chart['hoverinfo'] = "all"
                data_chart['type'] = 'scatter'
                data_chart['mode']= 'markers'
                chart['data'].append(data_chart)

            result['charts'].append(chart)

    interval = time.time() - start_time
    result['time'] = interval
    result['selected'] = selected_class
    return result
