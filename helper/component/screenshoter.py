"""
    屏幕截图组件
    作用：获取最新的屏幕截图
"""
from helper.util import adbUtil, imageUtil, fileUtil

# 默认的截图设置
SCREENSHOT_FILE_NAME = "screenshot"
SCREENSHOT_FILE_TYPE = "png"
SCREENSHOT_FILE_PUSH_PKG = "/sdcard"
SCREENSHOT_FILE_PULL_PKG = "./temp"


class Screenshoter:
    def __init__(self, adb_path, device_name, file_name=SCREENSHOT_FILE_NAME, file_type=SCREENSHOT_FILE_TYPE,
                 file_push_pkg=SCREENSHOT_FILE_PUSH_PKG, file_pull_pkg=SCREENSHOT_FILE_PULL_PKG):
        self.adb_path = adb_path
        self.device_name = device_name
        self.file_name = file_name
        self.file_type = file_type
        self.file_push_pkg = file_push_pkg
        self.file_pull_pkg = file_pull_pkg

    def flashAndGetScreenshot(self):
        """ 刷新：重新获取屏幕截图 """
        screenshot_path = adbUtil.getScreenshotFilePath(self.adb_path, self.device_name, file_name=self.file_name,
                                                        file_type=self.file_type,
                                                        file_push_pkg=self.file_push_pkg,
                                                        file_pull_pkg=self.file_pull_pkg)
        return screenshot_path

    def flashAndGetScreenshotCrop(self, start_x, start_y, end_x, end_y):
        """ 刷新：重新获取屏幕截图(带裁剪) """
        screenshot_path = self.flashAndGetScreenshot()
        image_save_path = '/'.join(
            [self.file_pull_pkg, self.device_name, self.file_name + "_crop." + self.file_type])
        fileUtil.isFileFatherDirExistAndCreate(image_save_path, True)
        screenshot_crop_path = imageUtil.cropPicture(screenshot_path, image_save_path, start_x, start_y, end_x, end_y)
        return screenshot_crop_path
