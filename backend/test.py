from threading import Thread
import requests as R
from sys import exit
import time
from pprint import pprint

thdCnt = 10 # 线程数
addCnt = 10 # 每个线程加 addCnt 次

res = R.get('http://127.0.0.1:5000/create')
if res.status_code != 200:
    print('Unable to create. ' + res.reason)

testID = res.json()["id"]

print(f'test id: {testID}')

result = {}

def task():
    global testID
    for i in range(addCnt):
        res = R.get(f'http://127.0.0.1:5000/add/{testID}')
        code = res.status_code
        result[code] = (result.get(code) or 0) + 1

thd = []
for i in range(thdCnt):
    t = Thread(target=task)
    thd.append(t)

startAt = time.time()
for t in thd:
    t.start()

for t in thd:
    t.join()
endAt = time.time()

res = R.get(f'http://127.0.0.1:5000/qry/{testID}')
num = res.json()['num']

pprint(result)
print(f'elapsed: {endAt - startAt}')
print(f'expect: {thdCnt * addCnt}, result: {num}')