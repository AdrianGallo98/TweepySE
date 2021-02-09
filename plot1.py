# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:02:49 2020

@author: Adrian Gallo
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
x = []
pos = []
neg = []
neu = []



def animate(i):
    data = pd.read_csv('abortion.csv', index_col=False)
    

    x = data['ID'].values
    pos = data['Positives'].values
    neg = data['Negatives'].values
    neu = data['Neutrals'].values
    
    ax1.clear()
    
    ax1.plot(x, pos, label='Positives')
    ax1.plot(x, neg, label='Negatives')
    ax1.plot(x, neu, label='Neutrals')
    
    ax1.set_title('Difference between sentiment analysis of tweets')
    ax1.legend(loc='upper left')
    ax1.set_xlabel('total')
    ax1.set_ylabel('tweets')
    
ani = animation.FuncAnimation(fig,animate,interval=100)
plt.show()