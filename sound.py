import os
import threading
import glob
from playsound import playsound

class sound():
    def __init__(self):
        self.sound_file = os.path.dirname(os.path.realpath(__file__))
        self.sound_file += "/EliteProspecting2sound/*"
        fileList = glob.glob(self.sound_file)
        self.sound_file = fileList[0]
        print(fileList)

    def play(self):
        threading.Thread(target=self.playSound).start()

    def playSound(self):
        try:
            print("playing ",self.sound_file)
            playsound(self.sound_file)
        except Exception as e :
            print("there was an error playing sound file ", e, self.sound_file)
