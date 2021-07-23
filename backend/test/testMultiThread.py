from threading import *

# mutex = Lock()
# a = 0

# def add(tid):
#     with mutex:
#         for i in range(10):
#             print(f'{tid} {i}')
#             \

# thds = []
# cnt = 3
# for i in range(cnt):
#     thds.append(Thread(target=add, args=(i, )))

# for i in range(cnt):
#     thds[i].start()

# for i in range(cnt):
#     thds[i].join()

# print(a)

class Print:
    def __init__(self) -> None:
        self._mutex = Lock()
        
    def myprint(self, tid):
        with self._mutex:
            for i in range(10):
                print(f'{tid} {i}')

p = Print()

def invoke(tid):
    p.myprint(tid)

thds = []
cnt = 3
for i in range(cnt):
    thds.append(Thread(target=invoke, args=(i, )))

for i in range(cnt):
    thds[i].start()

for i in range(cnt):
    thds[i].join()