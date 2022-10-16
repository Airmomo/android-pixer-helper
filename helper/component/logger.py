"""
    日志记录组件
    作用：按指定级别记录和输出运行日志
"""
from datetime import datetime

# 日志级别
LEVEL_DEBUG = 5
LEVEL_INFO = 4
LEVEL_WARNING = 3
LEVEL_ERROR = 2
LEVEL_CRITICAL = 1
# 日志级别名称
LEVEL_DEBUG_NAME = "DEBUG"
LEVEL_INFO_NAME = "INFO"
LEVEL_WARNING_NAME = "WARNING"
LEVEL_ERROR_NAME = "ERROR"
LEVEL_CRITICAL_NAME = "CRITICAL"
# 日志颜色 # \033[显示方式;前景色;背景色m 要输出的内容 \033[m
LEVEL_DEBUG_COLOR = "37m "  # 白色
LEVEL_INFO_COLOR = "32m "  # 绿色
LEVEL_WARNING_COLOR = "33m "  # 黄色
LEVEL_ERROR_COLOR = "31m "  # 红色
LEVEL_CRITICAL_COLOR = "1;31m "  # 红色高亮


def _getLevelColor(level):
    level_color = "0;0;0m "
    if level == LEVEL_DEBUG_NAME:
        level_color = LEVEL_DEBUG_COLOR
    elif level == LEVEL_INFO_NAME:
        level_color = LEVEL_INFO_COLOR
    elif level == LEVEL_WARNING_NAME:
        level_color = LEVEL_WARNING_COLOR
    elif level == LEVEL_ERROR_NAME:
        level_color = LEVEL_ERROR_COLOR
    elif level == LEVEL_CRITICAL_NAME:
        level_color = LEVEL_CRITICAL_COLOR
    return level_color


def _printOnly(adb_path, device_name, level, *value):
    # \033[显示方式;前景色;背景色m 要输出的内容 \033[m
    color_pre = "\033["
    color_set = _getLevelColor(level)
    color_tail = " \033[0m"
    start = datetime.now()
    start_time = start.strftime('%Y-%m-%d %H:%M:%S')
    # "[" + adb_path + "]" + "--" \
    header = "[" + device_name + "]" + "--" \
             + "[" + start_time + "]" + "--" \
             + "[" + level + "]" + " : "
    print_str_list = [color_pre, color_set, header]
    for v in value:
        print_str_list.append(str(v))
    print_str_list.append(color_tail)
    print_str = "".join(print_str_list)
    print(print_str, end="\r\n")


class Logger:

    def __init__(self, adb_path, device_name, level):
        self.adb_path = adb_path
        self.device_name = device_name
        self.level = level

    def debug(self, *value):
        if self.level >= LEVEL_DEBUG:
            _printOnly(self.adb_path, self.device_name, LEVEL_DEBUG_NAME, *value)

    def info(self, *value):
        if self.level >= LEVEL_INFO:
            _printOnly(self.adb_path, self.device_name, LEVEL_INFO_NAME, *value)

    def warning(self, *value):
        if self.level >= LEVEL_WARNING:
            _printOnly(self.adb_path, self.device_name, LEVEL_WARNING_NAME, *value)

    def error(self, *value):
        if self.level >= LEVEL_ERROR:
            _printOnly(self.adb_path, self.device_name, LEVEL_ERROR_NAME, *value)

    def critical(self, *value):
        if self.level >= LEVEL_CRITICAL:
            _printOnly(self.adb_path, self.device_name, LEVEL_CRITICAL_NAME, *value)

