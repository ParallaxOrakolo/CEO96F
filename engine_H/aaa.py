from random import choice, randint
from threading import Thread
import threading
import timeit
from time import sleep

def verificaCLP():
    a = choice(["ok", 10, 4,7, 20])
    print("clp:", a)
    return a
class CLP(threading.Thread):
    def __init__(self, serial, interval):
        super(CLP, self).__init__()
        self.serial = serial
        self.Status_Atual = "ok"
        self.errorList = ["ok"]
        self.readInterval = interval
        self._stop_event = threading.Event()
        self._read_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def removeDuplicate(self):
        return list(dict.fromkeys(self.errorList))
    
    def getStatus(self):
        self._read_event.set()
        if self.errorList:
            self.Status_Atual = self.errorList[0]
            del self.errorList[0]
        else:
            self.Status_Atual = "ok"

        #print("Antes:", self.errorList)
        #print("Depois:", self.errorList)
        self._read_event.clear()
        return self.Status_Atual

    def getList(self):
        return self.errorList

    def run(self):
        while not self.stopped():
            tt = timeit.default_timer()
            while timeit.default_timer() - tt <= self.readInterval:
                pass
            if not self._read_event.is_set():
                self.errorList.append(verificaCLP())
                self.errorList = self.removeDuplicate()
                #print(">>",self.errorList)

clp = CLP("nano", 0.1)
clp.start()
#print(clp.getList())
for _ in range(10):
    tt = timeit.default_timer()
    # while timeit.default_timer() - tt <= 0.35:
    #     pass
    #print("<<<",clp.getList())
    # z = clp.getStatus()*tt
    print("deletou:", clp.getStatus())
    #print("<",clp.getList())

clp.stop()
clp.stop()
exit()

