#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 21:11:45 2018

@author: pirate
"""

# Make plots appear inline, set custom plotting style
import matplotlib.pyplot as plt
from scipy.io import wavfile

import numpy as np
from scipy import fftpack

f = 1411  # Frequency, in cycles per second, or Hertz
f_s = 44100  # Sampling rate, or number of measurements per second

rate, audio = wavfile.read('soft_cell.wav')

audio_in = np.mean(audio, axis=1)

step = 0.01

# Grab the chunk and scale to between -1,1
audio = audio_in[1*rate:round((1+step)*rate)]/(2**15)

dbs = 20*np.log10(np.sqrt(np.mean(audio**2)) )

t = np.linspace(0, (1*step), round(step * f_s), endpoint=False)
x = np.sin(f * 2 * np.pi * t)
x=audio

fig, ax = plt.subplots()
ax.plot(t, x)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Signal amplitude');

X = fftpack.fft(x)
freqs = fftpack.fftfreq(len(x))*f_s

fig, ax = plt.subplots()

ax.stem(freqs,np.abs((X)))
ax.set_xlim(0,f_s/10)
#ax.stem(freqs,np.abs(X))
#ax.set_xlabel('Frequency in Hertz [Hz]')
#ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
#ax.set_xlim(-f_s / 2, f_s / 2)
#ax.set_ylim(-5, 110)