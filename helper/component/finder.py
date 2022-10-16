"""
    图色识别操作组件
    Finder基于Opencv-python开发
    支持模版匹配、多点找色、偏色找色、获取像素点颜色等功能
    作用：找图、找色、获取图色信息
"""
from helper.util import adbUtil, opencvUtil


class Finder:

    def __init__(self, adb_path, device_name, source_width, source_height, screenshoter):
        """ 识图处理对象 """
        self.adb_path = adb_path
        self.device_name = device_name
        self.source_width = source_width
        self.source_height = source_height
        self.screenshoter = screenshoter

    def findImageFull(self, template_path, threshold=opencvUtil.MATCH_THRESHOLD, match_methods=opencvUtil.MATCH_METHOD,
                      match_is_gray=opencvUtil.MATCH_IS_GRAY,
                      match_is_canny=opencvUtil.MATCH_IS_CANNY, match_is_show=opencvUtil.MATCH_IS_SHOW):
        """
            从屏幕左上角开始，实现的全屏找图\n
            :param template_path: 待匹配的模版图片路径
            :param threshold: 相似度阈值
            :param match_methods: 模版匹配方法（必须传列表类型，可多个）
            :param match_is_gray: 是否转为灰度图进行匹配
            :param match_is_canny: 是否启用边缘检测
            :param match_is_show: 是否展示匹配结果
            :return: 结果的相似度大于阈值才会返回坐标，否则返回-1
        """
        screenshot_path = self.screenshoter.flashAndGetScreenshot()
        res_loc = opencvUtil.matchTemplateSameSize(screenshot_path, template_path, match_methods, threshold,
                                                   match_is_gray,
                                                   match_is_canny,
                                                   match_is_show)
        if not res_loc:
            return -1, -1
        return res_loc[0], res_loc[1]

    def findImage(self, start_x, start_y, end_x, end_y, template_path, threshold=opencvUtil.MATCH_THRESHOLD,
                  is_base_source=True, match_methods=opencvUtil.MATCH_METHOD,
                  match_is_gray=opencvUtil.MATCH_IS_GRAY, match_is_canny=opencvUtil.MATCH_IS_CANNY,
                  match_is_show=opencvUtil.MATCH_IS_SHOW):
        """
            从屏幕左上角开始，裁剪截图再后找图，提高找图效率和准确率
            :param start_x: 裁剪起点的x坐标
            :param start_y: 裁剪起点的y坐标
            :param end_x: 裁剪终点的x坐标
            :param end_y: 裁剪终端的y坐标
            :param template_path: 待匹配的模版图片路径
            :param threshold: 相似度阈值
            :param is_base_source: 是否基于原图返回找到的坐标
            :param match_methods: 模版匹配方法（必须传列表类型，可多个）
            :param match_is_gray: 是否转为灰度图进行匹配
            :param match_is_canny: 是否启用边缘检测
            :param match_is_show: 是否展示匹配结果
            :return: 结果的相似度大于阈值才会返回坐标，否则返回-1
        """
        # 兼容不同分辨率的设备
        start_x, start_y, end_x, end_y = adbUtil.loc2CompatibleLocAll(self.adb_path, self.device_name,
                                                                      self.source_width,
                                                                      self.source_height, start_x, start_y, end_x,
                                                                      end_y)
        screenshot_crop_path = self.screenshoter.flashAndGetScreenshotCrop(start_x, start_y, end_x, end_y)
        res_loc = opencvUtil.matchTemplateSameSize(screenshot_crop_path, template_path, match_methods, threshold,
                                                   match_is_gray,
                                                   match_is_canny,
                                                   match_is_show)
        if not res_loc:
            return -1, -1
        if is_base_source:
            return start_x + res_loc[0], start_y + res_loc[1]
        return res_loc[0], res_loc[1]

    def findMultiImageFull(self, template_path, threshold=opencvUtil.MATCH_THRESHOLD,
                           match_methods=opencvUtil.MATCH_METHOD,
                           match_is_gray=opencvUtil.MATCH_IS_GRAY,
                           match_is_canny=opencvUtil.MATCH_IS_CANNY, match_is_show=opencvUtil.MATCH_IS_SHOW):
        """
            从屏幕左上角开始，实现的全屏找图（多模版匹配，返回结果集合）\n
            :param template_path: 待匹配的模版图片路径
            :param threshold: 相似度阈值
            :param match_methods: 模版匹配方法（必须传列表类型，可多个）
            :param match_is_gray: 是否转为灰度图进行匹配
            :param match_is_canny: 是否启用边缘检测
            :param match_is_show: 是否展示匹配结果
            :return: 结果的相似度大于阈值才会返回坐标，否则返回-1
        """
        screenshot_path = self.screenshoter.flashAndGetScreenshot()
        res_locs = opencvUtil.matchMultiTemplateSameSize(screenshot_path, template_path, match_methods, threshold,
                                                         match_is_gray,
                                                         match_is_canny,
                                                         match_is_show)
        if not res_locs:
            return []
        return res_locs

    def findMultiImage(self, start_x, start_y, end_x, end_y, template_path, threshold=opencvUtil.MATCH_THRESHOLD,
                       is_base_source=True, match_methods=opencvUtil.MATCH_METHOD,
                       match_is_gray=opencvUtil.MATCH_IS_GRAY, match_is_canny=opencvUtil.MATCH_IS_CANNY,
                       match_is_show=opencvUtil.MATCH_IS_SHOW):
        """
            从屏幕左上角开始，裁剪截图再后找图，提高找图效率和准确率（多模版匹配，返回结果集合）\n
            :param start_x: 裁剪起点的x坐标
            :param start_y: 裁剪起点的y坐标
            :param end_x: 裁剪终点的x坐标
            :param end_y: 裁剪终端的y坐标
            :param template_path: 待匹配的模版图片路径
            :param threshold: 相似度阈值
            :param is_base_source: 是否基于原图返回找到的坐标
            :param match_methods: 模版匹配方法（必须传列表类型，可多个）
            :param match_is_gray: 是否转为灰度图进行匹配
            :param match_is_canny: 是否启用边缘检测
            :param match_is_show: 是否展示匹配结果
            :return: 结果的相似度大于阈值才会返回坐标，否则返回-1
        """
        start_x, start_y, end_x, end_y = adbUtil.loc2CompatibleLocAll(self.adb_path, self.device_name,
                                                                      self.source_width,
                                                                      self.source_height, start_x, start_y, end_x,
                                                                      end_y)
        screenshot_crop_path = self.screenshoter.flashAndGetScreenshotCrop(start_x, start_y, end_x, end_y)
        res_locs = opencvUtil.matchMultiTemplateSameSize(screenshot_crop_path, template_path, match_methods, threshold,
                                                         match_is_gray,
                                                         match_is_canny,
                                                         match_is_show)
        if not res_locs:
            return []
        if is_base_source:
            res = []
            for res_loc in res_locs:
                res.append((start_x + res_loc[0], start_y + res_loc[1]))
            return res
        return res_locs

    def getColor(self, x, y):
        """
            获取截屏某一像素点的RGB颜色
        """
        screenshot_path = self.screenshoter.flashAndGetScreenshot()
        new_x, new_y = adbUtil.loc2CompatibleLoc(self.adb_path, self.device_name, self.source_width, self.source_height,
                                                 x, y)
        rgb_str, rgb_tuple = opencvUtil.getPixelColor(screenshot_path, new_x, new_y)
        return rgb_str, rgb_tuple

    def getMultiColorCount(self, start_x, start_y, end_x, end_y, multi_color_str):
        """
            获取指定RGB颜色在图片中的数量，支持一个或多个颜色，支持偏色
        """
        start_x, start_y, end_x, end_y = adbUtil.loc2CompatibleLocAll(self.adb_path, self.device_name,
                                                                      self.source_width,
                                                                      self.source_height, start_x, start_y, end_x,
                                                                      end_y)
        # 裁剪图片后找色
        screenshot_crop_path = self.screenshoter.flashAndGetScreenshotCrop(start_x, start_y, end_x, end_y)
        res_count = opencvUtil.getMultiColorCount(screenshot_crop_path, multi_color_str)
        return res_count

    def findMultiColor(self, start_x, start_y, end_x, end_y, match_color_str):
        """
            在指定范围内，从左上到右下进行单点或多点找色，支持偏色\n
            :param start_x: 起点坐标x值
            :param start_y: 起点坐标y值
            :param end_x: 终点坐标x值
            :param end_y: 终点坐标y值
            :param match_color_str: 多点找色字符串（支持偏色也可以不偏色，也可以只输入单色，相似度通过偏色大小来控制）
            :param match_mode: 找色方式（0:从左上到右下/1:从右下到左上/2:从中间到周围）
            :return: 能找到所有色点的主色点的坐标值x,y，找不到则返回-1,-1
        """
        start_x, start_y, end_x, end_y = adbUtil.loc2CompatibleLocAll(self.adb_path, self.device_name,
                                                                      self.source_width,
                                                                      self.source_height, start_x, start_y, end_x,
                                                                      end_y)
        # 使多点找色字符串自适应所有分辨率
        color_list = match_color_str.split(',')
        match_color_str = [color_list[0]]
        for color in color_list[1:]:
            color_py = color.split('|')
            py_x, py_y = int(color_py[0]), int(color_py[1])
            py_new_x, py_new_y = adbUtil.loc2CompatibleLoc(self.adb_path, self.device_name, self.source_width,
                                                           self.source_height, py_x, py_y)
            color_new = color.replace(r'%d|' % py_x, str(py_new_x) + '|').replace(r'%d|' % py_y, str(py_new_y) + '|')
            match_color_str.append(color_new)
        match_color_str = ','.join(match_color_str)
        # 裁剪图片后找色
        screenshot_crop_path = self.screenshoter.flashAndGetScreenshotCrop(start_x, start_y, end_x, end_y)
        res_loc = opencvUtil.matchMultiColor(screenshot_crop_path, match_color_str)
        if not res_loc:
            return -1, -1
        return start_x + res_loc[0], start_y + res_loc[1]
