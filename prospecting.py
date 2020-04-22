import tkinter as tk
import threading
import hashlib
import json
import time
from config import config
from journal import journal
from communication import comm
from sound import sound

class application():

    def __init__(self,master,config):
        #display options
        row = 2
        PADX = 10
        PADY = 3

        self.totalMsg = 0
        self.messages = []
        self.hashlist = []
        self.colors = []
        self.config = config
        self.run = True
        self.connected = False
        self.soundplayer = sound()

        try:
            self.journal = journal()
        except ValueError as e :
            print(e)
            quit()


        #setup ui
        self.w = master
        self.w.title("EliteProspecting")
        self.w.protocol("WM_DELETE_WINDOW", self.closing)
        self.w.resizable(False,False)
        self.tLtd = tk.IntVar(value=self.config.config['mining']['track_ltd'])
        self.tPainite = tk.IntVar(value=self.config.config['mining']['track_painite'])
        self.sound = tk.IntVar(value=self.config.config['ui']['sound'])
        self.trans = tk.IntVar(value=self.config.config['ui']['transparency'])

        self.ipLabel = tk.Label(self.w,text="Server IP")
        self.ipAddr = tk.Entry(self.w)
        self.ipLabel.grid(row=row,padx=PADX,sticky=tk.W)
        self.ipAddr.grid(row=row,column=1,padx=PADX,pady=PADY,sticky=tk.EW)

        row += 1
        self.portLabel = tk.Label(self.w, text="Server Port")
        self.port  = tk.Entry(self.w)
        self.portLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.port.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.roomLabel = tk.Label(self.w,text="Server Room")
        self.room = tk.Entry(self.w)
        self.roomLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.room.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.myColorLabel = tk.Label(self.w,text="My Color")
        self.myColor = tk.Entry(self.w)
        self.myColorLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.myColor.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.otherColorLabel = tk.Label(self.w,text="Other's Color")
        self.otherColor = tk.Entry(self.w)
        self.otherColorLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.otherColor.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.fontLabel = tk.Label(self.w,text="Font size")
        self.font = tk.Entry(self.w)
        self.fontLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.font.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.lineLabel = tk.Label(self.w,text="Lines number")
        self.line = tk.Entry(self.w)
        self.lineLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.line.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.ltdCB = tk.Checkbutton(self.w,text='track LDT greater that',variable=self.tLtd)
        self.ltdCB.grid(row=row, padx=PADX, pady=PADY, sticky=tk.W)
        self.ltdThreshold = tk.Entry(self.w)
        self.ltdThreshold.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.painiteCB = tk.Checkbutton(self.w,text='track painite greater that',variable=self.tPainite)
        self.painiteCB.grid(row=row, padx=PADX, pady=PADY, sticky=tk.W)
        self.painiteThreshold = tk.Entry(self.w)
        self.painiteThreshold.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.soundCB = tk.Checkbutton(self.w,text='Play a sound when threshold is met',variable=self.sound)
        self.soundCB.grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.W)

        row += 1
        self.transB = tk.Checkbutton(self.w,text='Make overlay transparent',variable=self.trans)
        self.transB.grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.W)

        row += 1
        self.settings = tk.Button(self.w, text="save settings", command=self.saveSettings)
        self.settings.grid(row=row, padx=PADX, pady=PADY, sticky=tk.W)

        row += 1
        self.onlineB = tk.Button(self.w, text="Go Online", command=self.connect)
        self.onlineLabel = tk.Label(self.w,text="Offline")
        self.onlineB.grid(row=row, padx=PADX, pady=PADY, sticky=tk.W)
        self.onlineLabel.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        self.loadConf()
        self.loadSetup()
        self.setupUi()

        self.processThread = threading.Thread(target=self.processEvents)
        self.processThread.start()

        self.networkThread = threading.Thread(target=self.receiveMsg)
        self.networkThread.start()

    def setupUi(self):
        try:
            self.wr.destroy()
        except AttributeError as e:
            print("window was not created yet")

        self.wr = tk.Toplevel()
        self.wr.wm_attributes("-topmost", True)
        self.wr.overrideredirect(True)
        self.wr.configure(background='black')
        self.wr.bind("<ButtonPress-1>", self.startMove)
        self.wr.bind("<B1-Motion>", self.dragging)
        self.wr.bind("<ButtonRelease-1>", self.stopMove)
        self.wr.wm_geometry('+' + str(self.config.config['ui']['pos_x']) + '+' + str(self.config.config['ui']['pos_y']))
        #transparency
        if self.config.config['ui']['transparency'] == "1":
            self.wr.attributes("-transparentcolor", 'black')

        for i in range(self.totalMsgDisplay):
            self.status[i] = tk.Label(self.wr, text="", foreground="yellow")
            self.status[i].config(font=("Courier", int(self.font.get())),background='black')
            self.status[i].pack(side="top", fill="both", expand=True, padx=10, pady=10)
            if i == 0:
                self.status[i]['text'] = "Waiting..."
        self.refreshDisplay()

    def startMove(self,event):
        self.posX = event.x
        self.posY = event.y

    def stopMove(self,event):
        self.config.changeConf("ui","pos_x",self.wr.winfo_x())
        self.config.changeConf("ui","pos_y",self.wr.winfo_y())
        self.config.configSave()
        self.posX = None
        self.posY = None

    def dragging(self,event):
        deltax = event.x - self.posX
        deltay = event.y - self.posY
        x = self.wr.winfo_x() + deltax
        y = self.wr.winfo_y() + deltay
        self.wr.wm_geometry('+' + str(x) + '+' + str(y))

    def saveSettings(self):
        #bit of sanity check
        if len(self.room.get()) > 20:
            room = "default"
        else:
            room = self.room.get()
        try:
            int(self.port.get())
            port = self.port.get()
        except ValueError:
            port = "44988"

        self.config.changeConf("server","ip",self.ipAddr.get())
        self.config.changeConf("server","port",port)
        self.config.changeConf("server","room",room)
        self.config.changeConf("ui","text_color",self.myColor.get())
        self.config.changeConf("ui","text_other_color",self.otherColor.get())
        self.config.changeConf("ui","font_size",self.font.get())
        self.config.changeConf("ui","sound",self.sound.get())
        self.config.changeConf("ui","total_message",self.line.get())
        self.config.changeConf("ui","transparency",self.trans.get())
        self.config.changeConf("mining","ltd_t",self.ltdThreshold.get())
        self.config.changeConf("mining","painite_t",self.painiteThreshold.get())
        self.config.changeConf("mining","track_ltd",self.tLtd.get())
        self.config.changeConf("mining","track_painite",self.tPainite.get())

        self.config.configSave()
        self.loadSetup()
        self.setupUi()

    def updateWin(self,val):
        print(val)
        self.posX = self.winX.get()
        self.posY = self.winY.get()
        self.wr.wm_geometry('+' + str(self.posX) + '+' + str(self.posY))

    def connect(self):
        if not self.connected:
            self.comm = comm(self.config)
            self.connected = True
            self.onlineB['text'] = "Go offline"
            self.onlineLabel['text'] = "Online"
        else:
            self.connected = False
            time.sleep(0.2)
            self.comm.stop()
            self.onlineB['text'] = "Go online"
            self.onlineLabel['text'] = "Offline"

    def loadSetup(self):
        #setup variable
        self.totalMsgDisplay = int(self.config.config['ui']['total_message'])
        self.status = [None] * self.totalMsgDisplay

    def loadConf(self):
        #load from config file
        self.ipAddr.insert(0,self.config.config['server']['ip'])
        self.port.insert(0,self.config.config['server']['port'])
        self.room.insert(0,self.config.config['server']['room'])
        self.myColor.insert(0,self.config.config['ui']['text_color'])
        self.otherColor.insert(0,self.config.config['ui']['text_other_color'])
        self.font.insert(0,self.config.config['ui']['font_size'])
        self.ltdThreshold.insert(0,self.config.config['mining']['ltd_t'])
        self.painiteThreshold.insert(0,self.config.config['mining']['painite_t'])
        self.line.insert(0,self.config.config['ui']['total_message'])

    def refreshDisplay(self):
            for i in range(len(self.messages)):
                if self.colors[i] == "mine":
                    color = self.config.config['ui']['text_color']
                else:
                    color = self.config.config['ui']['text_other_color']
                self.status[i].config(foreground=color)
                self.status[i]['text'] = self.messages[i]

    def displayMsg(self, msg, mine=True):
        if mine:
            color = "mine"
        else:
            color = "other"

        self.colors.append(color)
        self.messages.append(msg)
        self.totalMsg += 1

        if self.totalMsg > self.totalMsgDisplay:
            self.messages.pop(0)
            self.colors.pop(0)
            self.totalMsg -= 1

        self.refreshDisplay()


    def processEvents(self):
        for entry in self.journal.events():
            if not self.run:
                return
            if entry['event'] == "ProspectedAsteroid":
                #we have winneer
                self.processMat(entry)


    def processMat(self,entry):
        empty = True
        belowT = False

        #hash material to easly find duplicate between wings mate
        matHash = hashlib.md5(json.dumps(entry["Materials"]).encode()).hexdigest()

        if matHash in self.hashlist:
            print("duplicate")
            self.displayMsg("Asteroid already prospected")
            return
        else:
            self.hashlist.append(matHash)
        print("check mats")
        #check for materials
        for mat in entry['Materials']:
            if mat['Name'] == "LowTemperatureDiamond" and self.config.config['mining']['track_ltd'] == "1" :
                if mat['Proportion'] > float(self.config.config['mining']['ltd_t']):
                    self.publish(mat['Name_Localised'], mat['Proportion'], matHash)
                else:
                    belowT = True
                empty = False
            elif mat['Name'] == "Painite" and self.config.config['mining']['track_painite']  == "1" :
                if mat['Proportion'] > float(self.config.config['mining']['painite_t']):
                    self.publish("Painite", mat['Proportion'], matHash)
                else:
                    belowT = True
                empty = False

        if empty and not belowT:
            self.displayMsg("Asteroid without materials")
        if belowT:
            self.displayMsg("Threshold not met")

    def publish(self, name, prop, hash):
        data = name + " {:.2f}%"
        data = data.format(prop)

        message = {
            "cmdr" : self.journal.cmdrName,
            "data" : data,
            "hash" : hash,
            "room" : self.config.config['server']['room']
        }
        #send here to network
        if self.connected :
            self.comm.sendMsg(message)

        self.playsound()
        msg = self.journal.cmdrName + " " + name + " {:.2f}%"
        self.displayMsg(msg.format(prop))

    def receiveMsg(self):
        while self.run:
            if self.connected:
                reception = self.comm.rcvMsg()
                try:
                    if reception['room'] != self.config.config['server']['room'] or reception['cmdr'] == self.journal.cmdrName:
                        continue
                    self.processMsg(reception)
                except ValueError as e:
                    print("Bad formating ",e)
            else:
                time.sleep(0.5)

    def processMsg(self,msg):
        message = msg['cmdr']
        hash = msg['hash']

        if hash in self.hashlist:
            message += " duplicate"
            self.displayMsg(message,False)
            return

        self.hashlist.append(hash)
        self.playsound()

        message += " " + msg['data']
        self.displayMsg(message,False)

    def playsound(self):
        print("play sound")
        if self.config.config['ui']['sound'] == "1":
            self.soundplayer.play()

    def closing(self):
        self.run = False
        self.journal.stop = True
        self.w.destroy()
        time.sleep(1)
        quit()

def main():
    myconf = config()
    root = tk.Tk()
    app = application(root,myconf)
    root.mainloop()


if __name__ == "__main__":
    # execute only if run as a script
    main()
