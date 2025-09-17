## Members
Phillip Bozzay, Electrical Engineering Student (2025)
phillipb23@vt.edu

## Mentor
N/A

## Current Status
STARTING 

## Project Overview


This is an extremely low cost DSP project for displaying the audio frequency spectrum on a grid of LEDs.

<img width="550" height="308" alt="image" src="https://github.com/user-attachments/assets/9b9a9174-8d4a-44c7-a234-b787b9473ce4" />
Inspiration: https://www.hackster.io/maxblack/diy-led-audio-spectrum-analyzer-fe8ba7

Goal: 
Pick up sound in a room and display the frequencies on a grid of leds.
Front end analog equipment for signal filtering/amplification 
Raspberry pi 2 for signal processing


## Educational Value Added
Digital signal processing on the pi (fft algorithm optimization, processing acceleration) 
  - Since I will be using a raspberry pi 2 for signal processing, this will probably need to be implemented in C
Digital filtering
  - Expecting an abundance of background noise, so will need to digitally account for this

Using I2S communication protocal

## Tasks


## Design Decisions
Addressable LEDs: BTF-LIGHTING WS2812B
Microphone: INMP441 -> connect directly to the pi 
Signal amplifier: LM381n -> Amplify analog audio signal before reaching the pi
Microcontroler: Raspberry pi 2 or 3 for signal processing, which I already have
<img width="1470" height="714" alt="image" src="https://github.com/user-attachments/assets/687a24eb-37db-4cf8-b11f-1c14cdd2a73b" />

## Design Misc

<!-- Your Text Here. You may work with your mentor on this later when they are assigned -->

## Steps for Documenting Your Design Process

<!-- Your Text Here. You may work with your mentor on this later when they are assigned -->

## BOM + Component Cost

<!-- Your Text Here. You may work with your mentor on this later when they are assigned -->

## Timeline

<!-- Your Text Here. You may work with your mentor on this later when they are assigned -->

## Useful Links

<!-- Your Text Here. You may work with your mentor on this later when they are assigned -->

## Log

<!-- Your Text Here. You may work with your mentor on this later when they are assigned -->



