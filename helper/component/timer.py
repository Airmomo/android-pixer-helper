class Timer:

    def __init__(self, adb_path, device_name):
        self.adb_path = adb_path
        self.device_name = device_name
        self.time = __import__("time")
        self.timer = {}
        self.timer_s = {}

    def getRealName(self, timer_name):
        """
            获取前缀为当前设备名的时钟名称\n
            :param timer_name: 待加缀的名称
            :return: 前缀为当前设备名的时钟名称
        """
        timer_name = "&".join([self.device_name, timer_name])
        return timer_name

    def sleep(self, time_ms):
        """
            利用校验时间实现毫秒级延迟，避免由于多线程调用底层延迟而导致多个线程同时延迟
            :param time_ms: 毫秒
            :return: True
        """
        time_s = time_ms / 1000
        cur_time = int(self.time.time())
        target_time = cur_time + time_s
        while cur_time < target_time:
            cur_time = int(self.time.time())
        return True

    def init(self, timer_name, time_s):
        """
            初始化时钟周期
            :param timer_name: 时钟名称
            :param time_s: 周期时间，单位是秒
            :return: True
        """
        timer_name = self.getRealName(timer_name)
        init_time = int(self.time.time())
        target_time = init_time + time_s
        self.timer[timer_name] = target_time
        self.timer_s[timer_name] = time_s
        return True

    def check(self, timer_name):
        """
            判断指定时钟周期是否到达
            :param timer_name: 时钟名称
            :return: 到达返回True，并按周期继续计算下一个时刻，未到达返回False
        """
        timer_name = self.getRealName(timer_name)
        if self.timer[timer_name]:
            cur_time = int(self.time.time())
            target_time = self.timer[timer_name]
            if cur_time >= target_time:
                next_target_time = cur_time + self.timer_s[timer_name]
                self.timer[timer_name] = next_target_time
                return True
        return False
