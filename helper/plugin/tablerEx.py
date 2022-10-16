"""
    数据库表定义插件
    定义了各种字段用于存储对应的属性
    起到了解包和封包的作用
"""
from helper.util import fileUtil
from helper.error import colorError, opencvError, ocrError

# 字段类型标识
TABLE_ITEM_TYPE_COLOR = "COLOR"
TABLE_ITEM_TYPE_IMAGE = "IMAGE"
TABLE_ITEM_TYPE_OCR_CHECK = "OCR_CHECK"
TABLE_ITEM_TYPE_OCR_READ = "OCR_READ"


class TablerEx:
    def __init__(self, table):
        """
            数据库表对象
        """
        self.table = table


class TablePositionItem:
    def __init__(self, position_x, position_y, test_pass_flag=False):
        """
            坐标点定义
        """
        self.position_x = position_x
        self.position_y = position_y
        # 仅作标识，True表示已通过测试，False表示临时设置
        self._test_pass_flag = test_pass_flag


class TableRangeItem:
    def __init__(self, start_x, start_y, end_x, end_y, test_pass_flag=False):
        """
            范围定义
        """
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        # 仅作标识，True表示已通过测试，False表示临时设置
        self._test_pass_flag = test_pass_flag


class TableColorItem:
    def __init__(self, start_x, start_y, end_x, end_y, match_color_str, test_pass_flag=False):
        """
            找色字段定义
        """
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.match_color_str = match_color_str
        if match_color_str == "":
            raise colorError.ColorNoneError()
        self.table_item_type = TABLE_ITEM_TYPE_COLOR
        # 仅作标识，True表示已通过测试，False表示临时设置
        self._test_pass_flag = test_pass_flag


class TableImageItem:
    def __init__(self, start_x, start_y, end_x, end_y, template_path, threshold=0.9, test_pass_flag=False):
        """
            找图字段定义
        """
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.template_path = template_path
        if not fileUtil.isFileFatherDirExistAndCreate(self.template_path):
            raise opencvError.ImageNoneError()
        self.threshold = threshold
        if not 0 <= threshold <= 1.0:
            raise opencvError.ThresholdOutRangeError()
        self.table_item_type = TABLE_ITEM_TYPE_IMAGE
        # 仅作标识，True表示已通过测试，False表示临时设置
        self._test_pass_flag = test_pass_flag


class TableOcrCheckItem:
    def __init__(self, start_x, start_y, end_x, end_y, target_text, test_pass_flag=False):
        """
            校验识别结果字段定义
        """
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.target_text = target_text
        if target_text == "":
            raise ocrError.TextNoneError()
        self.table_item_type = TABLE_ITEM_TYPE_OCR_CHECK
        # 仅作标识，True表示已通过测试，False表示临时设置
        self._test_pass_flag = test_pass_flag


class TableOcrReadItem:
    def __init__(self, start_x, start_y, end_x, end_y, test_pass_flag=False):
        """
            获取识别结果字段定义
        """
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.table_item_type = TABLE_ITEM_TYPE_OCR_READ
        # 仅作标识，True表示已通过测试，False表示临时设置
        self._test_pass_flag = test_pass_flag
