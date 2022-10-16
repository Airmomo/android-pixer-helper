"""
    安卓设备对象：
    包括必要的属性，以及通过属性实例化的功能组件和插件
"""
from helper.component.activityManager import ActivityManager
from helper.component.finder import Finder
from helper.component.logger import Logger
from helper.component.phone import Phone
from helper.component.toucher import Toucher
from helper.component.ocrer import Ocrer
from helper.component.switcher import Switcher
from helper.component.timer import Timer
from helper.component.screenshoter import Screenshoter


class AndroidDevice:

    def __init__(self, adb_path, device_name, source_width, source_height, logger_level):
        """
            :param adb_path: adb文件路径
            :param device_name: 设备名称（通过adb获取获得）
            :param source_width: （原宽度）脚本开发时设备的宽度
            :param source_height: （原高度）脚本开发时设备的高度
            :param logger_level: 日志级别
        """
        # 基本属性
        self.adb_path = adb_path
        self.device_name = device_name.replace('-', '_').replace(':', '_').replace('.', '_')
        self.source_width = source_width
        self.source_height = source_height
        # 系统组件
        self.activity_manager = ActivityManager(adb_path, device_name)
        self.logger = Logger(adb_path, device_name, logger_level)
        self.phone = Phone(adb_path, device_name)
        # 输入/输出组件
        self.screenshoter = Screenshoter(adb_path, device_name)
        self.toucher = Toucher(adb_path, device_name, source_width, source_height)
        # 识别组件
        self.finder = Finder(adb_path, device_name, source_width, source_height, self.screenshoter)
        self.ocrer = Ocrer(adb_path, device_name, source_width, source_height, self.screenshoter)
        # 记录组件
        self.switcher = Switcher(adb_path, device_name)
        self.timer = Timer(adb_path, device_name)
        # 插件
        # 是设备的扩展类，主要用于组合运用设备的组件，即使删除也对设备没有影响
        # 预留插槽，在应用初始化的时候，按需插入来初始化插件对象
        self.tabler_ex = None
        self.finder_ex = None
        self.ocrer_ex = None
