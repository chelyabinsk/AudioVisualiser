#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 23:12:10 2018

@author: pirate
"""

import pygame
from pygame import mixer
import audio_reader2 as Audio
import time
import numpy as np
import sys
 
class Renderer():
    def __init__(self,resolution=(800,680),fps=60):
        M = 2048  # slice size
        # Load the song
        song_name = "bonnie.wav"
        song = Audio.Audio_fft(song_name,True,M=M)
        #song = Audio.Audio_fft("test.wav",False,M=M)
        
        # Initialize the game engine
        pygame.init()
        # Load audio
        pygame.mixer.music.load(song_name)
        #pygame.mixer.music.load('test.wav')
        # Start audio
        pygame.mixer.music.play(0)
    
         
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(resolution)
         
        # Loop until the user clicks the close button.
        done = False
        while not done:
            song_time = pygame.mixer.music.get_pos()
            #print(song_time)
            for event in pygame.event.get():   # User did something
                if(event.type == 2):
                    mixer.pause()
                    time.sleep(2)
                    mixer.unpause()
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True   # Flag that we are done so we exit this loop
            #seconds=(pygame.time.get_ticks()-start_ticks)/1000
            seconds = song_time/1000
            try:
                scale = int(np.floor(song.rate/M*seconds))
                slice_num = [M*(scale),M*(scale+1)]
                #print(slice_num,seconds)
                self.draw_fourier(song.get_fft(slice_num,grouped=True,localAvg=False))
                self.draw_raw(song.get_wave(slice_num))
            except:
                break
                
                
            fps = pygame.font.Font(None, 30).render("FPS: " + str(int(clock.get_fps())), True, pygame.Color('white'))
            #framecounter = pygame.font.Font(None, 30).render("SLICE: " + str(frame), True, pygame.Color('white'))
            minutes = seconds//60
            secs = seconds - minutes*60
            time_string = "{:02.0f}:{:02.0f}".format(minutes,secs)
            runningtime = pygame.font.Font(None, 30).render(time_string, True, pygame.Color('white'))
            self.screen.blit(fps, (20, 320))
            #self.screen.blit(framecounter, (300, 320))
            self.screen.blit(runningtime, (100, 320))
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            
            clock.tick(60)
         
        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit()
    
    def draw_fourier(self,data):
        # Set the screen background
        self.screen.fill((200,180,200))
        
        # Draw the box
        pygame.draw.rect(self.screen,(155,155,115),(10,10,780,300))
        pygame.draw.rect(self.screen,(0,0,0),(10,10,780,300),2)
        
        # Draw the equally spaced points to represent x axis
        for i in range(0,29):
            if(data[i] >= 0):
                pygame.draw.rect(self.screen,(0,0,0),(9+10+26.5*i,310-2,20,-1*295*data[i]))
            #print(data[i])
    
    def draw_raw(self, data):
        pygame.draw.rect(self.screen,(155,155,115),(144,350,512,300))
        pygame.draw.rect(self.screen,(0,0,0),(144,350,512,300),2)
        # Width 770 pixels
        
        dat = np.array(data)
        
        avg = np.mean(dat.reshape(-1, 4), axis=1)
        avg /= 2**15
        
        for i in range(len(avg)):
            pygame.draw.rect(self.screen,(0,0,0),(144+i,350+150,1,-1*150*avg[i]))

app = Renderer(fps=30)
