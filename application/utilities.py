### UNCATEGORIZED USEFUL FUNCTIONS=======================================>>>

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np



## ===================VALIDATIONS===================================
def reqvalidation(ftext):
    return

def normalvalidation(fieldtext):
    """This is for Name, Description and Notes Validation"""
    flag = True
    # if not fieldtext:
    #     flag = False
    validate_exp = (';' in fieldtext) or ('=' in fieldtext)
    if validate_exp:
        flag = False
    if ' ' in fieldtext:
        try:
            l = list(fieldtext.split(' '))
            for val in l:
                val = val.strip() # remove double or more consecutive spaceses
                if val.isalpha():
                    if val.upper()=='DELETE' or val.upper()=='SELECT' or val.upper()=='TRIGGER':
                        flag = False
        except:
            return False
        finally:
            if flag:
                return flag #which is True
            else:
                return False
    return flag

def usernamevalidation(fieldtext):
    """This is for Name, Description and Notes Validation"""
    flag = True
    if not fieldtext:
        flag = False
    validate_exp = (' ' in fieldtext) or (';' in fieldtext) or ('=' in fieldtext)
    if validate_exp:
        flag = False
    if not fieldtext:
        flag = False
    return flag

def idvalidation(idval):
    flag = True
    if not idval:
        flag = False
    if not isinstance(idval, int):
        try:
            idval = int(idval)
        except:
            flag = False
    if isinstance(idval, float):
        flag = False
    return flag

def csvvalidation(fieldtext):
    """This is for csv Validation of settings"""
    flag = True
    validate_exp = (' ' in fieldtext) or (';' in fieldtext) or ('=' in fieldtext)
    if validate_exp:
        flag = False
    try:
        l = list(fieldtext.split(','))
        for val in l:
            if val.isalpha():
                if val.upper()=='DELETE' or val.upper()=='SELECT' or val.upper()=='TRIGGER':
                    flag = False
        # return flag
    except:
        return False
    return flag

## ============================PLOTTING=========================================
def getmonthlyDatanum(loglist, lastlog, tname):
    
    cts = lastlog.timestamp
    # print(cts)
    cmonth = cts[5:7]
    # print(cmonth)
    mappingdict = {}
    for logrec in loglist:
        if (logrec.timestamp)[5:7]==cmonth:
            k = int(logrec.timestamp[8:10])
            v = float(logrec.value)
            # print(k,v)
            if k not in mappingdict.keys():
                # print(k,v)
                mappingdict[k] = [v]
            else:
                # print(k,v)
                # mappingdict[k] = mappingdict[k].append(v)
                mappingdict[k] = mappingdict[k]+[v]
    xdate = []
    yval = []
    # print(mappingdict)
    for k in mappingdict.keys():
        xdate.append(k)
        templ = mappingdict[k]
        yval.append(float(sum(templ)/len(templ)))

    lowest, highest = min(yval), max(yval)
    # lowlim = int(lowest - (highest-lowest)/2)
    # highlim = int(highest + (highest-lowest)/2)
    lowlim = (lowest - (highest-lowest)/2)
    highlim = (highest + (highest-lowest)/2)

    x = np.array(xdate)
    y = np.array(yval)
    rcParams['figure.figsize'] = 8, 5
    plt.plot(x,y)
    plt.ylim(lowlim, highlim)
    # if highlim-lowlim>1:
    #     plt.ylim(lowlim, highlim)
    plt.xlabel("Date-->")
    plt.ylabel(str(tname)+" value-->")
    plt.savefig('static/images/monthlygraph.png')
    plt.clf()


def getoverallDatanum(loglist, lastlog, tname):
    pass


def getmonthlyDatamcq(loglist, lastlog, tname, allvars):
    cts = lastlog.timestamp
    # print(cts)
    cmonth = cts[5:7]
    # print(cmonth)
    mappingdict = {eachvar:0 for eachvar in allvars}
    for logrec in loglist:
        if (logrec.timestamp)[5:7]==cmonth:
            mappingdict[logrec.value] += 1

    names = list(mappingdict.keys())
    values = list(mappingdict.values())
    rcParams['figure.figsize'] = 8, 5
    fig, axs = plt.subplots(1, 1, figsize=(9, 3), sharey=True)
    axs.bar(names, values)
    plt.xlabel("Date-->")
    plt.ylabel(str(tname)+" value-->")
    plt.savefig('static/images/hist.png')
    plt.clf()
