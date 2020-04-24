import glob
import os
import time
import json
import pygetwindow as gw
import threading

class journal():
    def __init__(self):
        self.defaultPath = os.getenv('userprofile') + '\Saved Games\Frontier Developments\\Elite Dangerous\\*.log'
        self.journalAcess = False
        self.stop = False
        threading.Thread(target=self.lookForProcess).start()

    def lookForProcess(self):
        found = False
        while not self.stop :
            #check if active every 3 seconds
            time.sleep(3)

            if self.gameIsRunning():
                if not self.journalAcess:
                    print("game running")
                    self.getLatestJournal()
                continue
            else:
                print("game is not running")
                if self.journalAcess:
                    self.journalAcess = False
                    #give time for events()  to resolve
                    time.sleep(1.5)
                    self.logfile.close()

        #get here is stop was issue
        if self.journalAcess:
            #give time for events()  to resolve
            time.sleep(2)
            self.logfile.close()

    def gameIsRunning(self):
        windowTitles = gw.getAllTitles()
        for title in windowTitles:
            if "Elite - Dangerous" in title:
                return True
        return False

    def getLatestJournal(self):
        #listing files
        fileList = glob.glob(self.defaultPath)
        #get the lastet one
        logfile = max(fileList, key=os.path.getctime)
        if not os.path.exists(logfile):
            raise ValueError("No log file found")
        try:
            self.logfile = open(logfile)
        except (OSError, IOError) as e:
            print("can't read log file ",e)
            return

        self.cmdrName = self.getCmdrName()
        print("Cmdr Name : ", self.cmdrName)
        self.journalAcess = True
        print("journal hooked")

        #go to end of file
        self.logfile.seek(0, os.SEEK_END)

    def getCmdrName(self):
        #cmdr name should be in the first 10 lines
        for i in range(10):
            try:
                data = json.loads(self.logfile.readline())
            except ValueError as e:
                print("line was not json ",e)
                print(data)
                continue

            if data['event'] == "Commander":
                return data['Name']

        return "Unknown name"

    def events(self):
        while True:
            if self.journalAcess:
                line = self.logfile.readline()
                if not line:
                    time.sleep(1)
                    if self.stop:
                        return
                    else:
                        continue
                try:
                    decoded = json.loads(line)
                    yield decoded
                except ValueError as e:
                    print("line was not json ",e)
                    print(line)
                    continue
            else:
                if self.stop:
                    return
                time.sleep(2)
