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
        if self.wheel == 0:
            self.audioLib = glob("audio/left/*.wav")
        else:
            self.audioLib = glob("audio/right/*.wav")
        
        self.numAudioFiles = len(self.audioLib)
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
                
                rndSound = randrange(0, self.numAudioFiles)
                if self.queueLock:
                    playing.stop()
                # make new audio obj
                audiofile = self.audioLib[rndSound]
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
        self.threshold = 1000

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


    def scale (self, x):
        y1 = 0
        y2 = 1
        return y1 + (y2 - y1)*x / 45000 


    def main(self):
        while self.running:
            # set up listening stream
            data = np.frombuffer(self.stream.read(self.CHUNK, exception_on_overflow=False), dtype=np.int16)

            # grab the RMS for left and right channels
            peakLeft = np.average(np.abs(data[0])) * 2 - self.threshold
            peakRight = np.average(np.abs(data[1])) * 2 - self.threshold

            if peakLeft > 0 and peakRight > 0:
     
            # change motor speed for each wheel depending on RMS
                if peakLeft > peakRight:
                    
                    bars = "#" * int(50 * peakLeft / 2 ** 16)
                    print("%05d  %s" % (peakLeft, bars))
                    right_speed = self.scale(peakLeft)
                    self.leftAudioQ.append(right_speed)

                    bars = "=" * int(50 * peakRight / 2 ** 16)
                    print("%05d  %s" % (0.5*peakRight, bars))
                    # round number to 1dp to avoid lots of
                    left_speed = 0.5*self.scale(peakRight)
                    # add to Right wheel audio Queue
                    self.rightAudioQ.append(left_speed)

                elif peakRight > peakLeft:

                    bars = "=" * int(50 * peakRight / 2 ** 16)
                    print("%05d  %s" % (peakRight, bars))
                    # round number to 1dp to avoid lots of
                    left_speed = self.scale(peakRight)
                    # add to Right wheel audio Queue
                    self.rightAudioQ.append(left_speed)
                    
                    bars = "#" * int(50 * peakLeft / 2 ** 16)
                    print("%05d  %s" % (0.5*peakLeft, bars))
                    right_speed = 0.5*self.scale(peakLeft)
                    self.leftAudioQ.append(right_speed)

                else:
                    if peakLeft > 0:
                        #2000
                        bars = "#" * int(50 * peakLeft / 2 ** 16)
                        print("%05d  %s" % (peakLeft, bars))
                        right_speed = self.scale(peakLeft)
                        #round(peakLeft / 10000, 1)
                        # add to Left wheel audio Queue
                        self.leftAudioQ.append(right_speed)

                    if peakRight > 0:
                        bars = "=" * int(50 * peakRight / 2 ** 16)
                        print("%05d  %s" % (peakRight, bars))
                        # round number to 1dp to avoid lots of
                        left_speed = self.scale(peakRight)
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