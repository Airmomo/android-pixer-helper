"""
    名称：安卓调试桥（ADB）工具\n
    获取事件日志：./adb shell --getevent \n
    官方文档：https://source.android.com/docs/core/input/getevent
"""
import warnings
import re
import subprocess
import os

# 输入法
IME_ADB_KEY_BOARD = "com.android.adbkeyboard/.AdbIME"
IME_QQPINYIN = "com.tencent.qqpinyin/.QQPYInputMethodService"

# 设备文件号
TOUCH_EVENT = "event0"
PHONE_EVENT = "event0"

# 事件类型
EV_SYN = 0
EV_KEY = int('0001', 16)
EV_REL = int('0002', 16)
EV_ABS = int('0003', 16)
EV_MSC = int('0004', 16)
EV_SW = int('0005', 16)
EV_LED = int('0011', 16)

# 事件码
SYN_REPORT = 0
"""
events:
    KEY (0001): 0001  0002  0003  0004  0005  0006  0007  0008
                0009  000a  000b  000c  000d  000e  000f  0010
                0011  0012  0013  0014  0015  0016  0017  0018
                0019  001a  001b  001c  001d  001e  001f  0020
                0021  0022  0023  0024  0025  0026  0027  0028
                0029  002a  002b  002c  002d  002e  002f  0030
                0031  0032  0033  0034  0035  0036  0037  0038
                0039  003a  003b  003c  003d  003e  003f  0040
                0041  0042  0043  0044  0045  0046  0047  0048
                0049  004a  004b  004c  004d  004e  004f  0050
                0051  0052  0053  0055  0056  0057  0058  0059
                005a  005b  005c  005d  005e  005f  0060  0061
                0062  0063  0064  0066  0067  0068  0069  006a
                006b  006c  006d  006e  006f  0071  0072  0073
                0074  0075  0077  0079  007a  007b  007c  007d
                007e  007f  0080  0081  0082  0083  0084  0085
                0086  0087  0088  0089  008a  008c  008e  0090
                0096  0098  009b  009c  009e  009f  00a1  00a3
                00a4  00a5  00a6  00ab  00ac  00ad  00b0  00b1
                00b2  00b3  00b4  00b7  00b8  00b9  00ba  00bb
                00bc  00bd  00be  00bf  00c0  00c1  00c2  00d9
                00f0  0110  0111  0112  01ba
    KEYCODE：
            0 –> “KEYCODE_UNKNOWN”
            1 –> “KEYCODE_MENU”
            2 –> “KEYCODE_SOFT_RIGHT”
            3 –> “KEYCODE_HOME” //Home键
            4 –> “KEYCODE_BACK” //返回键
            5 –> “KEYCODE_CALL” 
            6 –> “KEYCODE_ENDCALL” 
            7 –> “KEYCODE_0” //数字键0
            8 –> “KEYCODE_1” 
            9 –> “KEYCODE_2” 
            10 –> “KEYCODE_3”
            11 –> “KEYCODE_4” 
            12 –> “KEYCODE_5” 
            13 –> “KEYCODE_6” 
            14 –> “KEYCODE_7” 
            15 –> “KEYCODE_8” 
            16 –> “KEYCODE_9” 
            17 –> “KEYCODE_STAR” 
            18 –> “KEYCODE_POUND” 
            19 –> “KEYCODE_DPAD_UP” 
            20 –> “KEYCODE_DPAD_DOWN” 
            21 –> “KEYCODE_DPAD_LEFT”
            22 –> “KEYCODE_DPAD_RIGHT” 
            23 –> “KEYCODE_DPAD_CENTER” 
            24 –> “KEYCODE_VOLUME_UP” //音量键+
            25 –> “KEYCODE_VOLUME_DOWN” //音量键-
            26 –> “KEYCODE_POWER” //Power键
            27 –> “KEYCODE_CAMERA” 
            28 –> “KEYCODE_CLEAR”
            29 –> “KEYCODE_A” //字母键A
            30 –> “KEYCODE_B” 
            31 –> “KEYCODE_C” 
            32 –> “KEYCODE_D” 
            33 –> “KEYCODE_E” 
            34 –> “KEYCODE_F” 
            35 –> “KEYCODE_G”
            36 –> “KEYCODE_H”
            37 –> “KEYCODE_I”
            38 –> “KEYCODE_J” 
            39 –> “KEYCODE_K” 
            40 –> “KEYCODE_L” 
            41 –> “KEYCODE_M”
            42 –> “KEYCODE_N” 
            43 –> “KEYCODE_O” 
            44 –> “KEYCODE_P” 
            45 –> “KEYCODE_Q” 
            46 –> “KEYCODE_R”
            47 –> “KEYCODE_S”
            48 –> “KEYCODE_T” 
            49 –> “KEYCODE_U” 
            50 –> “KEYCODE_V” 
            51 –> “KEYCODE_W” 
            52 –> “KEYCODE_X”
            53 –> “KEYCODE_Y” 
            54 –> “KEYCODE_Z”
            55 –> “KEYCODE_COMMA” 
            56 –> “KEYCODE_PERIOD”
            57 –> “KEYCODE_ALT_LEFT” 
            58 –> “KEYCODE_ALT_RIGHT” 
            59 –> “KEYCODE_SHIFT_LEFT” 
            60 –> “KEYCODE_SHIFT_RIGHT”
            61 -> “KEYCODE_TAB” 
            62 –> “KEYCODE_SPACE” 
            63 –> “KEYCODE_SYM” 
            64 –> “KEYCODE_EXPLORER” 
            65 –> “KEYCODE_ENVELOPE” 
            66 –> “KEYCODE_ENTER” //回车键
            67 –> “KEYCODE_DEL” 
            68 –> “KEYCODE_GRAVE” 
            69 –> “KEYCODE_MINUS” 
            70 –> “KEYCODE_EQUALS” 
            71 –> “KEYCODE_LEFT_BRACKET” 
            72 –> “KEYCODE_RIGHT_BRACKET” 
            73 –> “KEYCODE_BACKSLASH” 
            74 –> “KEYCODE_SEMICOLON” 
            75 –> “KEYCODE_APOSTROPHE”
            76 –> “KEYCODE_SLASH” 
            77 –> “KEYCODE_AT” 
            78 –> “KEYCODE_NUM” 
            79 –> “KEYCODE_HEADSETHOOK” 
            80 –> “KEYCODE_FOCUS”
            81 –> “KEYCODE_PLUS”
            82 –> “KEYCODE_MENU”
            83 –> “KEYCODE_NOTIFICATION”
            84 –> “KEYCODE_SEARCH”
"""
KEYCODE_HOME = 3
KEYCODE_BACK = 4
KEYCODE_VOLUME_UP = 24
KEYCODE_VOLUME_DOWN = 25
KEYCODE_POWER = 26
KEYCODE_DEL = 67
KEYCODE_VOLUME_SILENT = 164
"""
events:
    ABS (0003): 
        ABS_X                           : value 0, min 0, max 32767, fuzz 0, flat 0, resolution 0
        ABS_Y                           : value 0, min 0, max 32767, fuzz 0, flat 0, resolution 0
        ABS_Z                           : value 0, min 0, max 1, fuzz 0, flat 0, resolution 0
        触控的手指：ABS_MT_SLOT           : value 0, min 0, max 9, fuzz 0, flat 0, resolution 0
        触碰尺寸：ABS_MT_TOUCH_MAJOR      : value 0, min 0, max 2147483647, fuzz 0, flat 0, resolution 0
        ABS_MT_TOUCH_MINOR              : value 0, min 0, max 2147483647, fuzz 0, flat 0, resolution 0
        ABS_MT_ORIENTATION              : value 0, min 0, max 90, fuzz 0, flat 0, resolution 0
        *触碰X轴：ABS_MT_POSITION_X      : value 0, min 0, max 32767, fuzz 0, flat 0, resolution 0
        *触碰Y轴：ABS_MT_POSITION_Y      : value 0, min 0, max 32767, fuzz 0, flat 0, resolution 0
        ABS_MT_TOOL_TYPE                : value 0, min 0, max 15, fuzz 0, flat 0, resolution 0
        手指的跟踪id：ABS_MT_TRACKING_ID  : value 0, min 0, max 11, fuzz 0, flat 0, resolution 0
        触碰力度：ABS_MT_PRESSURE         : value 0, min 0, max 1024, fuzz 0, flat 0, resolution 0
"""
ABS_X = int('0000', 16)
ABS_Y = int('0001', 16)
ABS_Z = int('0002', 16)
ABS_MT_SLOT = int('002f', 16)
ABS_MT_TOUCH_MAJOR = int('0030', 16)
ABS_MT_TOUCH_MINOR = int('0031', 16)
ABS_MT_ORIENTATION = int('0034', 16)
ABS_MT_POSITION_X = int('0035', 16)
ABS_MT_POSITION_Y = int('0036', 16)
ABS_MT_TOOL_TYPE = int('0037', 16)
ABS_MT_TRACKING_ID = int('0039', 16)
ABS_MT_PRESSURE = int('003a', 16)
# 默认触控的手指
FINGER_COMMON = 0
# 触控的范围
ABS_MT_POSITION_X_MIN = 0
ABS_MT_POSITION_Y_MIN = 0
ABS_MT_POSITION_X_MAX = 32767
ABS_MT_POSITION_Y_MAX = 32767


