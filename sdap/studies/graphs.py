import os
import json
from datetime import datetime

import numpy as np
import pandas as pd
import uuid
import shutil
import time

import pickle

# Get requested values from file
def getValues(data, selectedvalues):
    dIndex = pickle.load(open(data.file.path + ".pickle", 'rb'))
    fList = data.file.file.open("rb")
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
def getClasses(data):
    dIndex = pickle.load(open(data.file.path + ".pickle", 'rb'))
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

def get_graph_data_full(file, selected_class=None):

    result = {'charts':[],'warning':[],'time':''}
    start_time = time.time()
    chart = {}
    # Should not happen. We select the class before
    chart['classes'] = getClasses(file)
    if not selected_class:
        selected_class = chart['classes'][0]
    groups = getValues(file, [selected_class])
    groups = np.array(groups[selected_class])
    _, idx = np.unique(groups, return_index=True)
    uniq_groups = groups[np.sort(idx)[::-1]]
    # Maybe we should have done this at the previous step
    samples = getValues(file,['Sample'])
    samples = np.array(samples['Sample'])

    x = np.array(getValues(file, ['X'])['X'])
    y = np.array(getValues(file, ['Y'])['Y'])
    chart['config']={'displaylogo':False,'modeBarButtonsToRemove':['toImage','zoom2d','pan2d','lasso2d','resetScale2d']}
    chart['data']=[]
    chart['description'] = ""
    chart['name'] = "Classification by: %s" % (selected_class)

    chart['layout'] = { #'autosize': True,
                        'width':"",
                        'height':"",
                        'yaxis':{'autorange': True,'showgrid': False,'showticklabels': False,'zeroline': True,'showline': False, 'autotick': True},
                        'xaxis':{'showticklabels': False,'autorange': True,'showgrid': False,'zeroline': True,'showline': False,'autotick': True},
                        'autoexpand': True,
                        'showlegend': True,
                        'legend': {'yanchor':'bottom','orientation':'h','traceorder':'reversed'},
                        'title':'',
                        'hovermode':'closest'
                      }
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

    result['chart'] = chart
    interval = time.time() - start_time
    result['time'] = interval
    return result

