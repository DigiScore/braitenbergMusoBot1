# get python libraries
import numpy as np
import pyaudio
from glob import glob

class BBBot1:
    def __init__(self, robot=False):
        # own the jetbot
        self.robot = robot
        if self.robot:
            from jetbot import robot
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

        # set up audio library
        self.audioLib = glob("audio/*.wav")

        # set the ball running
        # todo - replace with threading once we get the audio engine working
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

            if peakRight > 2000:
                bars = "=" * int(100 * peakRight / 2 ** 16)
                print("%05d %s" % (peakRight, bars))
                # round number to 1dp to avoid lots of
                left_speed = round(peakRight / 10000, 1)

            else:
                left_speed = 0
                right_speed = 0

            # send the command to the jetbot wheels
            if self.robot:
                self.jetbot.set_motors(left_speed, right_speed)

    def makeSound(self):
        pass

if __name__ == "__main__":
    bot = BBBot1(robot = True)
    bot.main()