# Convert the audio file from mp3 to wav
# A wav is need for the visualization 
# 
# Change EXAMPLE with the desired mp3 file 

from pydub import AudioSegment
sound = AudioSegment.from_mp3("EXAMPLE.mp3")
sound.export("EXAMPLE.wav", format="wav")