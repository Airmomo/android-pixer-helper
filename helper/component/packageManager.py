"""
    应用管理组件
    作用：安装应用、卸载应用、清理应用缓存
"""
from helper.util import adbUtil


class PackageManager:

    def __init__(self, adb_path, device_name):
        self.adb_path = adb_path
        self.device_name = device_name

    def installApp(self, package_name):
        """ 安装指定应用 """
        adbUtil.installApp(self.adb_path, self.device_name, package_name)

    def uninstallApp(self, package_name, is_keep=False):
        """
            卸载指定应用\n
            :param package_name: 应用包名
            :param is_keep: 是否移除软件包后保留数据和缓存目录
        """
        adbUtil.uninstallApp(self.adb_path, self.device_name, package_name, is_keep)

