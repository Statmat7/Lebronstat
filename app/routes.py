#!/usr/bin/env python3
from flask import render_template,request
from app import app
from app.forms import StartForm
from io import BytesIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import base64
import copy
from matplotlib.pyplot import figure
import seaborn as sns

roster={
    1:['Lebron James',23.0,],
    2:['Kevin Love',19.7,],
    3:['Kyrie Irving', 16.4,],
    4:['Tristan Thompson', 14.3,],
    5:['J.R. Smith', 5.0,],
    6:['Iman Shumpert', 9.0,],
    7:['Channing Frye', 8.2,],
    8:['Richard Jefferson', 1.5,],
    9:['James Jones', 5.0,],
    10:['Timofey Mozgov', 5.0,],
    11:['Mo Williams', 2.1,],
    12:['Sasha Kaun', 1.3,],
    13:['M. Dellavedova',1]
    }

orig_roster=copy.deepcopy(roster)
xticks=[]
for v in range(18):
    xticks.append(2*v)
@app.route('/')   
@app.route('/index' , methods=['GET', 'POST'])
def f():
    form = StartForm()
    if request.method == 'POST':
        l_status=form.lebron_status.data
        f_raise=form.flat_raise.data
        s_raise=form.scale_raise.data
        reset_vals=form.reset_salaries.data
    else:
        l_status='In'
        f_raise='None'
        s_raise='None'
        reset_vals='Yes'
    if reset_vals=='Yes':
        cur_roster=copy.deepcopy(orig_roster)
    else:
        cur_roster=roster.copy()
    if l_status=='Out':
        cur_roster.pop(1,None)
    if f_raise=='$2 Million':
         for key , value in cur_roster.items():
            value[1]=value[1]+2
    if s_raise=='10%':
        for key , value in cur_roster.items():
            value[1]=round(value[1]*1.1,1)
    ls = [v[1] for (k,v) in cur_roster.items()]
    mean=round(np.mean(ls),2)
    median=np.median(ls)
    std=round(np.std(ls),2)
    q1=np.percentile(ls,25)
    q3=np.percentile(ls,75)
    IQR=round(q3-q1,2)
    met_table=pd.DataFrame({0:['Mean',mean], 1:['StDev',std],2:['Median',median],3:['IQR',IQR]}).T
    met_table=pd.DataFrame({'Mean':[mean], 'StDev':[std],'Median':[median],'IQR':[IQR]})
    roster_table=pd.DataFrame(cur_roster).T
    roster_table.columns=['Player','Salary in Millions']
    plt.clf()
    figure(figsize=(9, 4))
    sns.set(style="ticks")
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, 
                                        gridspec_kw={"height_ratios": (.15, .85)})
    sns.boxplot(ls, ax=ax_box)
    sns.distplot(ls, ax=ax_hist, kde=False, rug=True, bins=8)
    plt.axvline(x=mean , color='r', label='mean',linewidth=3.0)
    plt.axvline(x=mean-std , color='r', linestyle='--', label='mean-std_deviation',linewidth=3.0)
    plt.axvline(x=mean+std , color='r', linestyle='--', label='mean+std_deviation',linewidth=3.0)
    plt.xticks(xticks)
    plt.title("Distribution of Salaries")
    plt.xlabel("Salary in Millions of Dollars")
    plt.ylabel("Count")
    ax_box.set(yticks=[])
    sns.despine(ax=ax_hist)
    sns.despine(ax=ax_box, left=True)
    figfile=BytesIO()
    plt.savefig(figfile,format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return render_template("lebron.html",result=figdata_png.decode('utf8'),
                           table1=roster_table.to_html(index=False, justify='left'),
                           table2=met_table.to_html(index=False,header=True),
                           form=form,
                           l_status=l_status,
                           f_raise=f_raise,
                           s_raise=s_raise)
