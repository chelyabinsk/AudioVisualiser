# Visualizes the rendered audio using Dynamic FFT 
# We use a 31-band visualizer, though the last two frequency bands are not shown
# The audio file is rendered in AudioRender.py

import pygame
from pygame import mixer

import AudioRender as Audio
import time
import numpy as np
import random
from Interpolate import Polynomial
 
class Renderer():
    def __init__(self,resolution=(900,720),fps=60,jump_fps=15):
        self.screen_size = resolution
        self.interpolate = Polynomial(steps=jump_fps,n=1)
        self.fps = fps
        self.jump_fps = jump_fps
        M = 1024  # Slice size

        # Load the song
        songName = "backstage.mp3"
        
        # Number of FFT bar groups
        self.num_groups = 100
        
        song = Audio.Audio_fft(songName, M=M,group_num=self.num_groups)
        
        self.max_amp = song.max_amp
        self.max_amp_raw = song.max_amp_raw

        # Initalise visualiser
        pygame.init()        
        # Initialize mixer
        pygame.mixer.quit()
        pygame.mixer.init(frequency=song.rate)
        pygame.mixer.music.load(songName)
        pygame.mixer.music.play(0)

        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
         
        # Close the program if the user clicks the close button
        done = False
        frame_count = 0
        
        prev_seconds = 0
        prev_ccc = np.array([0,0,0])

        while not done:
            frame_count += 1
            self.screen.fill(pygame.Color('white'))
            
            song_time = pygame.mixer.music.get_pos()

            for event in pygame.event.get():   
                if(event.type == 2):
                    mixer.pause()
                    time.sleep(2)
                    mixer.unpause()
                if event.type == pygame.QUIT:  
                    done = True   
              
            seconds = song_time/1000
            
            try:                    
                if frame_count == 1:
                    scale = int(np.floor(song.rate/M*seconds))
                    #print(prev_seconds,seconds)
                    prev_scale = int(np.floor(song.rate/M*(prev_seconds)))
                    slice_num = [M*(scale),M*(scale+1)]
                    #next_slice = [M*(next_scale),M*(next_scale+1)]
                    prev_slice = [M*(prev_scale),M*(prev_scale+1)]
                    #print(slice_num,next_slice)
                    
                    ccc = np.array([random.randint(0, 25),
                                    random.randint(0, 255),
                                    random.randint(0, 25)
                                    ])
                    #ccc = [25,25,25]
                    
                    curr_fft = song.get_fft(slice_num,grouped=True,localAvg=False)
                    prev_fft = song.get_fft(prev_slice,grouped=True,localAvg=False)
                    #print(curr_fft[-1],next_fft[-1])
                    inner_vals = self.interpolate.calc(prev_fft,curr_fft)
                    inner_cols = self.interpolate.calc(prev_ccc,ccc)
                    #print(inner_vals)
                    #print("\n\n")
                    prev_seconds = seconds
                    prev_ccc = ccc

            except ValueError:
                break
            
            try:
                #self.draw_fourier(song.get_fft(slice_num,grouped=True,localAvg=False),ccc)
                self.draw_fourier(inner_vals[frame_count-1],inner_cols[frame_count-1])
                self.draw_raw(song.get_wave(slice_num))
            except:
                pass
            # Titles on the screen
            FrequencyTitle = pygame.font.Font(None, 30).render("Frequency Spectrum of the Song", True, pygame.Color('black'))
            TimeTitle = pygame.font.Font(None, 30).render("Song Frequency", True, pygame.Color('black'))
            
            self.screen.blit(FrequencyTitle, (260, 320))
            self.screen.blit(TimeTitle, (320, 690))


            # Update the screen 
            pygame.display.flip()
            clock.tick(fps)
            if frame_count == jump_fps:
                frame_count = 0
        pygame.quit()

    def draw_fourier(self,data,c_colour=(20,20,20)):
        # Draw the 29 frequency bands
        
        s_width,s_height = self.screen_size
        
        left_top = (10,10)
        
        fourier_height = 300
        fourier_width = s_width - 2*left_top[0] - 2
        
        width_height = (fourier_width,fourier_height)
        bar_spacing = 1

        graph_col = (50,50,50)
                
        cols = [ c_colour for i in range(1,self.num_groups-2)]
        
        # Draw the box
        pygame.draw.rect(self.screen,(255,255,255),(left_top,width_height))
        pygame.draw.rect(self.screen,graph_col,(left_top,width_height),2)
    
        bar_w = (fourier_width-(self.num_groups+1)*bar_spacing)/(self.num_groups-3)
        for i in range(1,self.num_groups-2):
            if(data[i] >= 0):
                bar_h = data[i]
                box_x = left_top[0]+2+i*bar_spacing+(i-1)*(bar_w)
                if bar_h > width_height[1] - left_top[0]//2:
                    bar_h = width_height[1] - left_top[0]//2

                pygame.draw.rect(self.screen,cols[i-1],(int(box_x),
                                                      308,   
                                                      int(bar_w),
                                                      int(-bar_h))
                                 )
    
    def draw_raw(self, data):
        # Draw the raw music frequency

        left_top = (144,370)
        width_height = (512,300)

        pygame.draw.rect(self.screen,(255,255,255),(left_top,width_height))
        pygame.draw.rect(self.screen,(0,0,0),(left_top,width_height),2)
        
        dat = np.array(data)
        
        avg = np.mean(dat.reshape(-1, 4), axis=1)
        avg /= (self.max_amp_raw)
        
        num_els = len(avg)
        rec_w = int(width_height[0]/num_els)
        
        for i in range(num_els):
            pygame.draw.rect(self.screen,(0,0,0),(int(left_top[0]+i*rec_w),
                                                  int(left_top[1]+width_height[1]//2),
                                                  rec_w,
                                    int(-(width_height[1]//2)*avg[i]))
                             )

app = Renderer(fps=60,jump_fps=5)
