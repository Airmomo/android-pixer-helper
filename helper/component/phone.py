"""
    系统操作组件
    作用：执行输入/输出操作、系统级别操作，模拟物理按键
"""
from helper.util import adbUtil


class Phone:

    def __init__(self, adb_path, device_name):
        self.adb_path = adb_path
        self.device_name = device_name

    def hideStatusAndNavigationBar(self):
        adbUtil.hideStatusAndNavigationBar(self.adb_path, self.device_name)

    def setADBIme(self):
        adbUtil.setIme(self.adb_path, self.device_name, adbUtil.IME_ADB_KEY_BOARD)

    def inputStrText(self, str_text):
        adbUtil.inputStrText(self.adb_path, self.device_name, str_text)

    def inputStrTextBackIme(self, str_text):
        """
            在焦点处于某文本框时，可以通过 input 命令来输入文本\n
            注意：支持传入中文字符，但需要在模拟器上安装ADBKeyBoard.apk\n
            本方法与inputStrText的区别是会自动恢复原先的输入法
        """
        # 备份当前输入法设置
        bak_kb = adbUtil.getCurrentIme(self.adb_path, self.device_name)
        # 设置输入法为ADBKeyBoard
        self.setADBIme()
        self.inputStrText(str_text)
        # 恢复原来的输入法
        if bak_kb != adbUtil.IME_ADB_KEY_BOARD:
            adbUtil.setIme(self.adb_path, self.device_name, bak_kb)

    def tapVolumeLower(self, time_count):
        """ 点击降低音量键，time_count可设置点击次数，即降低多少次音量"""
        for i in range(0, time_count):
            adbUtil.sendKeyEvent(self.adb_path, self.device_name, adbUtil.KEYCODE_VOLUME_DOWN)

    def tapVolumeUpper(self, time_count):
        """ 点击提升音量键，time_count可设置点击次数，即提升多少次音量"""
        for i in range(0, time_count):
            adbUtil.sendKeyEvent(self.adb_path, self.device_name, adbUtil.KEYCODE_VOLUME_UP)

    def tapVolumeSilent(self):
        """ 点击静音键，再次点击取消静音 """
        adbUtil.sendKeyEvent(self.adb_path, self.device_name, adbUtil.KEYCODE_VOLUME_SILENT)

    def tapPower(self):
        """ 点击Home键，应用置于后台 """
        adbUtil.sendKeyEvent(self.adb_path, self.device_name, adbUtil.KEYCODE_POWER)

    def tapBack(self):
        """ 点击返回键 ，返回上一级"""
        adbUtil.sendKeyEvent(self.adb_path, self.device_name, adbUtil.KEYCODE_BACK)

    def tapDel(self):
        """ 点击删除/退格键 """
        adbUtil.sendKeyEvent(self.adb_path, self.device_name, adbUtil.KEYCODE_DEL)

    def reboot(self):
        """ 重启设备 """
        adbUtil.reboot(self.adb_path, self.device_name)