def _getCompatibleAdbLoc(device_cur_loc, device_max_range, adb_max_range, device_min_range=0, adb_min_range=0):
    """
        根据用户传入的设备坐标数值，转换为adb点击时对应的坐标数值
        value: min: 0 , max: adb_max_range
    """
    return (adb_max_range - adb_min_range) / (device_max_range - device_min_range) * device_cur_loc


def _getCompatibleDeviceLoc(adb_cur_loc, device_max_range, adb_max_range, device_min_range=0, adb_min_range=0):
    """
        根据用户传入的Adb坐标数值，转换为设备真实点击时对应的坐标数值
        value: min: 0 , max: device_max_range
    """
    return (adb_cur_loc - adb_min_range) * device_max_range / (adb_max_range - device_min_range)


def _cmd(cmdStr: str):
    """
        执行命令行\n
        :param cmdStr: 命令字符串
        :return 终端的输出内容（包括标识符）
    """
    cmds = cmdStr.split(' ')
    proc = subprocess.Popen(
        cmds,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    # returncode > 0 代表执行cmd命令报错
    if proc.returncode > 0:
        raise Exception(proc.returncode, stderr)
    return stdout


def _getCompatibleLoc(cur_loc, device_source_range, device_target_range, adb_source_max_range, adb_target_max_range):
    """
        设备坐标转换: 根据用户传入的坐标，转换为兼容当前设备的坐标\n
        :param cur_loc: 待转换的坐标
        :param device_source_range: 坐标转换前支持的分辨率
        :param device_target_range: 坐标转换后支持的分辨率
        :param adb_source_max_range: 坐标转换前其设备Adb位置大小支持的最大范围
        :param adb_target_max_range: 坐标转换后其设备Adb位置大小支持的最大范围
        :return: (转换后的设备坐标，转换后的Adb坐标)
    """
    """
        # 例如：
            基于720p分辨率开发的脚本，点击的坐标x=250
            为了兼容1080p分辨率的设备，则需要：
            # 将在720p下的坐标数值，转换为其adb点击的坐标数值
                1、adb_loc_pre = getCompatibleAdbLoc(cur_loc=250, device_source_range=720, adb_source_max_range)
            # 将adb点击的坐标数值，转换为在1080p下点击的坐标数值
                2、device_loc_res = getCompatibleDeviceLoc(adb_loc_pre=adb_loc, device_target_range=1080, adb_target_max_range)
            # 将在1080p下的坐标数值，转换为其adb点击的坐标数值
                3、adb_loc_res = getCompatibleAdbLoc(device_loc_res=device_loc, device_target_range=1080, adb_target_max_range)
        # 实现兼容的原理：
            1、对于不同分辨率的设备，其ADB的触控范围大小一般都是固定，最小是0，最大是32767；
            2、那么就可以计算出一个固定的数值，即开发时脚本的坐标大小与该范围大小的比例
            3、利用该比例就可以计算出开发脚本时，点击的adb的坐标大小
            4、再计算出待兼容的分辨率与该范围大小的比例，利用adb的坐标大小除以该比例，就可以计算出在待兼容的分辨率下，点击的坐标大小
            5、最后将该坐标大小乘以兼容的比例，就可以得到其点击的adb的坐标大小
    """
    adb_loc_pre = _getCompatibleAdbLoc(cur_loc, device_source_range, adb_source_max_range)
    device_loc_res = _getCompatibleDeviceLoc(adb_loc_pre, device_target_range, adb_target_max_range)
    adb_loc_res = _getCompatibleAdbLoc(device_loc_res, device_target_range, adb_target_max_range)
    return device_loc_res, adb_loc_res


def _getCompatibleLocSimple(cur_loc, device_source_range, device_target_range, adb_source_max_range=32767,
                           adb_target_max_range=32767):
    """
        设备坐标转换方法（getCompatibleLoc方法的简化调用版）\n
        注意：调用该方法需要转换前后的ABS_MT_POSITION_X_MAX和ABS_MT_POSITION_Y_MAX都相等，都为32767 \n
        :param cur_loc: 待转换的坐标
        :param device_source_range: 坐标转换前支持的分辨率
        :param device_target_range: 坐标转换后支持的分辨率
        :param adb_source_max_range: 坐标转换前其设备Adb位置大小支持的最大范围
        :param adb_target_max_range: 坐标转换后其设备Adb位置大小支持的最大范围
        :return: (转换后的设备坐标，转换后的Adb坐标)
    """
    device_loc_res, adb_loc_res = _getCompatibleLoc(cur_loc, device_source_range, device_target_range,
                                                    adb_source_max_range, adb_target_max_range)
    return int(device_loc_res), int(adb_loc_res)


def loc2CompatibleLoc(adb_path, device_name, source_width, source_height, x, y):
    """ 转化x, y 坐标兼容当前设备 """
    # 当屏幕发生旋转时，坐标轴的取向和分辨率也会发生改变，所以需要获取当前的分辨率
    device_width, device_height = getCurScreenSize(adb_path, device_name)
    x = _getCompatibleLocSimple(x, source_width, device_width)[0]
    y = _getCompatibleLocSimple(y, source_height, device_height)[0]
    return x, y


def loc2CompatibleLocAll(adb_path, device_name, source_width, source_height, start_x, start_y, end_x, end_y):
    """ 转化所有坐标兼容当前设备 """
    start_x, start_y = loc2CompatibleLoc(adb_path, device_name, source_width, source_height, start_x, start_y)
    end_x, end_y = loc2CompatibleLoc(adb_path, device_name, source_width, source_height, end_x, end_y)
    return start_x, start_y, end_x, end_y


def loc2CompatibleADBLoc(adb_path, device_name, source_width, source_height, x, y):
    """ 转化x, y 坐标兼容当前设备ADB点击的坐标 """
    # 当屏幕发生旋转时，Adb坐标轴的取向和分辨率不会发生改变，所以需要获取初始化时设备的分辨率
    device_width_init, device_height_init = getInitScreenSize(adb_path, device_name)
    device_width_cur, device_height_cur = getCurScreenSize(adb_path, device_name)
    # 判断屏幕是否发生了旋转
    if device_width_cur == device_height_init and device_height_cur == device_width_init:
        # 对应的ADB点击的坐标也要一起旋转，默认一直旋转到左上角
        x_bak = x
        x = device_width_init - y
        y = x_bak
    x = _getCompatibleLocSimple(x, device_width_init, source_width)[1]
    y = _getCompatibleLocSimple(y, device_height_init, source_height)[1]
    return x, y


def loc2CompatibleADBLocAll(adb_path, device_name, source_width, source_height, start_x, start_y, end_x, end_y):
    """ 转化所有坐标兼容当前设备ADB点击的坐标 """
    start_x, start_y = loc2CompatibleADBLoc(adb_path, device_name, source_width, source_height, start_x, start_y)
    end_x, end_y = loc2CompatibleADBLoc(adb_path, device_name, source_width, source_height, end_x, end_y)
    return start_x, start_y, end_x, end_y


def sendShell(adb_path: str, device_name: str, input_str: str):
    """
        发送Adb-Shell命令，发送后立即被提交执行
    """
    shell = "%s -s %s shell %s" % (adb_path, device_name, input_str)
    return _cmd(shell)


def sendAm(adb_path: str, device_name: str, input_str: str):
    """
        发送应用交互相关命令，发送后立即被提交执行
    """
    shell_str = "am %s" % input_str
    return sendShell(adb_path, device_name, shell_str)


def sendPm(adb_path: str, device_name: str, input_str: str):
    """
        发送应用操作相关命令，发送后立即被提交执行
    """
    shell_str = "pm %s" % input_str
    return sendShell(adb_path, device_name, shell_str)


def sendIme(adb_path: str, device_name: str, input_str: str):
    """
        发送应用操作相关命令，发送后立即被提交执行
    """
    shell_str = "ime %s" % input_str
    return sendShell(adb_path, device_name, shell_str)


def sendSettings(adb_path: str, device_name: str, input_str: str):
    """
        发送应用操作相关命令，发送后立即被提交执行
    """
    shell_str = "settings %s" % input_str
    return sendShell(adb_path, device_name, shell_str)


def sendInput(adb_path: str, device_name: str, input_str: str):
    """
        发送输入操作命令，发送后立即被提交执行
    """
    shell_str = "input %s" % input_str
    return sendShell(adb_path, device_name, shell_str)


def sendEvent(adb_path: str, device_name: str, eventIndex: str, eventType: int, eventParam: int, eventValue: int):
    """
        发送操作事件，发送后不会立即执行，待发送同步指令后才会按顺序执行\n
        注意：不支持 Android >= 10.0 , API > 24 的设备
    """
    shell_str = "sendevent /dev/input/%s %d %d %d" % (eventIndex, eventType, eventParam, eventValue)
    return sendShell(adb_path, device_name, shell_str)


def sendKeyEvent(adb_path: str, device_name: str, key_event_val: int):
    """
        发送操作命令，发送后立即被提交执行
    """
    input_str = "keyevent %d" % key_event_val
    return sendInput(adb_path, device_name, input_str)


def sendSynEvent(adb_path: str, device_name: str, eventIndex: str):
    """
        发送事件同步指令\n
        只有发送该指令后，其之前发送的操作事件才会被提交并执行
    """
    return sendEvent(adb_path, device_name, eventIndex, EV_SYN, SYN_REPORT, 0)


def getScreenshotByteImage(adb_path, device_name):
    """
        获取屏幕截图并以流的方式输出，直接转换为数组
    """
    shell = "%s -s %s shell screencap -p" % (adb_path, device_name)
    # 在 Windows 中，Python 获取的图片数据会把原数据流中的 \n 转义为 \r\r\n 或 \r\n，导致图片无法被正常识别。
    # 这里将\r\r\n 或 \r\n 替换回 \n 来保持兼容性
    byte_image = _cmd(shell).replace(b'\r\n', b'\n').replace(b'\r\n', b'\n')
    return byte_image


def getScreenshotFilePath(adb_path, device_name, file_name, file_type, file_push_pkg,
                          file_pull_pkg):
    """
        获取屏幕截图并按指定格式保存到本地
    """
    file = '.'.join([file_name, file_type])
    # 指定截屏保存到手机内的文件路径:
    # %s -s %s shell screencap -p > /sdcard/screen.png
    file_push_path = '/'.join([file_push_pkg, file])
    shell_str = 'screencap -p > %s' % file_push_path
    sendShell(adb_path, device_name, shell_str)
    file_pull_path = '/'.join([file_pull_pkg, device_name])
    # 判断文件是否存在
    if not os.path.exists(file_pull_path):
        os.makedirs(file_pull_path)
    file_pull_path = '/'.join([file_pull_pkg, device_name, file])
    # 指定从手机内拉取的文件路径，以及保存到本地保存的路径
    # %s -s %s pull /sdcard/screen.png ./screen.png
    shell_str = '%s -s %s pull %s %s' % (adb_path, device_name, file_push_path, file_pull_path)
    _cmd(shell_str)
    return file_pull_path


def _getScreenSize(adb_path, device_name):
    """
        获取设备的屏幕分辨率详细
    """
    input_str = "dumpsys window displays | grep cur="
    shell_res = sendShell(adb_path, device_name, input_str)
    shell_res = str(shell_res)
    match_res = re.search(r'init=(\d+)x(\d+) (\d+)dpi cur=(\d+)x(\d+) app=(\d+)x(\d+) rng=(\d+)x(\d+)-(\d+)x(\d+)', shell_res)
    return match_res


def getInitScreenSize(adb_path, device_name):
    """
        获取设备的物理屏幕分辨率
    """
    match_res = _getScreenSize(adb_path, device_name)
    width = int(match_res.group(1))
    height = int(match_res.group(2))
    return width, height


def getCurScreenSize(adb_path, device_name):
    """
        获取设备的当前屏幕分辨率\n
        因为屏幕旋转后会改变屏幕的取向，分辨率的数值会随着取向发生变化
    """
    match_res = _getScreenSize(adb_path, device_name)
    width = int(match_res.group(4))
    height = int(match_res.group(5))
    return width, height


def getScreenDensity(adb_path, device_name):
    """
        获取设备的屏幕密度
    """
    match_res = _getScreenSize(adb_path, device_name)
    dpi = int(match_res.group(3))
    return dpi


def modifyScreenSize(adb_path, device_name, width, height):
    """
        修改设备的屏幕分辨率
        注意：需要重启设备后才能生效
    """
    warnings.warn("不推荐通过该方法来兼容设备分辨率，推荐使用算法来实现程序对不同分辨率的支持", DeprecationWarning)
    shell_str = 'wm size reset'
    if width != 0 and height != 0:
        shell_str = 'wm size %dx%d' % (width, height)
    return sendShell(adb_path, device_name, shell_str)


def modifyScreenDensity(adb_path, device_name, dpi_value):
    """
        修改设备的屏幕密度dpi
        注意：需要重启设备后才能生效
    """
    warnings.warn("不推荐通过该方法来兼容设备屏幕密度，推荐使用算法来实现程序对不同密度的支持", DeprecationWarning)
    shell_pull = 'wm density reset'
    if dpi_value != 0:
        shell_pull = 'wm density %d' % dpi_value
    return sendShell(adb_path, device_name, shell_pull)


def setIme(adb_path, device_name, key_board):
    """
        设置默认输入法
    """
    input_str = "set %s" % key_board
    return sendIme(adb_path, device_name, input_str)


def getCurrentIme(adb_path, device_name):
    """
        获取当前正在使用的输入法
    """
    input_str = "get secure default_input_method"
    res = sendSettings(adb_path, device_name, input_str)
    match_res = str(res).replace("\\n\'", "").replace("b'", "")
    return match_res


def inputText(adb_path, device_name, text):
    """
        在焦点处于某文本框时，可以通过 input 命令来输入文本\n
        注意：不支持传入中文字符，想传入中文字符请配合ADBKeyBoard使用inputStrText方法\n
    """
    input_str = "text %s" % text
    return sendInput(adb_path, device_name, input_str)


def inputStrText(adb_path, device_name, str_text):
    """
        在焦点处于某文本框时，可以通过 input 命令来输入文本\n
        注意：支持传入中文字符，但需要在模拟器上安装ADBKeyBoard.apk\n
        本方法需要先用setADBIme方法设置为默认输入法
    """
    input_str = "broadcast -a ADB_INPUT_TEXT --es msg %s" % str_text
    return sendAm(adb_path, device_name, input_str)


def hideStatusAndNavigationBar(adb_path, device_name):
    """
        在所有界面下都同时隐藏状态栏和导航栏
    """
    input_str = "put global policy_control immersive.full = *"
    return sendSettings(adb_path, device_name, input_str)


def _getAppActivity(adb_path, device_name, package_name):
    """
        获取指定应用的Activity名称，需要应用正在运行\n
        :param adb_path: adb文件路径
        :param device_name: 安卓设备名
        :param package_name: 应用的包名
    """
    input_str = "dumpsys activity | grep 'mFocusedActivity'"
    shell_res = sendShell(adb_path, device_name, input_str)
    # mFocusedActivity: ActivityRecord{1ea55ae u0 com.next.netcraft.m4399/com.next.netcraft.NCNativeActivity t22}
    shell_output_str = str(shell_res)
    try:
        shell_output_str.rindex(package_name + '/')
    except ValueError as e:
        # 应用未运行会获取失败而报错，返回空字符串
        return ""
    else:
        start_index = shell_output_str.rindex('/')
        end_index = shell_output_str.rindex("Activity")
        res = shell_output_str[start_index + 1:end_index] + "Activity"
    return res


def startApp(adb_path, device_name, package_name, activity_name):
    """
        启动应用，如果应用已启动则把应用恢复到前台\n
        :param adb_path: adb文件路径
        :param device_name: 安卓设备名
        :param package_name: 应用的包名
        :param activity_name: Activity名称
        :return: None
    """
    input_str = "start %s/%s" % (package_name, activity_name)
    return sendAm(adb_path, device_name, input_str)


def stopApp(adb_path, device_name, package_name):
    """
        关闭应用，强制停止应用继续运行\n
        :param adb_path: adb文件路径
        :param device_name: 安卓设备名
        :param package_name: 应用的包名
        :return: None
    """
    input_str = "force-stop %s" % package_name
    return sendAm(adb_path, device_name, input_str)


def reStartApp(adb_path, device_name, package_name, activity_name):
    """
        强行停止目标应用，重启应用到指定的Activity\n
        :param adb_path: adb文件路径
        :param device_name: 安卓设备名
        :param package_name: 应用的包名
        :param activity_name: Activity名称
        :return: None
    """
    if activity_name == "":
        activity_name = _getAppActivity(package_name)
    input_str = "start -S %s/%s" % (package_name, activity_name)
    return sendAm(adb_path, device_name, input_str)


def stopAndClearApp(adb_path, device_name, package_name):
    """
        不仅会停止进程运行，还会清除应用的所有缓存数据\n
        :param adb_path: adb文件路径
        :param device_name: 安卓设备名
        :param package_name: 应用的包名
        :return: None
    """
    input_str = "clear %s" % package_name
    return sendPm(adb_path, device_name, input_str)


def installApp(adb_path, device_name, package_name):
    """ 安装指定应用 """
    pass


def uninstallApp(adb_path, device_name, package_name, is_keep=False):
    """
        卸载指定应用\n
        :param adb_path: adb文件路径
        :param device_name: 安卓设备名
        :param package_name: 应用包名
        :param is_keep: 是否移除软件包后保留数据和缓存目录
    """
    input_str = "uninstall %s" % package_name
    if is_keep:
        input_str = "uninstall -k %s" % package_name
    return sendPm(adb_path, device_name, input_str)


def tap(adb_path, device_name, x, y):
    """ 点击操作，不支持多指触控，且会导致多指触控立即松开 """
    input_str = "tap %d %d" % (x, y)
    return sendInput(adb_path, device_name, input_str)


def longTouch(adb_path, device_name, x, y, time_cost):
    """ 长按操作，不支持多指触控，且会导致多指触控立即松开 """
    input_str = "swipe %d %d %d %d %d" % (x, y, x, y, time_cost)
    return sendInput(adb_path, device_name, input_str)


def swipe(adb_path, device_name, x_start, y_start, x_end, y_end, time_cost):
    """ 滑动操作，不支持多指触控，且会导致多指触控立即松开 """
    input_str = "swipe %d %d %d %d %d" % (x_start, y_start, x_end, y_end, time_cost)
    return sendInput(adb_path, device_name, input_str)


def reboot(adb_path, device_name):
    """
        重启设备\n
        :param adb_path: adb文件路径
        :param device_name: 安卓设备名
    """
    shell_str = '%s -s %s reboot'
    return sendShell(adb_path, device_name, shell_str)


def getDevices(adb_path):
    """
        获取当前的设备列表
    """
    input_str = adb_path + " devices"
    output = subprocess.getoutput(input_str).split("\n")
    devices = []
    if len(output) > 2:
        for i in range(1, len(output) - 1):
            output[i] = output[i].split("\t")[0]
        devices = output[1:-1]
    return devices


if __name__ == '__main__':
    """ 
        用于临时测试模块方法的主函数，方法内容可忽略
        当 Run 当前模块 时，当前模块的 __name__ = __main__
        当 Run 其他模块 时，当前模块的 __name__ = __file_name__ (py文件名)
    """
    pass
