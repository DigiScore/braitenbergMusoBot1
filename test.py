import numpy as np
import pyaudio
from glob import glob
from queue import Queue
from threading import Thread
from random import randrange
import simpleaudio


audioLib = glob("audio/*.wav")
numAudioFiles = len(audioLib)

while True:
    rndSound = randrange(0, numAudioFiles)

    audiofile = audioLib[rndSound]
    player = simpleaudio.WaveObject.from_wave_file(audiofile)
    print(f'{id} is playing {audiofile}')
    playing = player.play()