"""
    名称：日志工具\n
    作用：初始化全局日志对象，打印日志
"""

from datetime import datetime

# 日志级别
LEVEL_DEBUG = 5
LEVEL_INFO = 4
LEVEL_WARNING = 3
LEVEL_ERROR = 2
LEVEL_CRITICAL = 1

# 当前日志级别
LOGGER_LEVEL = LEVEL_DEBUG


def setLevel(logger_level: str) -> None:
    """
        设置日志级别\n
        :param logger_level: 日志等级
        :return: None
    """
    global LOGGER_LEVEL
    if logger_level == 'debug':
        LOGGER_LEVEL = LEVEL_DEBUG
    elif logger_level == 'info':
        LOGGER_LEVEL = LEVEL_INFO
    elif logger_level == 'warning':
        LOGGER_LEVEL = LEVEL_WARNING
    elif logger_level == 'error':
        LOGGER_LEVEL = LEVEL_ERROR
    elif logger_level == 'critical':
        LOGGER_LEVEL = LEVEL_CRITICAL
    else:
        LOGGER_LEVEL = LEVEL_DEBUG


def _printOnly(level, *value):
    start = datetime.now()
    start_time = start.strftime('%Y-%m-%d %H:%M:%S')
    header = "[*SYSTEM-MAIN*]" + "--" \
             + "[" + start_time + "]" + "--" \
             + "[" + level + "]" + " : "
    print(header, end="")
    for v in value:
        print(str(v), end="")
    print("")


def debug(*value):
    if LOGGER_LEVEL >= LEVEL_DEBUG:
        _printOnly("DEBUG", *value)


def info(*value):
    if LOGGER_LEVEL >= LEVEL_INFO:
        _printOnly("INFO", *value)


def warning(*value):
    if LOGGER_LEVEL >= LEVEL_WARNING:
        _printOnly("WARNING", *value)


def error(*value):
    if LOGGER_LEVEL >= LEVEL_ERROR:
        _printOnly("ERROR", *value)


def critical(*value):
    if LOGGER_LEVEL >= LEVEL_CRITICAL:
        _printOnly("CRITICAL", *value)


if __name__ == '__main__':
    """ 
        用于临时测试模块方法的主函数，方法内容可忽略
        当 Run 当前模块 时，当前模块的 __name__ = __main__
        当 Run 其他模块 时，当前模块的 __name__ = __file_name__ (py文件名)
    """
    pass
