# Render the audio of the wav file
# The rendered audio is then visualized in AudioVisualizer.py


from scipy.io import wavfile
import numpy as np
from scipy.fftpack import fft
from pydub import AudioSegment

class Audio_fft():
    def __init__(self, filename,M=2048,group_num=16):
        self.song = AudioSegment.from_file(filename)
        
        self.rate, self.audio = wavfile.read(filename)
        
        self.M = M
        self.max_amp_raw = self.song.max_possible_amplitude
        self.max_amp = 2**(np.log2(self.max_amp_raw)*1.05)

        
        # Average out the left and right channels        
        if len(self.audio.shape) != 1:
            self.audio = np.mean(self.audio, axis=1)

        N = self.audio.shape[0]
        L = N / self.rate
        
        self.num_groups = group_num
        self.groups = self.gen_groups(group_num)        
        
    def gen_groups(self,num_groups):
        step_size = 1/num_groups
        out = []
        for i in range(num_groups):
            out.append(15.877*np.exp(i*step_size*7.1274))
        return out
                
    def get_fft(self,slice_num, group_num=16,song_time=0, get_freq_space=False,
                grouped=True,localAvg=False):
        
        samples = self.song[song_time:song_time+1].get_array_of_samples()
        song_slice = self.audio[slice_num[0]:slice_num[1]]
        spectrum = fft(song_slice)

        # Remove the second half, since the FFT of real frequencies is symmetric
        spectrum = np.abs(spectrum)[:self.M//2]  
        _spectrum = fft(samples)

        self.freq_space = (self.rate / self.M/2)
        
        # Return not grouped fft
        if(not grouped):
            return spectrum

        # Split array
        pos = 0
        separated_arrs = [0]*self.num_groups
        
        for i in range(self.M//2):
            if(self.groups[pos] <= (i+1)*self.freq_space):
                pos += 1
            separated_arrs[pos] += spectrum[i]


        # for i in range(len(_spectrum)//2):
        #     if(self.groups[pos] <= (i+1)*self.freq_space):
        #         pos += 1
            
            #print(len(_spectrum),i,self.M//2)
            # separated_arrs[pos] += _spectrum[i]
           
        if not localAvg:
            separated_arrs = np.nan_to_num(np.array(separated_arrs))
            return separated_arrs / (self.max_amp)
             
        
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
