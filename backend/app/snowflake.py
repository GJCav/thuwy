import threading
import time

def _stamp():
    return int(time.time()*1000)

_base = int(time.mktime(time.strftime('2020-1-1', '%Y-%m-%d'))*1000)

class Snowflake():
    def __init__(self, machine: int):
        self.machine = machine & 0b11111

        self._mutex = threading.Lock()
        self._lstTime = _stamp()
        self._flow = 0
    
    def next(self) -> int:
        with self._mutex:
            if self._flow == 256 and self._lstTime == _stamp():
                time.sleep(0.002)
            
            if self._lstTime != _stamp():
                self._lstTime = _stamp()
                self._flow = 0

            t = _stamp() - _base
            id = 0
            id |= (t<<13)
            id |= (self.machine << 8)
            id |= self._flow
        return id



if __name__ == '__main__':
    # test code here
    pass