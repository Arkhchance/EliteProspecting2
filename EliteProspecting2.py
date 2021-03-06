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
        PADX = 8
        PADY = 3

        self.totalMsg = 0
        self.messages = []
        self.hashlist = []
        self.cargoCount = "0"
        self.colors = []
        self.config = config
        self.run = True
        self.connected = False
        self.soundplayer = sound()
        self.checkBoxes = []
        self.entryStatList = ["ProspectedAsteroid","StartJump","SupercruiseExit"]
        try:
            self.journal = journal()
        except ValueError as e :
            print(e)
            quit()


        #setup ui
        backgroundColor = self.config.config['ui_colors']['backgroundColor']
        textColor = self.config.config['ui_colors']['textColor']
        boxColor = self.config.config['ui_colors']['boxColor']
        boxTextColor = self.config.config['ui_colors']['boxTextColor']

        self.w = master
        self.w.title("EliteProspecting")
        self.w.protocol("WM_DELETE_WINDOW", self.closing)
        self.w.bind("<Return>",self.saveSettings)
        self.w.resizable(False,False)
        self.w.configure(background=backgroundColor)
        self.tLtd = tk.IntVar(value=self.config.config['mining']['track_ltd'])
        self.tPainite = tk.IntVar(value=self.config.config['mining']['track_painite'])
        self.sound = tk.IntVar(value=self.config.config['ui']['sound'])
        self.trans = tk.IntVar(value=self.config.config['ui']['transparency'])
        self.collect = tk.IntVar(value=self.config.config['server']['collect'])
        self.onlineD = tk.IntVar(value=self.config.config['ui']['online'])
        self.overlay = tk.IntVar(value=self.config.config['ui']['show_overlay'])
        self.cargo = tk.IntVar(value=self.config.config['mining']['track_cargo'])

        self.ipLabel = tk.Label(self.w,text="Server IP",background=backgroundColor,foreground=textColor)
        self.ipAddr = tk.Entry(self.w,background=boxColor,foreground=boxTextColor)
        self.ipLabel.grid(row=row,padx=PADX,sticky=tk.W)
        self.ipAddr.grid(row=row,column=1,padx=PADX,pady=PADY,sticky=tk.EW)

        row += 1
        self.portLabel = tk.Label(self.w, text="Server Port",background=backgroundColor,foreground=textColor)
        self.port  = tk.Entry(self.w,background=boxColor,foreground=boxTextColor)
        self.portLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.port.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.roomLabel = tk.Label(self.w,text="Server Room",background=backgroundColor,foreground=textColor)
        self.room = tk.Entry(self.w,background=boxColor,foreground=boxTextColor)
        self.roomLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.room.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.myColorLabel = tk.Label(self.w,text="My Color",background=backgroundColor,foreground=textColor)
        self.myColor = tk.Entry(self.w,background=boxColor,foreground=boxTextColor)
        self.myColorLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.myColor.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.otherColorLabel = tk.Label(self.w,text="Other's Color",background=backgroundColor,foreground=textColor)
        self.otherColor = tk.Entry(self.w,background=boxColor,foreground=boxTextColor)
        self.otherColorLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.otherColor.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.fontLabel = tk.Label(self.w,text="Font size",background=backgroundColor,foreground=textColor)
        self.font = tk.Entry(self.w,background=boxColor,foreground=boxTextColor)
        self.fontLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.font.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.lineLabel = tk.Label(self.w,text="Lines number",background=backgroundColor,foreground=textColor)
        self.line = tk.Entry(self.w,background=boxColor,foreground=boxTextColor)
        self.lineLabel.grid(row=row, padx=PADX, sticky=tk.W)
        self.line.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

        row += 1
        self.ltdCB = tk.Checkbutton(self.w,text='Track LDT greater than',variable=self.tLtd,background=backgroundColor,foreground=textColor,command=self.onCheck)
        self.ltdCB.grid(row=row, padx=PADX, pady=PADY, sticky=tk.W)
        self.ltdThreshold = tk.Entry(self.w,background=boxColor,foreground=boxTextColor)
        self.ltdThreshold.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)
        self.checkBoxes.append((self.ltdCB,self.tLtd))

        row += 1
        self.painiteCB = tk.Checkbutton(self.w,text='Track painite greater than',variable=self.tPainite,background=backgroundColor,foreground=textColor,command=self.onCheck)
        self.painiteCB.grid(row=row, padx=PADX, pady=PADY, sticky=tk.W)
        self.painiteThreshold = tk.Entry(self.w,background=boxColor,foreground=boxTextColor)
        self.painiteThreshold.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)
        self.checkBoxes.append((self.painiteCB,self.tPainite))

        row += 1
        self.cargoB = tk.Checkbutton(self.w,text='Track my cargo',variable=self.cargo,background=backgroundColor,foreground=textColor,command=self.onCheck)
        self.cargoB.grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.W)
        self.checkBoxes.append((self.cargoB,self.cargo))

        row += 1
        self.soundCB = tk.Checkbutton(self.w,text='Play a sound when threshold is met',variable=self.sound,background=backgroundColor,foreground=textColor,command=self.onCheck)
        self.soundCB.grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.W)
        self.checkBoxes.append((self.soundCB,self.sound))

        row += 1
        self.overlayB = tk.Checkbutton(self.w,text='Show overlay',variable=self.overlay,background=backgroundColor,foreground=textColor,command=self.onCheck)
        self.overlayB.grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.W)
        self.checkBoxes.append((self.overlayB,self.overlay))

        row += 1
        self.transB = tk.Checkbutton(self.w,text='Make overlay transparent',variable=self.trans,background=backgroundColor,foreground=textColor,command=self.onCheck)
        self.transB.grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.W)
        self.checkBoxes.append((self.transB,self.trans))

        row += 1
        self.collectB = tk.Checkbutton(self.w,text='Allow server to store prospecting event for statistical purpose (anonymous)',variable=self.collect,background=backgroundColor,foreground=textColor,command=self.onCheck)
        self.collectB.grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.W)
        self.checkBoxes.append((self.collectB,self.collect))

        row += 1
        self.onlineDB = tk.Checkbutton(self.w,text='Start EliteProspecting online',variable=self.onlineD,background=backgroundColor,foreground=textColor,command=self.onCheck)
        self.onlineDB.grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.W)
        self.checkBoxes.append((self.onlineDB,self.onlineD))

        row += 1
        self.settings = tk.Button(self.w, text="Save settings", command=self.saveSettings,background=backgroundColor,foreground=textColor)
        self.settings.grid(row=row, padx=PADX, pady=PADY, sticky=tk.W)

        row += 1
        self.onlineB = tk.Button(self.w, text="Go online", command=self.connect,background=backgroundColor,foreground=textColor)
        self.onlineLabel = tk.Label(self.w,text="Offline",background=backgroundColor)
        self.onlineB.grid(row=row, padx=PADX, pady=PADY, sticky=tk.W)
        self.onlineLabel.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)
        self.onlineLabel.config(foreground="Red")

        self.loadConf()
        self.loadSetup()
        self.setupUi()
        self.onCheck()

        self.processThread = threading.Thread(target=self.processEvents)
        self.processThread.start()

        self.networkThread = threading.Thread(target=self.receiveMsg)
        self.networkThread.start()

        #go online at startup  ?
        if self.config.config['ui']['online'] == "1":
            self.connect()

    def onCheck(self,event=None):
        for (checkBox,value) in self.checkBoxes:
            if value.get() == 1:
                checkBox["foreground"] = self.config.config['ui_colors']['cbValid']
            else:
                checkBox["foreground"] = self.config.config['ui_colors']['textColor']

    def setupUi(self):
        try:
            self.wr.destroy()
        except AttributeError as e:
            print("window was not created yet")

        if self.config.config['ui']['show_overlay'] != "1":
            return;

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

        if self.config.config['mining']['track_cargo'] == "1":
            self.cargoStatus = tk.Label(self.wr, text="", foreground="yellow")
            self.cargoStatus.config(font=("Courier", int(self.font.get())),background='black')
            self.cargoStatus.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        for i in range(self.totalMsgDisplay):
            self.status[i] = tk.Label(self.wr, text="", foreground="yellow")
            self.status[i].config(font=("Courier", int(self.font.get())),background='black')
            self.status[i].pack(side="top", fill="both", expand=True, padx=10, pady=10)
            if i == 0:
                self.status[i]['text'] = "Waiting for prospector..."
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

    def saveSettings(self,event=None):
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
        self.config.changeConf("server","collect",self.collect.get())
        self.config.changeConf("ui","text_color",self.myColor.get())
        self.config.changeConf("ui","text_other_color",self.otherColor.get())
        self.config.changeConf("ui","font_size",self.font.get())
        self.config.changeConf("ui","sound",self.sound.get())
        self.config.changeConf("ui","total_message",self.line.get())
        self.config.changeConf("ui","transparency",self.trans.get())
        self.config.changeConf("ui","online",self.onlineD.get())
        self.config.changeConf("ui","show_overlay",self.overlay.get())
        self.config.changeConf("mining","ltd_t",self.ltdThreshold.get())
        self.config.changeConf("mining","painite_t",self.painiteThreshold.get())
        self.config.changeConf("mining","track_ltd",self.tLtd.get())
        self.config.changeConf("mining","track_painite",self.tPainite.get())
        self.config.changeConf("mining","track_cargo",self.cargo.get())

        self.config.configSave()
        self.loadSetup()
        self.setupUi()

    def updateWin(self,val):
        self.posX = self.winX.get()
        self.posY = self.winY.get()
        self.wr.wm_geometry('+' + str(self.posX) + '+' + str(self.posY))

    def connect(self):
        if not self.connected:
            self.comm = comm(self.config)
            self.connected = True
            self.onlineB['text'] = "Go offline"
            self.onlineLabel['text'] = "Online"
            self.onlineLabel.config(foreground="Green")
        else:
            self.connected = False
            time.sleep(0.2)
            self.comm.stop()
            self.onlineB['text'] = "Go online"
            self.onlineLabel['text'] = "Offline"
            self.onlineLabel.config(foreground="Red")

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
        if self.config.config['mining']['track_cargo'] == "1":
            self.cargoStatus['text'] = "Cargo : " + self.cargoCount

        for i in range(len(self.messages)):
            if self.colors[i] == "mine":
                color = self.config.config['ui']['text_color']
            else:
                color = self.config.config['ui']['text_other_color']
            self.status[i].config(foreground=color)
            self.status[i]['text'] = self.messages[i]

    def displayMsg(self, msg, mine=True):
        if self.config.config['ui']['show_overlay'] != "1":
            return;
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
            self.stats(entry)
            if entry['event'] == "ProspectedAsteroid":
                #we have a winner
                self.processMat(entry)

            elif entry['event'] == "Cargo":
                self.updateCargo(entry)

    #send statistc
    def stats(self,entry):
        if entry['event'] in self.entryStatList:
            if self.connected and self.config.config['server']['collect'] == "1":
                self.comm.sendStats(entry)

    def processMat(self,entry):
        empty = True
        belowT = False

        #hash material to easly find duplicate between wings mate
        matHash = hashlib.md5(json.dumps(entry["Materials"]).encode()).hexdigest()

        if matHash in self.hashlist:
            self.displayMsg("Asteroid already prospected")
            return
        else:
            self.hashlist.append(matHash)
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

    def updateCargo(self,event):
        self.cargoCount = str(event['Count'])
        self.refreshDisplay()

    def playsound(self):
        if self.config.config['ui']['sound'] == "1":
            self.soundplayer.play()

    def closing(self):
        self.run = False
        self.journal.stop = True
        if self.connected:
            self.connect()
        self.w.destroy()
        time.sleep(1)
        print("bye")

def main():
    myconf = config()
    root = tk.Tk()
    app = application(root,myconf)
    root.mainloop()


if __name__ == "__main__":
    # execute only if run as a script
    main()
