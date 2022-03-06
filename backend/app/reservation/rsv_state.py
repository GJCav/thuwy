STATE_WAIT = 0b000001
STATE_START = 0b000010
STATE_COMPLETE = 0b000100

STATE_CANCEL = 0b001000
STATE_REJECT = 0b010000
STATE_VIOLATE = 0b100000

COMPLETE_BY_CANCEL = STATE_COMPLETE | STATE_CANCEL
COMPLETE_BY_REJECT = STATE_COMPLETE | STATE_REJECT
COMPLETE_BY_VIOLATE = STATE_COMPLETE | STATE_VIOLATE


def isWait(s):
    return bool(s & STATE_WAIT)


def isStart(s):
    return bool(s & STATE_START)


def isComplete(s):
    return bool(s & STATE_COMPLETE)


def isCancel(s):
    return bool(s & STATE_CANCEL)


def isReject(s):
    return bool(s & STATE_REJECT)


def isViolate(s):
    return bool(s & STATE_VIOLATE)
