#!/usr/bin/python -u
import zmq
import signal
import json
import threading

def main():

    context = zmq.Context()
    sender = context.socket(zmq.PUB)
    sender.bind("tcp://*:44989")
    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://*:44988")

    while True:
        print('listening ...')
        try:
            msg = receiver.recv_json()
            if "stats" in msg.keys():
                threading.Thread(target=writeStats,args=(msg,)).start()
                continue #do not broadcast stats
            print("msg received ... ")
            sender.send_json(msg)
            print(json.dumps(msg))
        except KeyboardInterrupt:
            print("W: interrupt received, stopping…")
            sender.close()
            receiver.close()
            context.term()
            quit()

def writeStats(data):
    print("receive stat event")
    try:
        towrite = {
            "id" : data['id'],
            "data" : data['data']
        }
    except KeyError:
        print("received crap")
        return

    with open("event_stats.log","a+") as fh:
        fh.write(json.dumps(towrite)+"\n")

if __name__ == "__main__":
    # execute only if run as a script
    main()
