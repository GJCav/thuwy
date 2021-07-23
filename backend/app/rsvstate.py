
STATE_WAITING     = 0b000000
STATE_EXAM_END    = 0b000010
STATE_EXAM_PASS   = 0b000110
STATE_EXAM_REJECT = 0b000010
STATE_EXAM_RST    = 0b000100 # this is bitwise mask
STATE_CANCEL      = 0b001000
STATE_COMPLETE    = 0b010000
STATE_VIOLATION   = 0b100000

def isWaiting(state: int) -> bool:
    return (state & STATE_EXAM_END) == 0

def isExamEnded(state: int) -> bool:
    return not isWaiting(state)

def isExamPassed(state: int) -> bool:
    return isExamEnded() and (state & STATE_EXAM_RST)

def isExamRejected(state: int) -> bool:
    return isExamEnded() and not (state & STATE_EXAM_RST)

def isCanceled(state: int) -> bool:
    return bool(state & STATE_CANCEL)

def isCompleted(state: int) -> bool:
    return bool(state & STATE_COMPLETE)

def isViolation(state: int) -> bool:
    return bool(state & STATE_VIOLATION)


def cancel(state: int) -> bool:
    """
    cancel this rsv and return canceled state.
    """
    return state | STATE_CANCEL | STATE_COMPLETE