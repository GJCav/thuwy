import threading
import time

def _stamp():
    return int(time.time()*1000)

_base = int(time.mktime(time.strptime('2020-1-1', '%Y-%m-%d'))*1000)

class Snowflake():
    def __init__(self, machine: int = 0):
        self.machine = machine & 0b11111

        self._mutex = threading.Lock()
        self._lstTime = _stamp()
        self._flow = 0
    
    def next(self) -> int:
        with self._mutex:
            if self._flow == 256 and self._lstTime == _stamp():
                time.sleep(0.002)
            
            if self._lstTime < _stamp():
                self._lstTime = _stamp()
                self._flow = 0

            t = self._lstTime - _base
            # t = _stamp() - _base # this will cause bug
            id = 0
            id |= (t<<13)
            id |= (self.machine << 8)
            id |= self._flow

            self._flow += 1
        return id

def getFlow(id):
    return id & ((1<<8)-1)

def getMachineId(id):
    return (id>>8) & ((1<<5)-1)

def getTime(id):
    return (id>>13) / 1000 + _base


def makeId(timestamp = 0, machine = 0, flow = 0):
    """
    using unix style timestamp, not python timestamp
    """

    timestamp -= _base
    return (timestamp<<13) | (machine << 8) | flow

