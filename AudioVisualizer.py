# Visualizes the rendered audio using Dynamic FFT 
# We use a 31-band visualizer, though the last two frequency bands are not shown

import pygame
import numpy
from pygame import mixer
import audio_reader2 as Audio
import time
 
class Renderer():
    def __init__(self,resolution=(800,720),fps=60):
        # Load the song
        song = Audio.Audio_fft("soft_cell.wav",True)
        
        # Initialize the visualizer
        pygame.init()
        sound = mixer.Sound("soft_cell.wav")
        mixer.init()
        sound.play() 
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(resolution)
        self.screen.fill(pygame.Color('white'))

         

        # Close the program if the user clicks the close button
        done = False
        frame=0
        while not done:
            for event in pygame.event.get(): 
                if(event.type == 2):
                    mixer.pause()
                    time.sleep(2)
                    mixer.unpause()
                if event.type == pygame.QUIT:  
                    done = True   

            try:
                self.draw_fourier(song.get_fft(7*frame,grouped=True,localAvg=True))
                self.draw_raw(song.get_wave(7*frame))
            except:
                break
                
            # Titles on the screen
            FrequencyTitle = pygame.font.Font(None, 30).render("Frequency Spectrum of the Song", True, pygame.Color('black'))
            TimeTitle = pygame.font.Font(None, 30).render("Song Frequency", True, pygame.Color('black'))
            
            self.screen.blit(FrequencyTitle, (260, 320))
            self.screen.blit(TimeTitle, (320, 690))


            # Update the screen 
            pygame.display.flip()
            clock.tick(60)
            frame += 1

    
    def draw_fourier(self,data):
        # Draw the 29 frequency bands
        
        pygame.draw.rect(self.screen,pygame.Color('black'),(10,10,780,300),2)
        
        for i in range(0,29): 
            if(data[i] >= 0):
                pygame.draw.rect(self.screen,pygame.Color('black'),(19+26.5*i,308,20,-1*295*data[i]))

    
    def draw_raw(self, data):
    # Draw the raw music frequency
        pygame.draw.rect(self.screen,pygame.Color('black'),(144,370,512,300),2)
        
        dat = numpy.array(data)        
        avg = numpy.mean(dat.reshape(-1, 4), axis=1)
        avg /= 2**15
        
        for i in range(len(avg)):
            pygame.draw.rect(self.screen,pygame.Color('black'),(144+i,540,2,-3*150*avg[i]))

app = Renderer(fps=30)
