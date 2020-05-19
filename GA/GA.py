# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:08:14 2019

@author: 16413
"""

import numpy as np
import geatpy as gp

def aim(Phen):
    x1=Phen[:,[0]]
    x2=Phen[:,[1]]
    return np.sin(x1+x2)+(x1-x2)**2-1.5*x1+2.5*x2+1

x1_i=[-1.5,4]
x2_i=[-3,4]
b_x1=[1,1]
b_x2=[1,1]

ranges=np.vstack([x1_i,x2_i]).T
borders=np.vstack([b_x1,b_x2]).T
varTypes=np.array([0,0])

Encoding = 'BG'
codes = [1,1]
precisions = [6,6]
scales = [0,0]

FieldD = gp.crtfld(Encoding,varTypes,ranges,borders,precisions,codes,scales)

NIND = 20
MAXGEN = 100
maxormins = [1]# 1 means minimization
selectStyle = 'sus'
recStyle = 'xovdp'
mutStyle = 'mutbin'
pc = 0.9
pm = 1
Lind = int(np.sum(FieldD[0,:]))
obj_trace = np.zeros((MAXGEN,2))
var_trace = np.zeros((MAXGEN,Lind))

Chrom = gp.crtpc(Encoding,NIND,FieldD)
variable = gp.bs2real(Chrom,FieldD)

ObjV = aim(variable)

best_ind=np.argmin(ObjV)

for gen in range(MAXGEN):
    
    FitnV = gp.ranking(maxormins*ObjV)
    
    SelCh = Chrom[gp.selecting(selectStyle,FitnV,NIND-1),:]
    SelCh = gp.recombin(recStyle,SelCh,pc)
    SelCh = gp.mutate(mutStyle,Encoding,SelCh,pm)
    
    Chrom = np.vstack([Chrom[best_ind,:],SelCh])
    
    Phen = gp.bs2real(Chrom,FieldD)
    ObjV = aim(Phen)
    obj_trace[gen,1]=ObjV[best_ind]
    var_trace[gen,:]=Chrom[best_ind,:]
    
gp.trcplot(obj_trace,[['我就是试试','也没指望有啥结果']])
best_gen = np.argmin(obj_trace[:,[1]])
print('最好效果',obj_trace[best_gen,1])
variable=gp.bs2real(var_trace[[best_gen],:],FieldD)
print('最好变量:')
for i in range(variable.shape[1]):
    print('x'+str(i)+'=',variable[0,i])