def get_graph_data_genes(file, gene, selected_class=None):

    ensemblgene = gene.ensemble_id

    result = {'warning':[],'time':''}
    start_time = time.time()
    # We should do this in the view, and select the class before
    classes =  getClasses(file)
    if not selected_class:
        selected_class = classes[0]
    groups = getValues(file, [selected_class])
    groups = np.array(groups[selected_class])
    _, idx = np.unique(groups, return_index=True)
    uniq_groups = groups[np.sort(idx)[::-1]]
    # Maybe we should have done this at the previous step
    samples = getValues(file,['Sample'])
    samples = np.array(samples['Sample'])
    x = np.array(getValues(file, ['X'])['X'])
    y = np.array(getValues(file, ['Y'])['Y'])

    genes = getValues(file, [gene.gene_id])
    ensembl_genes = getValues(file, [ensemblgene])

    chart = {}
    gene_name = gene.symbol
    chart['config'] = {'displaylogo':False,'modeBarButtonsToRemove':['toImage','zoom2d','pan2d','lasso2d','resetScale2d']}
    chart['data'] = []
    chart['description'] = ""
    chart['name'] = "Expression of: %s " % (gene_name)
    chart['title'] = ""
    chart['layout'] = {'width':1180 ,'height':800,'yaxis':{'autorange': True,'showgrid': False,'showticklabels': False,'zeroline': True,'showline': False,'autotick': True},'xaxis':{'showticklabels': False,'autorange': True,'showgrid': False,'zeroline': True,'showline': False,'autotick': True},'autoexpand': True,'showlegend': False, 'legend': {'yanchor':'bottom','orientation':'h','traceorder':'reversed'},"title":'', 'hovermode': 'closest'}
    chart['gene'] = gene_name
    chart['msg'] = ""

    max_val = 0
    min_val = 0
    #EntrezGenes
    val_gene = np.array(genes[gene.gene_id])
    val_gene = val_gene.astype(np.float)
    if len(val_gene) != 0 :
        max_val =  np.max(val_gene.astype(np.float))
        min_val =  np.min(val_gene.astype(np.float))

    #Ensembl IDs
    val_gene_ensembl = np.array(ensembl_genes[ensemblgene])
    if len(val_gene_ensembl) != 0 :
        max_val =  np.max(val_gene_ensembl.astype(np.float))
        min_val =  np.min(val_gene_ensembl.astype(np.float))

    chart['maxval'] = int(round(max_val))
    chart['minval'] = int(round(min_val))

    #Add condition information according selected the class
    for cond in uniq_groups :
        if len(val_gene) != 0 :
            val = val_gene[np.where(groups == cond)[0]]
            val_x= x[np.where(groups == cond)[0]]
            val_y= y[np.where(groups == cond)[0]]
            text = samples[np.where(groups == cond)[0]]
            data_chart = {}
            data_chart['type'] = 'scattergl'
            data_chart['mode']= 'markers'
            data_chart['text'] = []
            data_chart['text'].extend(text)
            data_chart['x'] = []
            data_chart['x'].extend(val_x)
            data_chart['y'] = []
            data_chart['y'].extend(val_y)
            data_chart['name'] = cond
            data_chart['hoverinfo'] = "all"
            data_chart['marker']={'color':[],'cmax':max_val,'cmin':min_val}
            data_chart['marker']['color'].extend(val)
            chart['data'].append(data_chart)
        elif len(val_gene_ensembl) != 0 :
            val = val_gene_ensembl[np.where(groups == cond)[0]]
            val_x= x[np.where(groups == cond)[0]]
            val_y= y[np.where(groups == cond)[0]]
            text = samples[np.where(groups == cond)[0]]
            data_chart = {}
            data_chart['type'] = 'scattergl'
            data_chart['mode']= 'markers'
            data_chart['text'] = []
            data_chart['text'].extend(text)
            data_chart['x'] = []
            data_chart['x'].extend(val_x)
            data_chart['y'] = []
            data_chart['y'].extend(val_y)
            data_chart['name'] = cond
            data_chart['hoverinfo'] = "all"
            data_chart['marker']={'color':[],'cmax':max_val,'cmin':min_val}
            data_chart['marker']['color'].extend(val)
            chart['data'].append(data_chart)
        else :
            chart['msg'] = "No data available for %s gene" % (gene_name)

    #ADD VIOLIN PLOT FOR GENE
    violin_chart = {}
    violin_chart['config']={'displaylogo':False,'modeBarButtonsToRemove':['toImage','zoom2d','pan2d','lasso2d','resetScale2d']}
    violin_chart['data']=[]
    violin_chart['description'] = ""
    violin_chart['name'] = "Violin plot of: %s " % (gene_name)
    violin_chart['title'] = "violin"
    violin_chart['selected'] = selected_class
    if len(uniq_groups) > 25 :
        violin_chart['layout'] = {'height': 1000,'showlegend': False,'margin':{'l':300,},'yaxis':{'tickfont':10},'hovermode': 'closest'}
    else :
        violin_chart['layout'] = {'height': 600,'showlegend': False,"title":'','margin':{'l':300,},'yaxis':{'tickfont':10},'hovermode': 'closest'}
    violin_chart['gene'] = gene_name
    violin_chart['violmsg'] = ""

    for cond in uniq_groups :
        val =""
        if len(val_gene) != 0 :
            val = val_gene[np.where(groups == cond)[0]]
        elif len(val_gene_ensembl) != 0 :
            val = val_gene_ensembl[np.where(groups == cond)[0]]

        data_chart = {}
        data_chart['x'] = []

        q3 = np.percentile(val.astype(np.float), 75) #Q3

        data_chart['x'].extend(val)
        data_chart['name'] = cond
        data_chart['hoverinfo'] = "all"
        max_x = max(data_chart['x'])
        min_x = min(data_chart['x'])

        if len( data_chart['x']) > 5 :
            if max_x != min_x and q3 > 0 and len( data_chart['x']) > 10:
                bw = bw_nrd0(data_chart['x'])
                data_chart['type'] = 'violin'
                data_chart['points'] = False
                data_chart['pointpos'] = 0
                data_chart['jitter'] = 0.85
                #data_chart['bandwidth'] = bw
                data_chart['scalemode'] = "width"
                data_chart['spanmode'] = "hard"
                data_chart['orientation'] = 'h'
                data_chart['box'] = {'visible': True}
                data_chart['boxpoints'] = False
            else :
                data_chart['type'] = 'box'
                data_chart['orientation'] = "h"
                data_chart['boxpoints'] = False
                data_chart['y'] = [cond] * len(data_chart['x'])
                data_chart['boxmean'] = True
        else :
            data_chart['type'] = 'box'
            data_chart['orientation'] = "h"
            data_chart['boxpoints'] = False
            data_chart['y'] = [cond] * len(data_chart['x'])
            data_chart['boxmean'] = True
            violin_chart['violmsg'] = ""
        violin_chart['data'].append(data_chart)

    result['chart'] = chart
    result['violin_chart'] = violin_chart
    interval = time.time() - start_time
    result['time'] = interval
    return result
