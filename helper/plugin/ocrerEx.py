"""
    Ocr识别插件
    主要用于识别指定范围内的文本与要求的结果是否匹配
"""
from helper.plugin.tablerEx import TABLE_ITEM_TYPE_OCR_CHECK, TABLE_ITEM_TYPE_OCR_READ


def _checkOcr(ocrer, start_x, start_y, end_x, end_y, target_text):
    """
        校验识别的文本结果是否与目标文本相同
    """
    if ocrer.checkText(start_x, start_y, end_x, end_y, target_text):
        return start_x, start_y
    return -1, -1


def _readOcr(ocrer, start_x, start_y, end_x, end_y):
    """
        返回识别的文本结果
    """
    res_text = ocrer.readText2Str(start_x, start_y, end_x, end_y)
    return res_text.lower()


class OcrerEx:
    def __init__(self, ocrer, toucher, logger, timer, tabler_ex):
        self.ocrer = ocrer
        self.toucher = toucher
        self.logger = logger
        self.timer = timer
        self.table = tabler_ex.table

    def ocr(self, table_name, table_item_name, isReturnLoc=False):
        """
            识别操作主函数
            :param table_name: 表名
            :param table_item_name: 字段名
            :param isReturnLoc: 是否返回坐标
            :return: 识别结果
        """
        item = self.table[table_name][table_item_name]
        self.logger.debug("正在识别[", table_name, "][", table_item_name, "]", "->识别范围[",
                          ",".join([str(item.start_x), str(item.start_y), str(item.end_x), str(item.end_y)]), "]")
        x, y = -1, -1
        if item.table_item_type == TABLE_ITEM_TYPE_OCR_CHECK:
            x, y = _checkOcr(self.ocrer, item.start_x, item.start_y, item.end_x, item.end_y, item.target_text)
        elif item.table_item_type == TABLE_ITEM_TYPE_OCR_READ and not isReturnLoc:
            read_res = _readOcr(self.ocrer, item.start_x, item.start_y, item.end_x, item.end_y)
            self.logger.info("识别文本[", table_name, "][", table_item_name, "]->得到文本结果['", read_res, "']")
            return read_res
        if x != -1 and y != -1:
            self.logger.info("识别比对正确[", table_name, "][", table_item_name, "]->比对内容['", item.target_text,
                             "']->返回起点坐标[", ",".join([str(x), str(y)]), "]")
            return (x, y) if isReturnLoc else True
        self.logger.warning("识别比对错误[", table_name, "][", table_item_name, "]->比对内容['", item.target_text,
                            "']")
        return (x, y) if isReturnLoc else False

    def ocrTap(self, table_name, table_item_name, py_x=0, py_y=0):
        """
            识别通过则点击
            :param table_name: 表名
            :param table_item_name: 字段名
            :param py_x: x坐标偏移点击数值
            :param py_y: y坐标偏移点击数值
            :return: 是否点击成功
        """
        x, y = self.ocr(table_name, table_item_name, isReturnLoc=True)
        if x != -1 and y != -1:
            self.logger.info("识别成功[", table_name, "][", table_item_name, "]->坐标[",
                             ",".join([str(x + py_x), str(y + py_y)]), "]->执行操作[", "点击]")
            self.toucher.tap(x + py_x, y + py_y)
            return True
        return False

    def ocrLongTouch(self, table_name, table_item_name, time_cost, py_x=0, py_y=0):
        """
            识别通过则长按
            :param table_name: 表名
            :param table_item_name: 字段名
            :param time_cost: 长按时长
            :param py_x: x坐标偏移点击数值
            :param py_y: y坐标偏移点击数值
            :return: 是否长按成功
        """
        x, y = self.ocr(table_name, table_item_name, isReturnLoc=True)
        if x != -1 and y != -1:
            self.logger.info("识别成功[", table_name, "][", table_item_name, "]->坐标[",
                             ",".join([str(x + py_x), str(y + py_y)]), "]->执行操作[", "长按]->长按时长[", time_cost, "ms]")
            self.toucher.longTouch(x + py_x, y + py_y, time_cost)
            return True
        return False

    def ocrRepeat(self, table_name, table_item_name, time_out=30):
        """ 循环直到找到 """
        while True:
            if not self.ocr(table_name, table_item_name):
                self.timer.sleep(1000)
                time_out -= 1
                if time_out == 0:
                    break
            else:
                return True
        return False

    def ocrTapRepeat(self, table_name, table_item_name, time_out=30, py_x=0, py_y=0):
        """ 循环直到找到并点击成功 """
        while True:
            if not self.ocrTap(table_name, table_item_name, py_x, py_y):
                self.timer.sleep(1000)
                time_out -= 1
                if time_out == 0:
                    break
            else:
                return True
        return False

    def ocrLongTouchRepeat(self, table_name, table_item_name, time_cost, time_out=30, py_x=0, py_y=0):
        """ 循环直到找到并长按成功 """
        while True:
            if not self.ocrLongTouch(table_name, table_item_name, time_cost, py_x, py_y):
                self.timer.sleep(1000)
                time_out -= 1
                if time_out == 0:
                    break
            else:
                return True
        return False
