import zmq
import random
import string

class comm():
    def __init__(self,config):

        self.ip = config.config['server']['ip']
        self.port = int(config.config['server']['port'])

        self.context = zmq.Context()
        self.msgSender = self.context.socket(zmq.PUSH)
        self.msgReceiver = self.context.socket(zmq.SUB)
        self.name = self.randomName()

        print("connecting to ", self.ip)
        self.msgSender.connect("tcp://{}:{}".format(self.ip,self.port))
        self.msgReceiver.connect("tcp://{}:{}".format(self.ip,self.port+1))
        self.msgReceiver.setsockopt_string(zmq.SUBSCRIBE, "")

    def sendMsg(self,msg):
        #assuming json msg
        self.msgSender.send_json(msg)

    def sendStats(self,event):
        data = {
            "stats" : 1,
            "id" : self.name,
            "data" : event
        }
        self.msgSender.send_json(data)

    def rcvMsg(self):
        return self.msgReceiver.recv_json()

    def randomName(self,length=20):
        #use for serverstats and anonymity :)
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def stop(self):
        self.msgReceiver.close()
        self.msgSender.close()
        self.context.term()
