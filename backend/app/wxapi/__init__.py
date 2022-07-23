"""
这个模块的所有 API 在返回 None 时，都表示有些地方出错了，且无法恢复
"""

from .wxapi import (
    updateToken,
    wx_getUnlimited
)