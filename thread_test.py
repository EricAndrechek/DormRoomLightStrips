# Python program using
# traces to kill threads

import sys
import trace
import threading
import time
import os
class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run    
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

    def func():
        while True:
            print('thread running')

def func():
    command = "sudo python3 switches/color_rotate.py 100 0 0 0"
    os.system(command)

t1 = thread_with_trace(target = func)
t1.start()
time.sleep(10)
t1.kill()
t1.join()
if not t1.isAlive():
    print('thread killed')
