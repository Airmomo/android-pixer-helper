"""
    触控组件
    作用：模拟用户点击屏幕的操作，支持多点触控、滑动、长按等操作
"""
import time
from helper.util import adbUtil


def _setTouchFinger(adb_path, device_name, finger_id, finger_track_id):
    """
        设置触控的手指标识
        :param adb_path: adb文件路径
        :param device_name: 设备标识名
        :param finger_id: 触控的手指ID（支持0～9）
        :param finger_track_id: 手指的跟踪ID
        :return: None
    """
    adbUtil.sendEvent(adb_path, device_name, adbUtil.TOUCH_EVENT, adbUtil.EV_ABS, adbUtil.ABS_MT_SLOT, finger_id)
    adbUtil.sendEvent(adb_path, device_name, adbUtil.TOUCH_EVENT, adbUtil.EV_ABS, adbUtil.ABS_MT_TRACKING_ID, finger_track_id)


def _setTouchPosition(adb_path, device_name, x, y, source_width, source_height):
    """
        设置触控的位置
        :param adb_path: adb文件路径
        :param device_name: 设备标识名
        :param x: 点击位置的x坐标
        :param y: 点击位置的y坐标
        :param source_width: 原设备的屏幕宽度
        :param source_height: 原设备的屏幕高度
        :return: None
    """
    adb_x, adb_y = adbUtil.loc2CompatibleADBLoc(adb_path, device_name, source_width, source_height, x, y)
    adbUtil.sendEvent(adb_path, device_name, adbUtil.TOUCH_EVENT, adbUtil.EV_ABS, adbUtil.ABS_MT_POSITION_X, adb_x)
    adbUtil.sendEvent(adb_path, device_name, adbUtil.TOUCH_EVENT, adbUtil.EV_ABS, adbUtil.ABS_MT_POSITION_Y, adb_y)


def _setTouchPressure(adb_path, device_name, pressure: int):
    """
        设置触控的按压力度
        :param adb_path: adb文件路径
        :param device_name: 设备标识名
        :param pressure: 压力值（0～1024）
        :return: None
    """
    adbUtil.sendEvent(adb_path, device_name, adbUtil.TOUCH_EVENT, adbUtil.EV_ABS, adbUtil.ABS_MT_PRESSURE, pressure)


def _commitTouchEvent(adb_path, device_name):
    """
        同步事件，相当于提交设置好的触控事件给模拟器执行
        :param adb_path: adb文件路径
        :param device_name: 设备标识名
        :return: None
    """
    adbUtil.sendSynEvent(adb_path, device_name, adbUtil.TOUCH_EVENT)


class Toucher:

    def __init__(self, adb_path, device_name, source_width, source_height):
        """ 多点触控对象 """
        self.adb_path = adb_path
        self.device_name = device_name
        self.source_width = source_width
        self.source_height = source_height

    def touchDown(self, x, y, finger_id):
        """ 按下 """
        _setTouchFinger(self.adb_path, self.device_name, finger_id, finger_track_id=finger_id)
        _setTouchPosition(self.adb_path, self.device_name, x, y, self.source_width, self.source_height)
        _setTouchPressure(self.adb_path, self.device_name, pressure=int('00000400', 16))
        _commitTouchEvent(self.adb_path, self.device_name)

    def touchMove(self, x, y, finger_id):
        """ 移动 """
        _setTouchFinger(self.adb_path, self.device_name, finger_id, finger_track_id=finger_id)
        _setTouchPosition(self.adb_path, self.device_name, x, y, self.source_width, self.source_height)
        _commitTouchEvent(self.adb_path, self.device_name)

    def touchUp(self, finger_id):
        """ 松开 """
        _setTouchFinger(self.adb_path, self.device_name, finger_id, finger_track_id=int('ffffffff', 16))
        _setTouchPressure(self.adb_path, self.device_name, pressure=0)
        _commitTouchEvent(self.adb_path, self.device_name)

    def longTouch(self, x, y, time_cost, finger_id=adbUtil.FINGER_COMMON):
        """ 长按 """
        self.touchDown(x, y, finger_id)
        time.sleep(time_cost / 1000)
        self.touchUp(finger_id)
        return True

    def longTouchAndSwipe(self, x_start, y_start, x_end, y_end, time_cost, finger_id=adbUtil.FINGER_COMMON):
        """ 长按后滑动 """
        self.touchDown(x_start, y_start, finger_id)
        time.sleep(time_cost / 1000)
        self.touchMove(x_end, y_end, finger_id)
        # 增加延迟，防止释放失败
        time.sleep(0.1)
        self.touchUp(finger_id)
        return True

    def tap(self, x, y, finger_id=adbUtil.FINGER_COMMON):
        """ 点击 """
        self.touchDown(x, y, finger_id)
        # 增加延迟，防止释放失败
        time.sleep(0.1)
        self.touchUp(finger_id)
        return True

    def tapSingle(self, x, y):
        """ 点击操作，不支持多指触控，且会导致多指触控立即松开 """
        adbUtil.tap(self.adb_path, self.device_name, x, y)
        return True

    def longTouchSingle(self, x, y, time_cost):
        """ 长按操作，不支持多指触控，且会导致多指触控立即松开 """
        adbUtil.longTouch(self.adb_path, self.device_name, x, y, time_cost)
        return True

    def swipeSingle(self, x_start, y_start, x_end, y_end, time_cost):
        """ 滑动操作，不支持多指触控，且会导致多指触控立即松开 """
        adbUtil.swipe(self.adb_path, self.device_name, x_start, y_start, x_end, y_end, time_cost)
        return True
