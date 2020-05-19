# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 08:05:43 2019

@author: 16413
"""
count=0
for a in range(1,1000):
    for b in range(1,1000):
        c=1000-a-b
        if ((a*a)+(b*b))==(c*c):
            count+=1
            print(a,b,c,count)
        else:
            pass