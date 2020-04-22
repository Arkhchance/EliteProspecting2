#!/usr/bin/python
import zmq
import signal
import json

context = zmq.Context()

# Socket to send messages on
sender = context.socket(zmq.PUB)
sender.bind("tcp://*:44989")
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:44988")

while True:
    print('listening ...')
    try:
        msg = receiver.recv_json()
        print("msg received ... ")
        sender.send_json(msg)
        print(json.dumps(msg))
    except KeyboardInterrupt:
        print("W: interrupt received, stopping…")
        sender.close()
        receiver.close()
        context.term()
        quit()
