"""
格式：
\033[0m                         -> 默认字体显示
\033[显示方式;前景色;背景色m     -> 格式

三个参数顺序不敏感，因为值各不相同

显示方式列表：
    0 - 默认值
    1 - 高亮
    4 - 下划线
    5 - 闪烁
    7 - 反显
    8 - 不可见

前景色：
    30 - 黑色
    31 - 红色
    32 - 绿色
    33 - 黄色
    34 - 蓝色
    35 - 梅色
    36 - 青色
    37 - 白色

背景色:
    40 - 黑色
    前景色+10即可
"""
from copy import copy as _copy

METHOD_DEFAULT = -1

METHOD_BOLD      = 1
METHOD_UNDERLINE = 4
METHOD_FLASH     = 5
METHOD_REVERSE   = 7
METHOD_HIDE      = 8

FORE_BLACK  = 30
FORE_RED    = 31
FORE_GREEN  = 32
FORE_YELLOW = 33
FORE_BLUE   = 34
FORE_PLUM   = 35
FORE_CYAN   = 36
FORE_WHITE  = 37

FORE_DEFAULT = -1

BACK_BLACK  = 40
BACK_RED    = 41
BACK_GREEN  = 42
BACK_YELLOW = 43
BACK_BLUE   = 44
BACK_PLUM   = 45
BACK_CYAN   = 46
BACK_WHITE  = 47

BACK_DEFAULT = -1

def _ColorDecoratorAll(content, method, foreColor, backColor):
    rtn = '\033['
    if method  != METHOD_DEFAULT: rtn += str(method)
    if foreColor != FORE_DEFAULT: rtn += ';' + str(foreColor)
    if backColor != BACK_DEFAULT: rtn += ';' + str(backColor)
    rtn += 'm' + content + '\033[0m'
    return rtn

class _StrDecorator:
    method    = METHOD_DEFAULT
    foreColor = FORE_DEFAULT
    backColor = BACK_DEFAULT
    
    def __init__(self, method = METHOD_DEFAULT, foreColor = FORE_DEFAULT, backColor = BACK_DEFAULT):
        self.method    = method
        self.foreColor = foreColor
        self.backColor = backColor

    def __add__(self, ano):
        rtn = _copy(self)
        if ano.method  != METHOD_DEFAULT: rtn.method = ano.method
        if ano.foreColor != FORE_DEFAULT: rtn.foreColor = ano.foreColor
        if ano.backColor != BACK_DEFAULT: rtn.backColor = ano.backColor
        return rtn

    def __call__(self, str):
        return _ColorDecoratorAll(str, self.method, self.foreColor, self.backColor)

#Fore color
Black  = _StrDecorator(foreColor=FORE_BLACK)
Red    = _StrDecorator(foreColor=FORE_RED)
Green  = _StrDecorator(foreColor=FORE_GREEN)
Yellow = _StrDecorator(foreColor=FORE_YELLOW)
Blue   = _StrDecorator(foreColor=FORE_BLUE)
Plum   = _StrDecorator(foreColor=FORE_PLUM)
Cyan   = _StrDecorator(foreColor=FORE_CYAN)
White  = _StrDecorator(foreColor=FORE_WHITE)

# Method
Bold      = _StrDecorator(method=METHOD_BOLD)
Underline = _StrDecorator(method=METHOD_UNDERLINE)
Flash     = _StrDecorator(method=METHOD_FLASH)
Reverse   = _StrDecorator(method=METHOD_REVERSE)
Hide      = _StrDecorator(method=METHOD_HIDE)

# Back Color
BackBlack  = _StrDecorator(backColor=BACK_BLACK)
BackRed    = _StrDecorator(backColor=BACK_RED)
BackGreen  = _StrDecorator(backColor=BACK_GREEN)
BackYellow = _StrDecorator(backColor=BACK_YELLOW)
BackBlue   = _StrDecorator(backColor=BACK_BLUE)
BackPlum   = _StrDecorator(backColor=BACK_PLUM)
BackCyan   = _StrDecorator(backColor=BACK_CYAN)
BackWhite  = _StrDecorator(backColor=BACK_WHITE)

# Some short cuts
FontInfo     = _StrDecorator() # All default
FontStrength = _copy(Bold)
FontWarining = Yellow + Bold
FontError    = Red + Bold
