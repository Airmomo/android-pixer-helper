from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor


class MyImageLabel(QLabel):

    image = None
    cur_x = 0
    cur_y = 0
    cur_c_rgb_16 = ""
    cur_crop_point = 0

    def mousePressEvent(self, QMouseEvent):
        self.setFocusPolicy(Qt.ClickFocus)
        if self.image:
            self.setCurPixel(QMouseEvent)
            # nativeParentWidget 获取祖父控件
            parent_widget = self.nativeParentWidget()
            # 更新当前坐标信息
            self.updatePositionPixel(parent_widget)
            # 更新截图起点和终点
            self.updateCropPosition(parent_widget)

    def setCurPixel(self, event):
        """
            设置坐标属性
        """
        max_x, max_y = self.image.width(), self.image.height()
        back_x, back_y = self.cur_x, self.cur_y
        self.cur_x = event.pos().x()
        self.cur_y = event.pos().y()
        if self.cur_x > max_x or self.cur_y > max_y:
            self.cur_x, self.cur_y = back_x, back_y
            return
        cur_c = self.image.pixel(self.cur_x, self.cur_y)  # color code (integer): 3235912
        cur_c_rgb = QColor(cur_c).getRgb()[:3]  # 8bit RGBA: (255, 23, 0, 255)
        self.cur_c_rgb_16 = "".join([hex(cur_c_rgb[0])[-2:].replace('x', '0'), hex(cur_c_rgb[1])[-2:].replace('x', '0'), hex(cur_c_rgb[2])[-2:].replace('x', '0')])
        self.cur_c_rgb_16 = str.upper(self.cur_c_rgb_16)

    def updateCropPosition(self, widget):
        """
            更新裁剪的起点和终点
            当cur_crop_point为偶数时更新起点，奇数时更新终点
        """
        if self.cur_crop_point % 2 == 0:
            widget.crop_start_x.setText(str(self.cur_x))
            widget.crop_start_y.setText(str(self.cur_y))
        else:
            widget.crop_end_x.setText(str(self.cur_x))
            widget.crop_end_y.setText(str(self.cur_y))
        self.cur_crop_point += 1

    def updatePositionPixel(self, widget):
        """
            更新当前坐标信息
        """
        widget.position_x.setText(str(self.cur_x))
        widget.position_y.setText(str(self.cur_y))
        widget.position_rgb.setText(self.cur_c_rgb_16)

    def updateRecordPixel(self, check_box, color_x, color_y, color_RGB):
        """
            更新某一色点记录，更新后自动选中
        """
        color_x.setText(str(self.cur_x))
        color_y.setText(str(self.cur_y))
        color_RGB.setText(self.cur_c_rgb_16)
        check_box.setChecked(True)

    def recordPixel(self, widget, event):
        """
            快捷键 crtl/command + 数字键1～6，更新对应的色点记录
        """
        mo, key = event.modifiers(), event.key()
        if mo == Qt.ControlModifier:
            if key == Qt.Key_1:
                self.updateRecordPixel(widget.color_check_1, widget.color_x_1, widget.color_y_1, widget.color_RGB_1)
            elif key == Qt.Key_2:
                self.updateRecordPixel(widget.color_check_2, widget.color_x_2, widget.color_y_2, widget.color_RGB_2)
            elif key == Qt.Key_3:
                self.updateRecordPixel(widget.color_check_3, widget.color_x_3, widget.color_y_3, widget.color_RGB_3)
            elif key == Qt.Key_4:
                self.updateRecordPixel(widget.color_check_4, widget.color_x_4, widget.color_y_4, widget.color_RGB_4)
            elif key == Qt.Key_5:
                self.updateRecordPixel(widget.color_check_5, widget.color_x_5, widget.color_y_5, widget.color_RGB_5)
            elif key == Qt.Key_6:
                self.updateRecordPixel(widget.color_check_6, widget.color_x_6, widget.color_y_6, widget.color_RGB_6)
