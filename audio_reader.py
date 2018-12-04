from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
#
#M = 1024
#
#rate, audio = wavfile.read('nobody.wav')
#
#audio = np.mean(audio, axis=1)
#
#audio = audio[0*rate:round(0.5*rate)]
#
#N = audio.shape[0]
#L = N / rate
#
#print(f'Audio length: {L:.2f} seconds')
#
##f, ax = plt.subplots()
##ax.plot(np.arange(N) / rate, audio)
##ax.set_xlabel('Time [s]')
##ax.set_ylabel('Amplitude [unknown]');
#
#from scipy import signal
#
#freqs, times, Sx = signal.spectrogram(audio, fs=rate, window='hanning',
#                                      nperseg=1024, noverlap=M - 100,
#                                      detrend=False, scaling='spectrum')
#
#f, ax = plt.subplots(figsize=(4.8, 2.4))
#ax.pcolormesh(times, freqs / 1000, 10 * np.log10(Sx), cmap='viridis')
#ax.set_ylabel('Frequency [kHz]')
#ax.set_xlabel('Time [s]');


#rate, audio = wavfile.read('nobody.wav')
rate, audio = wavfile.read('test.wav')

# Average out the left and right channels
#audio = np.mean(audio, axis=1)

audio = audio[0:rate*6]/(2**15)

N = audio.shape[0]
L = N / rate

print(f'Audio length: {L:.2f} seconds')

# Plot whole song
f, ax = plt.subplots()
ax.plot(np.arange(N) / rate, audio)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Amplitude [unknown]');
from skimage import util

M = 2048

print("Creating slices")
slices = util.view_as_windows(audio, window_shape=(M,), step=100)
print(f'Audio shape: {audio.shape}, Sliced audio shape: {slices.shape}')

#win = np.hanning(M + 1)[:-1]
#slices = slices * win
#
#slices = slices.T
from scipy.fftpack import fft

spectrum = np.fft.fft(slices)
spectrum = fft(slices)
spectrum = np.abs(spectrum)/40

print('Shape of `slices`:', slices.shape)
freq_space = (rate / len(spectrum[0])/2)
print("Frequency spacing : ~{}Hz".format(freq_space))

plt.close() 

plt.plot(np.linspace(0,M*(freq_space+0.1),round(M/2)),spectrum[-1][0:1024])
plt.xlim(0,1024)
plt.xlabel("Frequency (Hz)")

# Get coefficients for different frequencies
#
## Generate frequencies 
#freqs = [0]
#max_freq = M/2
#while(max(freqs) + freq_space < max_freq):
#    freqs.append(max(freqs) + freq_space)
#    
## Split array
#separated_arrs = np.array_split(spectrum[0],len(freqs)*2)[0:len(freqs)]
## Workout averages
#means = []
#for i in separated_arrs:
#    means.append(np.mean(i))
#plt.close()    
#
#plt.plot(freqs,means)
#plt.xlim(0,500)
#
## Split array
#separated_arrs = np.array_split(spectrum[500],len(freqs)*2)[0:len(freqs)]
## Workout averages
#means = []
#for i in separated_arrs:
#    means.append(np.mean(i))   
#plt.plot(freqs,means)
