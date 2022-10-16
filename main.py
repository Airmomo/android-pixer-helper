import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QRect, QSize
from ui.findHelper_ui import UI
from helper.util import imageUtil, logUtil, adbUtil
from helper.entity.androidDevice import AndroidDevice


class FindHelperWindow(QMainWindow, UI):
    def __init__(self):
        # 相当于 QMainWindow.__init__(self)
        super(FindHelperWindow, self).__init__()
        self.setupUi(self)
        self.load_adb_image_button.setEnabled(device_enable)

    """
        热键监控
    """

    def keyPressEvent(self, QKeyEvent):
        self.image_label.recordPixel(widget=self, event=QKeyEvent)
        self.updateMultiColorStr()

    """
        定义槽函数
    """

    def resetAllValue(self):
        """
            重新打开图片时重置所有属性
        """
        self.image_label.cur_x = 0
        self.image_label.cur_y = 0
        self.image_label.cur_c_rgb_16 = ""
        self.image_label.cur_crop_point = 0
        self.retranslateUi(self)

    def openImage(self):
        """
            打开本地图片
        """
        global current_screenshot_path
        # 打开文件路径, 设置文件扩展名过滤,注意用双分号间隔
        img_path, _ = QFileDialog.getOpenFileName(self, caption="打开图片", filter="*.png;;*.bmp;;All Files (*)")
        current_screenshot_path = img_path
        if current_screenshot_path:
            self.resetAllValue()
            self.setLabelImage(current_screenshot_path)

    def openAdbImage(self):
        """
            从模拟器获取截图
        """
        global ADB_PATH, DEVICE_WIDTH, DEVICE_HEIGHT, LOG_LEVEL
        global current_screenshot_path, android_device
        devices = adbUtil.getDevices(ADB_PATH)
        if not devices:
            android_device = None
            msg_box = QMessageBox(QMessageBox.Critical, '错误', '模拟器连接失败\n当前不存在待连接的模拟器')
            msg_box.exec_()
        elif not android_device:
            android_device = AndroidDevice(ADB_PATH, devices[0], DEVICE_WIDTH, DEVICE_HEIGHT, LOG_LEVEL)
        else:
            img_path = android_device.finder.screenshoter.flashAndGetScreenshot()
            current_screenshot_path = img_path
            if current_screenshot_path:
                self.resetAllValue()
                self.setLabelImage(current_screenshot_path)

    def copyCropRange(self):
        """
            复制裁剪区域的坐标
        """
        clipboard = QApplication.clipboard()
        start_x = int(self.crop_start_x.text())
        start_y = int(self.crop_start_y.text())
        end_x = int(self.crop_end_x.text())
        end_y = int(self.crop_end_y.text())
        image = self.image_label.image
        image_width, image_height = int(image.width()), int(image.height())
        start_x, start_y, end_x, end_y = imageUtil.check2RightCropRange(start_x, start_y, end_x, end_y,
                                                                          image_width, image_height)
        clipboard.setText(", ".join([str(start_x), str(start_y), str(end_x), str(end_y)]))

    def saveCropImage(self):
        """
            保存指定区域裁剪出来的图片
        """
        start_x = int(self.crop_start_x.text())
        start_y = int(self.crop_start_y.text())
        end_x = int(self.crop_end_x.text())
        end_y = int(self.crop_end_y.text())
        image_save_path, _ = QFileDialog.getSaveFileName(self, caption="保存裁剪区域", directory=current_screenshot_path)
        try:
            imageUtil.cropPicture(current_screenshot_path, image_save_path, start_x, start_y, end_x, end_y)
        except ValueError:
            msg_box = QMessageBox(QMessageBox.Critical, '错误', '截图保存失败')
            msg_box.exec_()

    def copyColorResStr(self):
        """
            复制多点找色字符串
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(self.multi_color_res_str.text())

    def updateMultiColorStr(self):
        """
            色点选中状态变化事件：更新多点找色字符串
        """
        check_box_list = [self.color_check_1, self.color_check_2, self.color_check_3, self.color_check_4,
                          self.color_check_5, self.color_check_6]
        # 当前选中的复选框的序号
        cur_uncheck_box_index_list = []
        for check_box in check_box_list:
            if check_box.isChecked():
                cur_uncheck_box_index_list.append(check_box.objectName()[-1])
        # 将选中的色值生成多点找色字符串
        if not cur_uncheck_box_index_list:
            self.multi_color_res_str.setText("")
        else:
            primary_x = 0
            primary_y = 0
            str_list = []
            for i, index in enumerate(cur_uncheck_box_index_list):
                color_x_value = int(self.findChild(QLineEdit, "color_x_" + index).text())
                color_y_value = int(self.findChild(QLineEdit, "color_y_" + index).text())
                color_rgb_value = self.findChild(QLineEdit, "color_RGB_" + index).text()
                # zfill 数值前面自动补0
                color_offset_value = self.findChild(QLineEdit, "color_offset_" + index).text().zfill(6)
                # 首个色点
                if i == 0:
                    primary_x = color_x_value
                    primary_y = color_y_value
                    str_list.append("-".join([color_rgb_value, color_offset_value]))
                else:
                    cur_x = color_x_value - primary_x
                    cur_y = color_y_value - primary_y
                    color_str = "-".join([color_rgb_value, color_offset_value])
                    point_str = "|".join([str(cur_x), str(cur_y), color_str])
                    str_list.append(point_str)
            res_str = ",".join(str_list)
            self.multi_color_res_str.setText(res_str)

    """
        辅助函数
    """

    def setLabelImage(self, img_path):
        """
            设置展示的图片
        """
        self.image_label.image = QImage(img_path)
        image_pixmap = QPixmap(self.image_label.image)
        image_width, image_height = image_pixmap.width() + 50, image_pixmap.height() + 50  # 设置为图片的宽度和高度+50
        self.image_label.setGeometry(QRect(0, 0, image_width, image_height))
        self.image_label.setMinimumSize(QSize(image_width, image_height))
        self.image_label.setPixmap(image_pixmap)


# 需要按需设置的变量
# adb文件路径
ADB_PATH = ""
# 设备分辨率的宽度
DEVICE_WIDTH = 720
# 设备的分辨率高度
DEVICE_HEIGHT = 1280
# 日志级别
LOG_LEVEL = logUtil.LEVEL_DEBUG


if __name__ == '__main__':
    global ADB_PATH, DEVICE_WIDTH, DEVICE_HEIGHT, LOG_LEVEL
    # 初始化
    current_screenshot_path = ""
    android_device = None
    device_enable = False
    devices = adbUtil.getDevices(ADB_PATH)
    if devices:
        device_enable = True
        android_device = AndroidDevice(ADB_PATH, devices[0], 720, 1280, logger_level=LOG_LEVEL)
    # 渲染窗口
    app = QApplication(sys.argv)
    window = FindHelperWindow()
    window.show()
    sys.exit(app.exec_())
