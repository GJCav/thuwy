"""
这个文件里面所有的timestamp都是最小单位为毫秒的整型时间戳
"""

import time
import datetime

def _todayStart():
    today = datetime.datetime.now()
    tdStr = today.strftime('%Y-%m-%d')
    today = datetime.datetime.strptime(tdStr, '%Y-%m-%d')
    return today

def now() -> int:
    return (time.time() * 1000)

def today() -> int:
    return int(_todayStart().timestamp() * 1000)

def parseDate(s) -> int:
    return int(datetime.datetime.strptime(s, '%Y-%m-%d').timestamp() * 1000)

def todayStr() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d')

def clock(stamp) -> str:
    return time.strftime('%H:%M', time.localtime(stamp/1000))

def daysAfter(d, stamp = None) -> int:
    if stamp == None:
        today = _todayStart()
    else:
        today = datetime.datetime.fromtimestamp(stamp / 1000)
    after = today + datetime.timedelta(days=d)
    return int(after.timestamp()*1000)

def aWeekAfter() -> int:
    return daysAfter(7)

def hoursAfter(stamp, hours) -> int:
    t = datetime.datetime.fromtimestamp(stamp / 1000)
    t += datetime.timedelta(hours=hours)
    return int(t.timestamp() * 1000)

def clockAfter(stamp, hours, mins) -> int:
    t = datetime.datetime.fromtimestamp(stamp / 1000)
    t += datetime.timedelta(hours=hours, minutes=mins)
    return int(t.timestamp() * 1000)

def dateToTimestamp(dateStr) -> int:
    return int(time.mktime(time.strptime(dateStr, '%Y-%m-%d'))*1000)

def getDate(stamp) -> str:
    return time.strftime('%Y-%m-%d', time.localtime(stamp/1000))

def getHour(stamp):
    return time.localtime(stamp / 1000).tm_hour

def getMins(stamp):
    return time.localtime(stamp / 1000).tm_min

# 1 - 7
def getWDay(stamp):
    return time.localtime(stamp / 1000).tm_wday + 1
