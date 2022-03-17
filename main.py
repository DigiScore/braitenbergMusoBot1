# get python libraries
import numpy as np
import pyaudio
from glob import glob
from queue import Queue
from threading import Thread

class Audioplayer:
    def __init__(self, queueName):
        print(id)
        self.audioLib = glob("audio/*.wav")

    def makeSound(self):
        """a seperate thread """
        pass
    # if queuename > 0:
    # make sound
    # BUT replace with FIFO items in queuename

class BBBot1:
    def __init__(self, robot=False):
        # own the robot
        self.robot = robot
        if self.robot:
            from robot import robot
            self.jetbot = robot.Robot()

        # set up mic listening funcs
        running = True
        self.CHUNK = 2 ** 11
        self.RATE = 44100
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16,
                                          channels=2,
                                          rate=self.RATE,
                                          input=True,
                                          frames_per_buffer=self.CHUNK)

        # set up audio functions
        self.leftAudioQ = Queue()
        self.rightAudioQ = Queue()
        self.leftAudioBot = Audioplayer(self.leftAudioQ)
        self.rightAudioBot = Audioplayer(self.rightAudioQ)
        tLeft = Thread(target=self.leftAudioBot.makeSound)
        tRight = Thread(target=self.rightAudioBot.makeSound)
        tLeft.start()
        tRight.start()

        # set the ball running
        self.running = True

    def main(self):
        while self.running:
            # set up listening stream
            data = np.frombuffer(self.stream.read(self.CHUNK,
                                                  exception_on_overflow=False),
                                 dtype=np.int16)

            # grab the RMS for left and right channels
            peakLeft = np.average(np.abs(data[0])) * 2
            peakRight = np.average(np.abs(data[1])) * 2

            # change motor speed for each wheel depending on RMS
            if peakLeft > 2000:
                bars = "#" * int(100 * peakLeft / 2 ** 16)
                print("%05d %s" % (peakLeft, bars))
                right_speed = round(peakLeft / 10000, 1)
                # add to Left wheel audio Queue
                self.leftAudioQ.put(right_speed)

            if peakRight > 2000:
                bars = "=" * int(100 * peakRight / 2 ** 16)
                print("%05d %s" % (peakRight, bars))
                # round number to 1dp to avoid lots of
                left_speed = round(peakRight / 10000, 1)
                # add to Right wheel audio Queue
                self.rightAudioQ.put(left_speed)

            else:
                left_speed = 0
                right_speed = 0

            # send the command to the robot wheels
            if self.robot:
                self.jetbot.set_motors(left_speed, right_speed)



if __name__ == "__main__":
    bot = BBBot1(robot = True)
    bot.main()