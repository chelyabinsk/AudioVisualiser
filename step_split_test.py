#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 23:06:26 2018

@author: pirate
"""

from scipy.io import wavfile
import numpy as np
from skimage import util
from scipy.fftpack import fft
import matplotlib.pyplot as plt

freqs = (np.linspace(1,1024,1024))

freq_space = 15.3

groups = [20,25,31.5,40,50,63,80,100,125,160,200,250,315,400,
          500,630,800,1000,1200,1600,2000,2500,3000,4000,5000,
          6300,8000,10000,12000,16000,2000
         ]

pos = 0
l = [0]*len(groups)

for i in range(1024):
    if(groups[pos] <= (i+1)*freq_space):
        pos += 1
    l[pos] += 1
    
    
plt.plot(l)
