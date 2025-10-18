import time
from rpi_ws281x import *
import argparse
import RPi.GPIO as GPIO
import numpy as np
import sounddevice as sd
from scipy.signal import iirnotch,butter, lfilter
# LED strip configuration:
LED_COUNT      = 256     # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 30      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

NUM_LEDS_PER_COL = 16
INPUT_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN)


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

sample_rate = 16000  
duration = 1       
channels = 1         
num_samples = 256

# Record audio
def record_data(duration):
    recording = sd.rec(num_samples, samplerate=sample_rate, channels=channels, dtype='float32', device=1)
    sd.wait()  # Wait until recording is finishedi
    data = recording.flatten().tolist()
    data = data[num_samples-64:]
    data = data[:32]
    return data

def light_column(row,height, colors=(255,0,0)):
    """FUnction to light up grid columns
    Row (0-15)
    height - 0-16 
    """
    #strip.setPixelColor(row*NUM_LEDS_PER_COL, (255,0,0))    
    if row % 2 ==0:
        for i in range((row*NUM_LEDS_PER_COL) +NUM_LEDS_PER_COL -1, (row*NUM_LEDS_PER_COL)+NUM_LEDS_PER_COL - height-1,-1):
            strip.setPixelColor(i, Color(colors[0],colors[1],colors[2]))
    else:
        for i in range(row*NUM_LEDS_PER_COL, (row*NUM_LEDS_PER_COL) + height):
            strip.setPixelColor(i, Color(colors[0],colors[1],colors[2]))
    strip.show()
    return
def value_to_color(val):
    """
    Maps values 1–16 to a more dramatic Green → Yellow → Orange → Red gradient.
    """
    val = max(1, min(16, val))  # Clamp to valid range

    if val <= 3:
        # Green (0,255,0) → Yellow (255,255,0)
        ratio = (val - 1) / 2
        r = int(255 * ratio)
        g = 255
        b = 0
    elif val <= 8:
        # Yellow (255,255,0) → Orange (255,165,0)
        ratio = (val - 4) / 4
        r = 255
        g = int(255 - (90 * ratio))  # from 255 to 165
        b = 0
    else:
        # Orange (255,165,0) → Red (255,0,0)
        ratio = (val - 9) / 7
        r = 255
        g = int(165 * (1 - ratio))  # from 165 to 0
        b = 0

    return (r, g, b)
def light_row(heights,colors=(255,0,0)):
    
    heights = heights[0:-1]
    zeros = [0] * 16
    while(sum(heights) >0): 
        for i in range(len(heights)):
            
            val = heights[i]
            if val == 0:
                continue 
            index = i*NUM_LEDS_PER_COL
            add = 1
            if i %2 ==0:
               index += NUM_LEDS_PER_COL -1
               add = -1
            colors = value_to_color(abs(zeros[i]))
            strip.setPixelColor(index+add*zeros[i],Color(colors[0],colors[1],colors[2]))
            heights[i] = heights[i] -1
            zeros[i] +=add
        strip.show()


def clear_grid():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
def notch_filter(data, fs, notch_freq=60.0, quality=5):
    # fs: sampling frequency
    # notch_freq: frequency to remove (60 Hz)
    # quality: Q factor (higher = narrower notch)

    b, a = iirnotch(w0=notch_freq, Q=quality, fs=fs)
    filtered_data = lfilter(b, a, data)
    return filtered_data
def butter_lowpass(cutoff, fs, order=4):
    nyquist = 0.5 * fs
    norm_cutoff = cutoff / nyquist
    b, a = butter(order, norm_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff=2000, fs=16000, order=4):
    b, a = butter_lowpass(cutoff, fs, order)
    y = lfilter(b, a, data)
    return y
def compute_fft(n):
    signal = record_data(0.1)
    fft_result = np.fft.rfft(signal)
    fft_freqs = np.fft.fftfreq(n,1/sample_rate)
    magnitude = np.abs(fft_result[:n//2])
    freqs = fft_freqs[:n//2]
    mag = np.array(magnitude)
    mag = mag/np.max(mag)
    mag = np.round(16*mag)
    return mag

while True:
    mags = compute_fft(num_samples)
    light_row(mags)

    clear_grid()
    #time.sleep(1)
