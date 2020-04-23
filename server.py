#!/usr/bin/python -u
import zmq
import signal
import json
import threading

def main():

    context = zmq.Context()
    statfile = open("event_stats.log","a+")
    # Socket to send messages on
    sender = context.socket(zmq.PUB)
    sender.bind("tcp://*:44989")
    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://*:44988")

    while True:
        print('listening ...')
        try:
            msg = receiver.recv_json()
            if "stats" in msg.keys():
                writeStats(msg,statfile)
                continue #do not broadcast stats
            print("msg received ... ")
            sender.send_json(msg)
            print(json.dumps(msg))
        except KeyboardInterrupt:
            print("W: interrupt received, stopping…")
            sender.close()
            receiver.close()
            context.term()
            statfile.close()
            quit()

def writeStats(data,filehandler):
    print("receive stat event")
    try:
        towrite = {
            "id" : data['id'],
            "data" : data['data']
        }
    except KeyError:
        print("received crap")
        return

    filehandler.write(json.dumps(towrite)+"\n")

if __name__ == "__main__":
    # execute only if run as a script
    main()
