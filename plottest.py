#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 23:12:10 2018

@author: pirate
"""

import pygame
from pygame import mixer
import audio_reader2 as Audio
 
class Renderer():
    def __init__(self,resolution=(800,400),fps=60):
        # Load the song
        song = Audio.Audio_fft("black.wav",True)
        
        # Initialize the game engine
        pygame.init()
        sound = mixer.Sound("black.wav")
        mixer.init()
        sound.play()
         
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(resolution)
         
        # Loop until the user clicks the close button.
        done = False
        frame=0
        start_ticks=pygame.time.get_ticks() #starter tick
        while not done:
            seconds=(pygame.time.get_ticks()-start_ticks)/1000
            for event in pygame.event.get():   # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True   # Flag that we are done so we exit this loop
            try:
                self.draw_graph(song.get_fft(7*frame,grouped=True,localAvg=False))
            except:
                break
                
                
            fps = pygame.font.Font(None, 30).render("FPS: " + str(int(clock.get_fps())), True, pygame.Color('white'))
            framecounter = pygame.font.Font(None, 30).render("SLICE: " + str(frame), True, pygame.Color('white'))
            runningtime = pygame.font.Font(None, 30).render("TIME (S): " + str(seconds), True, pygame.Color('white'))
            self.screen.blit(fps, (20, 320))
            self.screen.blit(framecounter, (20, 340))
            self.screen.blit(runningtime, (20, 360))
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            
            clock.tick(60)
            frame += 1
         
        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit()
    
    def draw_graph(self,data):
        # Set the screen background
        self.screen.fill((200,180,200))
        
        # Draw the box
        pygame.draw.rect(self.screen,(155,155,155),(10,10,780,300))
        pygame.draw.rect(self.screen,(0,0,0),(10,10,780,300),2)
        
        # Draw the equally spaced points to represent x axis
        for i in range(0,29):
            if(data[i] >= 0):
                pygame.draw.rect(self.screen,(255,255,255),(9+10+26.5*i,310-2,20,-1*295*data[i]))
            #print(data[i])

app = Renderer(fps=30)