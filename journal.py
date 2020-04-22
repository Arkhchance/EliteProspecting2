import glob
import os
import time
import json

class journal():
    def __init__(self):
        self.defaultPath = os.getenv('userprofile') + '\Saved Games\Frontier Developments\\Elite Dangerous\\*.log'

        #listing files
        list_of_files = glob.glob(self.defaultPath)
        #get the lastet one
        logfile = max(list_of_files, key=os.path.getctime)
        if not os.path.exists(logfile):
            raise ValueError("No log file found")

        try:
            self.logfile = open(logfile)
        except (OSError, IOError) as e:
            print("can't read log file ",e)

        self.stop = False
        self.cmdrName = self.getCmdrName()

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
        # seek the end of the file
        self.logfile.seek(0, os.SEEK_END)

        while True:
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
