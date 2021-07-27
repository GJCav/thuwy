import threading
import time
import sys
sys.path.append('..')
from app.snowflake import Snowflake, getFlow, getTime, getMachineId

if __name__ == '__main__':
    # test code here
    pool = Snowflake()
    cnt = 100
    a = []
    flowBitoverflow = 0
    for i in range(cnt):
        a.append([])
    
    stlock = threading.Lock()
    stCdn = threading.Condition(stlock)

    def needId(idx):
        with stlock:
            stCdn.wait()

        # print(f'thread {idx}')
        for i in range(100):
            id = pool.next()
            # while id == -1:
            #     global flowBitoverflow
            #     flowBitoverflow += 1
            #     time.sleep(0.002)
            #     id = pool.next()
            a[idx].append((idx, id))
    
    thds = []
    for i in range(cnt):
        thds.append(threading.Thread(target=needId, args=(i, )))

    for i in range(cnt):
        thds[i].start()

    time.sleep(1)
    print('run!')
    with stlock:
        stCdn.notifyAll()
    
    for i in range(cnt):
        thds[i].join()

    allId = []
    for i in range(cnt):
        allId.extend(a[i])

    check = {}
    thdMap = {}
    for tid, id in allId:
        check[id] = check.get(id, 0) + 1
        thdMap[id] = thdMap.get(id, [])
        thdMap[id].append(tid)
    
    for key in check.keys():
        if key == -1:
            print(f'F: {key}')
            for e in thdMap[key]:
                print(f'   {e}')
        if check[key] != 1 and key != -1:
            print(f"E: {key} {check[key]}, flow: {getFlow(key)}, time {getTime(key)}, mach {getMachineId(key)}")
            for e in thdMap[key]:
                print(f'   {e}')

    print(f"flowbit overflow: {flowBitoverflow}")
    print('done.')
    