"""
    通过Table对象来实现找图找色、识别点击的插件
"""
from helper.plugin.tablerEx import TABLE_ITEM_TYPE_COLOR, TABLE_ITEM_TYPE_IMAGE


def _findColor(finder, start_x, start_y, end_x, end_y, match_color_str):
    """
        多点找色，支持偏色
    """
    x, y = finder.findMultiColor(start_x, start_y, end_x, end_y, match_color_str)
    return x, y


def _findImage(finder, start_x, start_y, end_x, end_y, template_path, threshold):
    """
        多尺寸找图
    """
    x, y = finder.findImage(start_x, start_y, end_x, end_y, template_path, threshold)
    return x, y


class FinderEx:
    def __init__(self, finder, toucher, phone, logger, timer, tabler_ex):
        self.finder = finder
        self.toucher = toucher
        self.phone = phone
        self.logger = logger
        self.timer = timer
        self.table = tabler_ex.table

    def tap(self, table_name, table_item_name):
        """
            点击操作主函数
            :param table_name: 表名
            :param table_item_name: 字段名
            :return: 点击结果
        """
        item = self.table[table_name][table_item_name]
        self.logger.info("正在点击[", table_name, "][", table_item_name, "]", "->点击坐标[",
                         ",".join([str(item.position_x), str(item.position_y)]), "]")
        return self.toucher.tapSingle(item.position_x, item.position_y)

    def longTouch(self, table_name, table_item_name, time_cost):
        """
            长按操作主函数
            :param table_name: 表名
            :param table_item_name: 字段名
            :param time_cost: 长按时长
            :return: 点击结果
        """
        item = self.table[table_name][table_item_name]
        self.logger.info("正在长按[", table_name, "][", table_item_name, "]", "->长按坐标[",
                         ",".join([str(item.position_x), str(item.position_y)]), "]->长按时长[", time_cost, "s]")
        return self.toucher.longTouchSingle(item.position_x, item.position_y, time_cost)

    def find(self, table_name, table_item_name, isReturnLoc=False):
        """
            查找操作主函数
            :param table_name: 表名
            :param table_item_name: 字段名
            :param isReturnLoc: 是否返回坐标
            :return: 查找结果
        """
        item = self.table[table_name][table_item_name]
        self.logger.debug("正在查找[", table_name, "][", table_item_name, "]", "->查找范围[",
                          ",".join([str(item.start_x), str(item.start_y), str(item.end_x), str(item.end_y)]), "]")
        x, y = -1, -1
        if item.table_item_type == TABLE_ITEM_TYPE_COLOR:
            x, y = _findColor(self.finder, item.start_x, item.start_y, item.end_x, item.end_y, item.match_color_str)
        elif item.table_item_type == TABLE_ITEM_TYPE_IMAGE:
            x, y = _findImage(self.finder, item.start_x, item.start_y, item.end_x, item.end_y, item.template_path,
                              item.threshold)
        if x != -1 and y != -1:
            self.logger.info("查找成功[", table_name, "][", table_item_name, "]->坐标[", ",".join([str(x), str(y)]), "]")
            return (x, y) if isReturnLoc else True
        self.logger.warning("未找到[", table_name, "][", table_item_name, "]")
        return (x, y) if isReturnLoc else False

    def findTap(self, table_name, table_item_name, py_x=0, py_y=0):
        """
            查找通过则点击
            :param table_name: 表名
            :param table_item_name: 字段名
            :param py_x: x坐标偏移点击数值
            :param py_y: y坐标偏移点击数值
            :return: 是否点击成功
        """
        x, y = self.find(table_name, table_item_name, isReturnLoc=True)
        if x != -1 and y != -1:
            self.logger.info("查找成功[", table_name, "][", table_item_name, "]->坐标[", ",".join([str(x), str(y)]),
                             "]->执行操作[", "点击]")
            self.toucher.tapSingle(x + py_x, y + py_y)
            return True
        return False

    def findLongTouch(self, table_name, table_item_name, time_cost, py_x=0, py_y=0):
        """
            查找通过则长按
            :param table_name: 表名
            :param table_item_name: 字段名
            :param time_cost: 长按时长
            :param py_x: x坐标偏移点击数值
            :param py_y: y坐标偏移点击数值
            :return: 是否长按成功
        """
        x, y = self.find(table_name, table_item_name, isReturnLoc=True)
        if x != -1 and y != -1:
            self.logger.info("查找成功[", table_name, "][", table_item_name, "]->坐标[", ",".join([str(x), str(y)]),
                             "]->执行操作[", "长按]->长按时长[", time_cost, "ms]")
            self.toucher.longTouchSingle(x + py_x, y + py_y, time_cost)
            return True
        return False

    def findTapAndInputStr(self, table_name, table_item_name, input_str, py_x=0, py_y=0):
        """
            找到并点击输入框，出现光标后输入字符串
            :param table_name: 表名
            :param table_item_name: 字段名
            :param input_str: 输入的字符串
            :param py_x: 偏移的x坐标值
            :param py_y: 偏移的y坐标值
            :return: 成功返回True，失败返回False
        """
        if self.findTap(table_name, table_item_name, py_x, py_y):
            self.timer.sleep(2000)
            self.phone.inputStrText(str(input_str))
            if self.find("输入框", "输入窗口底部边框") or self.find("输入框", "游戏内底部输入框"):
                self.phone.tapBack()
            return True
        return False

    def findTapThenClearAndInputStr(self, table_name, table_item_name, input_str, py_x=0, py_y=0):
        """
            找到并点击输入框，出现光标后全选并清空输入框内容，再输入字符串
            :param table_name: 表名
            :param table_item_name: 字段名
            :param input_str: 输入的字符串
            :param py_x: 偏移的x坐标值
            :param py_y: 偏移的y坐标值
            :return: 成功返回True，失败返回False
        """
        if self.findTap(table_name, table_item_name, py_x, py_y):
            self.timer.sleep(1500)
            # 是否是弹出式输入框
            input_mode_box = self.find("输入框", "输入窗口底部边框")
            # 是否是游戏内底部输入框
            input_mode_bottom = self.find("输入框", "游戏内底部输入框")
            # 长按，弹出输入菜单
            if input_mode_box:
                self.toucher.longTouchSingle(25, 50, 1500)
            elif input_mode_bottom:
                pass
            else:
                self.findLongTouch(table_name, table_item_name, 1500, py_x, py_y)
            self.timer.sleep(1000)

            # ------ OldMethod Begin ------
            # # 点击全选
            # if self.findTap("输入框", "白色样式全选按钮") or self.findTap("输入框", "黑色样式全选按钮"):
            #     self.timer.sleep(1000)
            # # 清空字符串：点击剪切
            # if self.findTap("输入框", "白色样式剪切按钮") or self.findTap("输入框", "黑色样式剪切按钮"):
            #     self.timer.sleep(1000)
            # ------ OldMethod Ending ------

            # ------ NewMethod Begin ------
            if input_mode_bottom:
                for i in range(0, 20):
                    self.phone.tapDel()
            else:
                # 点击全选
                self.findTap("输入框", "白色样式全选按钮") or self.findTap("输入框", "黑色样式全选按钮")
                # 清空字符串：全选后点击删除键
                self.phone.tapDel()
            # ------ NewMethod Ending ------

            # 输入新的字符串
            self.phone.inputStrText(str(input_str))
            self.timer.sleep(1000)
            # 弹出式输入框需要点击返回
            if input_mode_box or input_mode_bottom:
                self.phone.tapBack()
                self.timer.sleep(1500)
            return True
        return False

    def findRepeat(self, table_name, table_item_name, time_out=30):
        """ 循环直到找到 """
        while True:
            if not self.find(table_name, table_item_name):
                self.timer.sleep(1000)
                time_out -= 1
                if time_out == 0:
                    break
            else:
                return True
        return False

    def findTapRepeat(self, table_name, table_item_name, time_out=30, py_x=0, py_y=0):
        """ 循环直到找到并点击成功 """
        while True:
            if not self.findTap(table_name, table_item_name, py_x, py_y):
                self.timer.sleep(1000)
                time_out -= 1
                if time_out == 0:
                    break
            else:
                return True
        return False

    def findLongTouchRepeat(self, table_name, table_item_name, time_cost, time_out=30, py_x=0, py_y=0):
        """ 循环直到找到并长按成功 """
        while True:
            if not self.findLongTouch(table_name, table_item_name, time_cost, py_x, py_y):
                self.timer.sleep(1000)
                time_out -= 1
                if time_out == 0:
                    break
            else:
                return True
        return False
