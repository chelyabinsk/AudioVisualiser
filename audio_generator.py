#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 17:05:34 2018

@author: pirate
"""

# Create a wave file
import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

data = np.random.uniform(-1,1,44100) # 44100 random samples between -1 and 1

# Create a sin wave
data = []
rate = 44100

notes = [261.626,293.665,329.628,349.228,391.995,440.000,493.883,523.251,26]

def add_note(note,dur):
    freq = notes[note]
    for i in range(0,round(44100*dur)):
        data.append(np.math.sin(freq*i/rate*np.math.pi*2))
    
add_note(8,5)
add_note(0,1)
add_note(2,1)
add_note(4,1)
add_note(7,1)

for i in range(0,round(44100*2)):
    data.append(np.math.sin(notes[0]*i/rate*np.math.pi*2)
             +  np.math.sin(notes[2]*i/rate*np.math.pi*2)
             +  np.math.sin(notes[4]*i/rate*np.math.pi*2)
             +  np.math.sin(notes[7]*i/rate*np.math.pi*2)
             )

scaled = np.int16(data/np.max(np.abs(data)) * 32767)
write('test.wav', 44100, scaled)

plt.plot(data[0:44100])