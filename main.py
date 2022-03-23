import numpy as np
import pyaudio
from glob import glob
from threading import Thread
from random import randrange
import simpleaudio
from time import sleep

class Audioplayer:
    def __init__(self, queueName, wheel):
        print(f'Audioplayer {wheel} is [a]live')
        self.wheel = wheel
        #self.audioLib = glob("audio/*.wav")
        self.leftAudiolib = glob("audio/left/*.wav")
        self.rightAudiolib = glob("audio/right/*.wav")
        self.leftNumFiles = len(self.leftAudiolib)
        self.rightNumFiles = len(self.rightAudiolib)
        #self.numAudioFiles = len(self.audioLib)
        # own queue
        self.audioQueue = queueName
        self.queueLock = False
        # start thread
        thd = Thread(target=self.makeSound)
        thd.start()

    def makeSound(self):
        while True:
            if len(self.audioQueue) > 0: 
                _dummy = self.audioQueue.pop(0)
                if self.wheel == 0:
                    rndSound = randrange(0, self.leftNumFiles)
                    audiofile = self.leftAudiolib[rndSound]
                else:
                    rndSound = randrange(0, self.rightNumFiles) 
                    audiofile = self.rightAudiolib[rndSound]
                if self.queueLock:
                    playing.stop()
                # make new audio obj
                player = simpleaudio.WaveObject.from_wave_file(audiofile)
                playing = player.play()
                self.queueLock = True
            else:
                sleep(0.1)

class BBBot1:
    def __init__(self, robot=False):
        # own the robot
        self.robot = robot
        if self.robot:         # todo - delete this once beta tested
            from robot import robot
            self.jetbot = robot.Robot()

        # set up mic listening funcs
        running = True
        self.CHUNK = 2 ** 11
        self.RATE = 44100
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16, channels=2, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        # set up audio functions
        self.leftAudioQ = [] #Queue(maxsize=1)
        self.leftAudioBot = Audioplayer(self.leftAudioQ, 0)

        self.rightAudioQ = [] #Queue(maxsize=1)
        self.rightAudioBot = Audioplayer(self.rightAudioQ, 1)

        # set the ball running
        self.running = True

    def main(self):
        while self.running:
            # set up listening stream
            data = np.frombuffer(self.stream.read(self.CHUNK, exception_on_overflow=False), dtype=np.int16)

            # grab the RMS for left and right channels
            peakLeft = np.average(np.abs(data[0])) * 2
            peakRight = np.average(np.abs(data[1])) * 2

            
            # change motor speed for each wheel depending on RMS
            if peakLeft > 2000:
                bars = "#" * int(50 * peakLeft / 2 ** 16)
                print("%05d  %s" % (peakLeft, bars))
                right_speed = round(peakLeft / 10000, 1)
                # add to Left wheel audio Queue
                self.leftAudioQ.append(right_speed)

            elif peakRight > 2000:
                bars = "=" * int(50 * peakRight / 2 ** 16)
                print("%05d  %s" % (peakRight, bars))
                # round number to 1dp to avoid lots of
                left_speed = round(peakRight / 10000, 1)
                # add to Right wheel audio Queue
                self.rightAudioQ.append(left_speed)
            
            else:
                left_speed = 0
                right_speed = 0

            # send the command to the robot wheels
            if self.robot:
                self.jetbot.set_motors(left_speed, right_speed)

if __name__ == "__main__":
    bot = BBBot1(robot = False)
    bot.main()