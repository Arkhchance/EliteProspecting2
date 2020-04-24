import os
import threading
import glob
from playsound import playsound

class sound():
    def __init__(self):
        self.sound_file = os.getcwd() + "/EliteProspecting2sound/*"
        fileList = glob.glob(self.sound_file)
        self.isFile = True
        try:
            self.sound_file = fileList[0]
        except IndexError :
            print("no file found")
            self.isFile = False

    def play(self):
        if self.isFile:
            threading.Thread(target=self.playSound).start()

    def playSound(self):
        try:
            playsound(self.sound_file)
        except Exception as e :
            print("there was an error playing sound file ", e, self.sound_file)
