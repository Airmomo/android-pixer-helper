"""
    文字识别组件
    Ocrer基于EasyOCR开发，支持超过80种语言的识别
    包括英语、中文（简繁）、阿拉伯文、日文等
    并且该库在不断更新中，未来会支持更多的语言。
    缺点：
        1、图文的分辨率越低，识别准确度越低
        2、识别的语言列表越多，识别准确度越低，速度越慢
        3、对字符的识别准确度非常低
"""
import easyocr
from helper.util import adbUtil

# 支持的语言列表
LANG_CH_CN = 'ch_sim'  # 简体中文
LANG_EN = 'en'  # 英文


def _readText(reader, image_path, is_simple=False):
    """
        识别文本\n
        :param image_path: 图片文件地址，除了 filepath ，您还可以将 OpenCV 图像对象（numpy 数组）或图像文件作为字节传递，原始图像的 URL 也是可以接受的。
        :param is_simple: 是否返回详细的识别结果，默认只返回识别的文本数组
        :return: 识别结果
    """
    if is_simple:
        return reader.readtext(image_path, detail=0)
    return reader.readtext(image_path)


def _readTextOnly(image_path, lang_list, is_simple=False):
    """
        临时修改指定识别的语言列表再进行识别，识别后将恢复原来的语言列表\n
        - 注意：该方法由于需要重新设置和恢复语言列表，所以耗时较长，不推荐频繁使用\n
        - 建议：如果在长时间内需要识别固定的语言，请使用setReader重设语言列表，再使用readText进行识别\n
        :param image_path: 图片文件路径
        :param lang_list: 临时修改指定识别的语言列表
        :param is_simple: 是否返回只返回识别的文本数组，默认返回详细的识别结果
        :return: 识别结果
    """
    reader = easyocr.Reader(lang_list)
    return reader.readtext(image_path, is_simple)


def _readTextOnlyEn(image_path, is_simple=False):
    """
        临时设置只识别出英文结果，识别后将恢复原来的语言列表
        - 注意：该方法由于需要重新设置和恢复语言列表，所以耗时较长，不推荐频繁使用\n
        - 建议：如果在长时间内需要识别固定的语言，请使用setReader重设语言列表，再使用readText进行识别\n
    """
    return _readTextOnly(image_path, LANG_CH_CN, is_simple)


def _readTextOnlyCN(image_path, is_simple=False):
    """
        临时设置只识别出中文结果，识别后将恢复原来的语言列表
        - 注意：该方法由于需要重新设置和恢复语言列表，所以耗时较长，不推荐频繁使用\n
        - 建议：如果在长时间内需要识别固定的语言，请使用setReader重设语言列表，再使用readText进行识别\n
    """
    return _readTextOnly(image_path, LANG_EN, is_simple)


class Ocrer:

    def __init__(self, adb_path, device_name, source_width, source_height, screenshoter):
        self.adb_path = adb_path
        self.device_name = device_name
        self.source_width = source_width
        self.source_height = source_height
        self.screenshoter = screenshoter
        # ['ch_sim','en']，这是要识别的语言列表，ch_sim（简体中文）、en（英文）
        self.lang_list = [LANG_CH_CN, LANG_EN]
        # 该行 reader = easyocr.Reader(['ch_sim','en']) 用于将模型加载到内存中，这需要一些时间，但只需要运行一次
        self.reader = easyocr.Reader(self.lang_list)

    def getLangList(self):
        """
            获取当前识别的语言列表
        """
        return self.lang_list

    def setReader(self, lang_list):
        """
            设置识别的语言列表\n
            用于将模型加载到内存中，每次调用都需要一些时间
        """
        self.reader = easyocr.Reader(lang_list)

    def readText(self, start_x, start_y, end_x, end_y, is_simple=False):
        """
            识别指定范围内的文本，返回结果列表
        """
        # 兼容不同分辨率的设备
        start_x, start_y, end_x, end_y = adbUtil.loc2CompatibleLocAll(self.adb_path, self.device_name,
                                                                      self.source_width,
                                                                      self.source_height, start_x, start_y, end_x,
                                                                      end_y)
        screenshot_crop_path = self.screenshoter.flashAndGetScreenshotCrop(start_x, start_y, end_x, end_y)
        return _readText(self.reader, screenshot_crop_path, is_simple)

    def readText2Str(self, start_x, start_y, end_x, end_y):
        """
            识别指定范围内的文本，将文本结果转为字符串再返回
        """
        text_list = self.readText(start_x, start_y, end_x, end_y, is_simple=True)
        if not text_list:
            return ""
        return "".join(text_list)

    def checkText(self, start_x, start_y, end_x, end_y, target_text):
        """
            识别指定范围内的文本，判断与目标文本是否相同
        """
        res_text = self.readText2Str(start_x, start_y, end_x, end_y)
        return res_text.lower() == target_text.lower()


if __name__ == '__main__':
    pass
