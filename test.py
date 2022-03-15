# get python libraries
import numpy as np
import pyaudio


class BBBot1:
    def __init__(self, robot=False):
        # own the robot
        self.robot = robot
        if self.robot:
            from jetbot import Robot
            self.jetbot = Robot()

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

        self.running = True


    def main(self):
        while self.running:
            # set up listening stream
            data = np.frombuffer(self.stream.read(self.CHUNK,
                                                  exception_on_overflow=False),
                                 dtype=np.int16)
            peakLeft = np.average(np.abs(data[0])) * 2
            peakRight = np.average(np.abs(data[1])) * 2

            # do stuff with this data
            if peakLeft > 2000:
                bars = "#" * int(50 * peakLeft / 2 ** 16)
                print("%05d %s" % (peakLeft, bars))
                left_speed = peakLeft / 10000

            if peakRight > 2000:
                bars = "=" * int(50 * peakRight / 2 ** 16)
                print("%05d %s" % (peakRight, bars))
                right_speed = peakRight / 10000

            else:
                left_speed = 0
                right_speed = 0

            # send the command to the robot wheels
            if self.robot:
                self.jetbot.set_motors(left_speed, right_speed)


if __name__ == "__main__":
    bot = BBBot1(robot = False)
    bot.main()