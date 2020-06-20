#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 20:08:06 2018

https://stackoverflow.com/questions/604453/analyze-audio-using-fast-fourier-transform

@author: pirate
"""


from scipy.io import wavfile
import numpy as np
from skimage import util
from scipy.fftpack import fft
import matplotlib.pyplot as plt

class Audio_fft():
    def __init__(self, filename, stereo=True, M=2048):
        self.rate, self.audio = wavfile.read(filename)
        
        self.M = M
        # Average out the left and right channels
        if(stereo):
            self.audio = np.mean(self.audio, axis=1)
            
        N = self.audio.shape[0]
        L = N / self.rate
        
        #print(self.audio.shape,self.rate)
        #print(f'Audio shape: {self.audio.shape}, Sliced audio shape: {self.slices.shape}')
        
    def get_fft(self,slice_num, group_num=16, get_freq_space=False,grouped=True,localAvg=False):
        song_slice = self.audio[slice_num[0]:slice_num[1]]
        spectrum = fft(song_slice)
        spectrum = np.abs(spectrum)[:self.M//2]  # Remove the second half
                
        self.freq_space = (self.rate / self.M/2)
        
        #print("freq_space === {}".format(self.freq_space))
        #print((spectrum))
        
        # Return not grouped fft
        if(not grouped):
            return spectrum
        
        # Create grouped results
        # 20,25,31.5,40,50,63,80
        # 100,125,160,200,250,315,400
        # 500,630,800,1k,1k2,1k6,
        # 2k,2k5,3k1,4k,5k,6k3,8k,
        # 10k,12k,16k,20k
        groups = [20,25,31.5,40,50,63,80,100,125,160,200,250,315,400,
                500,630,800,1000,1200,1600,2000,2500,3000,4000,5000,
                6300,8000,10000,12000,16000,2000]
        
        # Split array
        
        pos = 0
        separated_arrs = [0]*len(groups)
        
        for i in range(self.M//2):
            if(groups[pos] <= (i+1)*self.freq_space):
                pos += 1
            separated_arrs[pos] += spectrum[i]
            
        if not localAvg:
            separated_arrs = np.nan_to_num(np.array(separated_arrs))
            return separated_arrs / (2**25)
             
        #print(separated_arrs)
        
        # Workout averages
        means = []
        for i in separated_arrs:
            means.append(np.mean(i))  
            
        # Scale means
        means = np.nan_to_num(np.array(means))
        means /= (means).max()
        return means
    
    def get_freq_array(self):
        freq_space = (self.rate / self.M/2)
        return np.linspace(0,self.M*(freq_space+0.1),self.M/2)
    
    def get_wave(self,slice_num):
        return self.audio[slice_num[0]:slice_num[1]]
    
#audio = Audio_fft("test.wav",False)
#plt.plot(audio.get_freq_array(),audio.get_fft(0,grouped=False))
#plt.xlim(0,262)
#
#a=audio.get_fft(0)