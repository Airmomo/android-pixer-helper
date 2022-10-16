"""
    应用生命周期管理组件
    作用：控制应用的启动和关闭
"""
from helper.util import adbUtil


class ActivityManager:

    def __init__(self, adb_path, device_name):
        self.adb_path = adb_path
        self.device_name = device_name

    def startApp(self, package_name, activity_name):
        """
            启动应用，如果应用已启动则把应用恢复到前台
            :param package_name: 应用的包名
            :param activity_name: Activity名称
            :return: None
        """
        adbUtil.startApp(self.adb_path, self.device_name, package_name, activity_name)

    def stopApp(self, package_name):
        """
            关闭应用，强制停止应用继续运行
            :param package_name: 应用的包名
            :return: None
        """
        adbUtil.stopApp(self.adb_path, self.device_name, package_name)

    def reStartApp(self, package_name, activity_name):
        """
            强行停止目标应用，重启应用到指定的Activity
            :param package_name: 应用的包名
            :param activity_name: Activity名称
            :return: None
        """
        adbUtil.reStartApp(self.adb_path, self.device_name, package_name, activity_name)

    def stopAndClearApp(self, package_name):
        """
            不仅会停止进程运行，还会清除应用的所有缓存数据
            :param package_name: 应用的包名
            :return: None
        """
        adbUtil.stopAndClearApp(self.adb_path, self.device_name, package_name)
