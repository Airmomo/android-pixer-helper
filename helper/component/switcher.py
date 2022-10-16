"""
    全局开关组件
    作用：模拟开关，用于APP中控制某段代码或功能的开启或关闭
"""

SWITCH_ON_FLAG = True
SWITCH_OFF_FLAG = False
SWITCH_DEFAULT_FLAG = SWITCH_OFF_FLAG


class Switcher:

    def __init__(self, adb_path, device_name):
        self.adb_path = adb_path
        self.device_name = device_name
        self.switch_map = {}

    def getRealName(self, switch_name):
        """
            获取前缀为当前设备名的开关名称\n
            :param switch_name: 待加缀的名称
            :return: 前缀为当前设备名的开关名称
        """
        switch_name = "&".join([self.device_name, switch_name])
        return switch_name

    def switchOn(self, switch_name):
        """
            打开开关
            :param switch_name: 开关标识名
            :return: 当前开关状态
        """
        switch_name = self.getRealName(switch_name)
        self.switch_map[switch_name] = SWITCH_ON_FLAG
        return self.switch_map[switch_name]

    def switchOff(self, switch_name):
        """
            关闭开关
            :param switch_name: 开关标识名
            :return: 当前开关状态
        """
        switch_name = self.getRealName(switch_name)
        self.switch_map[switch_name] = SWITCH_OFF_FLAG
        return self.switch_map[switch_name]

    def switchInit(self, switch_name):
        """
            初始化开关
            :param switch_name: 开关标识名
            :return: 当前开关状态
        """
        switch_name = self.getRealName(switch_name)
        self.switch_map[switch_name] = SWITCH_DEFAULT_FLAG
        return self.switch_map[switch_name]

    def getSwitchStatus(self, switch_name):
        """
            获取当前开关状态
            :param switch_name: 开关标识名
            :return: 当前开关状态
        """
        switch_name = self.getRealName(switch_name)
        if not self.switch_map[switch_name]:
            return self.switch_map[switch_name]
        self.switchInit(switch_name)
        return self.switch_map[switch_name]
