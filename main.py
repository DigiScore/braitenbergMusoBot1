# import python libs
import sys
from threading import Thread, Timer
from random import randrange
from time import time

# import project libs
from audioEngine import AudioEngine
from ai_engine import AiDataEngine

# class Director:
#     """controls the overall behaviour and timing"""
#
#     def __init__(self):
#         # logs start time in seconds
#         startTime = time()
#
#         # todo - this is a wizard-of-oz HACK
#         # todo - need to implement the 2 audio analysis transistions
#
#         # 1) global form starts at 1
#         self.globalForm = 1
#
#         # 2) transition into B section starts at 6 mins
#         # triggered by density clouds of short attacks from Carla
#         self.transA = startTime + 360
#
#         # 3) section B must start before 8 mins or when triggered by Carla
#         self.sectionB = self.transA + randrange(20, 60) # startTime + 480
#
#         # 4) transition into C section starts after 30"
#         # trans triggered by low C held note
#         self.transC = self.sectionB + 30
#
#         # 5) section C must start by 11 mins
#         self.sectionC = self.transC + randrange(30, 150) # startTime + 660
#         # self.pitchChange = "low"
#
#         # 6) end section (ascension) must start at 14 mins
#         self.endSection = startTime + 840
#         # self.triggerEndFade = False
#
#         # 7) piece ends at 16 mins
#         self.end = startTime + 960
#
#     def conductor(self):
#         """controls the overall behaviour and timing"""
#
#         # determime which section we are in
#         # get now time
#         nowTime = time()
#
#         # are we at the end of the piece?
#         if nowTime >= self.end:
#             self.globalForm = 7
#             print("\t\t\t\tFinsihed")
#
#         # last section (ascension)
#         elif nowTime >= self.endSection:
#             # self.triggerEndFade = True
#             self.globalForm = 6
#             print("\t\t\t\tAscension")
#
#         elif nowTime >= self.sectionC:
#             # self.pitchChange = "high"
#             self.globalForm = 5
#             print("\t\t\t\tSection C")
#
#         elif nowTime >= self.transC:
#             # self.pitchChange = "norm"
#             self.globalForm = 4
#             print("\t\t\t\tTransition to Section C")
#
#         elif nowTime >= self.sectionB:
#             self.globalForm = 3
#             print("\t\t\t\tSection B")
#
#         elif nowTime >= self.transA:
#             self.globalForm = 2
#             print("\t\t\t\tTransition to Section B")


class Main:
    """start all the data threading
     pass it the master signal class for emmission"""

    def __init__(self):
        # instantiate the AI server
        engine = AiDataEngine(speed=0.1)

        # # instantiate the dircetor
        # aiDirector = Director()

        # instantiate the controller client and pass it te queue
        audioEngine = AudioEngine(engine)

        # declares all threads and starts the piece
        t1 = Thread(target=engine.make_data)
        t2 = Thread(target=engine.affect)
        t3 = Thread(target=audioEngine.snd_listen)

        # # starts the conductor
        # t4 = Timer(interval= 1, function=aiDirector.conductor)

        # assigns them all daemons
        t1.daemon = True
        t2.daemon = True
        # t3.daemon = True

        # starts them all
        t1.start()
        t2.start()
        t3.start()
        # t4.start()


if __name__ == "__main__":
    go = Main()
