import subprocess
from multiprocessing.connection import Listener


def listen():
    listener = Listener(('localhost', 6000), authkey=b'secret')
    conn = listener.accept()
    while True:
        msg = conn.recv()
        print("received: {}".format(msg))
        if msg == 'close':
            break

        if msg[0] == 'video':
            print(msg[0])
            print(msg[1])
            # subprocess.Popen(['vlc', msg[1], '--fullscreen'])
        if msg[0] == 'website':
            print(msg[0])
            print(msg[1])
            subprocess.Popen(['firefox', msg[1]])


listen()
