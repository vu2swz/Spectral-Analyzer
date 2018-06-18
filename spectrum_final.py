import alsaaudio as aa
import wave
from struct import unpack
import numpy as np
import time

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

matrix    = [0,0,0,0,0,0]
power     = []
weighting = [2,8,8,16,32,64] 


# Return power array index corresponding to a particular frequency


def display():
   for i in range(0,6):
	for k in range(0,6):
	   if(k==i):
		GPIO.output(25-k,1)
	   else:
		GPIO.output(25-k,0)
	for j in range(1,14):
	   if(matrix[i]>j):
		GPIO.output(2+j,1)
	   else:
		GPIO.output(2+j,0)
        if(i!=5):
          time.sleep(0.005)

def piff(val):
   return int(2*chunk*val/sample_rate)
   
def calculate_levels(data, chunk,sample_rate):
   global matrix

   # Convert raw data (ASCII string) to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')

   # Apply FFT - real data
   fourier=np.fft.rfft(data)
   # Remove last element in array to make it the same size as chunk
   fourier=np.delete(fourier,len(fourier)-1)
   # Find average 'amplitude' for specific frequency ranges in Hz
   power = np.abs(fourier)
   optim_factor=2
   matrix[0]= (int(np.mean(power[piff(0)    :piff(270):1])))/optim_factor
   matrix[1]= (int(np.mean(power[piff(270)  :piff(313):1])))/optim_factor
   matrix[2]= (int(np.mean(power[piff(313)  :piff(625):1])))/optim_factor
   matrix[3]= (int(np.mean(power[piff(625)  :piff(1250):1])))/optim_factor
   matrix[4]= (int(np.mean(power[piff(1250) :piff(2500):1])))/optim_factor
   matrix[5]= (int(np.mean(power[piff(2500) :piff(20000):1])))/optim_factor

   # Tidy up column values for the LED matrix
   matrix=np.divide(np.multiply(matrix,weighting),1000000)
   # Set floor at 0 and ceiling at 8 for LED matrix
   matrix=matrix.clip(0,14)
   if(matrix[5]>6):
     matrix[5]=6
   return matrix


songs=[""] # Array of songs (.wav)
while(True):
  for i in range (0,len(songs):
    song_name="/home/pi/Documents/songs/"+songs[i]

# Audio setup
    wavfile = wave.open(song_name,'r')
    sample_rate = wavfile.getframerate()
    no_channels = wavfile.getnchannels()
    chunk       = 4096 # Use a multiple of 8
    # ALSA
    output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
    output.setchannels(no_channels)
    output.setrate(sample_rate)
    output.setformat(aa.PCM_FORMAT_S16_LE)
    output.setperiodsize(chunk)

    # Start reading .wav file  
    data = wavfile.readframes(chunk)
    # Loop while audio data present
    while data!='':
        output.write(data)   
        matrix=calculate_levels(data, chunk,sample_rate)
        #print matrix
        display()
        data = wavfile.readframes(chunk)
   
