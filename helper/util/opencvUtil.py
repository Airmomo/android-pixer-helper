"""
    名称：OpenCV 工具类
"""

import warnings
import imutils
import cv2 as cv
import numpy as np

# 推荐的读取图像方式
IMREAD_METHOD = cv.IMREAD_COLOR
# 推荐的边缘检测数值
THRESHOLD_1 = 20
THRESHOLD_2 = 100
# 推荐的模版匹配设置
MATCH_METHOD = cv.TM_CCOEFF_NORMED
MATCH_THRESHOLD = 0.8
MATCH_IS_GRAY = True
MATCH_IS_CANNY = True
MATCH_IS_SHOW = False
# 未归一化的模版匹配方法
MATCH_METHOD_NOT_NORMED = [cv.TM_SQDIFF, cv.TM_CCORR, cv.TM_CCOEFF]
# 已归一化的模版匹配方法
MATCH_METHOD_NORMED = [cv.TM_SQDIFF_NORMED, cv.TM_CCORR_NORMED, cv.TM_CCOEFF_NORMED]


def _getImageByByte(image_byte, flag=IMREAD_METHOD):
    warnings.warn("该方法已失效，无法正常运行", DeprecationWarning)
    """opencv 从数组中读取图片"""
    # 先用 bytearray 将图片数据流转为 ByteArray 格式，再用 numpy.asarray 将 ByteArray 转为数组。
    return cv.imdecode(np.asarray(bytearray(image_byte), dtype=np.uint8), flag)


def _getImageByFile(file_path, flag=IMREAD_METHOD):
    """opencv 从文件中读取图片"""
    return cv.imread(file_path, flag)


def getMatchMethodName(method_index):
    """
        获取模版匹配方法对应的名称\n
        :param method_index: 匹配方法的标识符
        :return:
        """
    """
        # 注意调用 matchTemplate 方法时，原图的模版的图像类型必须一致，否则会出现错误：
            (depth == CV_8U || depth == CV_32F) && type == _templ.type() && _img.dims() <= 2
        # 执行模板匹配，采用的匹配方式 cv.TM_CCOEFF
            cv.TM_SQDIFF------平方差匹配法(数值越小匹配越好，数值越大匹配越坏)
            cv.TM_SQDIFF_NORMED------归一化平方差匹配法(最好匹配0)
            cv.TM_CCORR------相关匹配法(数值越小匹配越坏，数值越大匹配越好)
            cv.TM_CCORR_NORMED------归一化相关匹配法(最坏匹配0)
            cv.TM_CCOEFF------系数匹配法(数值越小匹配越坏，数值越大匹配越好)
            cv.TM_CCOEFF_NORMED------归一化系数匹配法(最好匹配1)【推荐】
    """
    name = "Non-existent Method"
    if method_index == cv.TM_SQDIFF:
        name = "TM_SQDIFF"
    elif method_index == cv.TM_SQDIFF_NORMED:
        name = "TM_SQDIFF_NORMED"
    elif method_index == cv.TM_CCORR:
        name = "TM_CCORR"
    elif method_index == cv.TM_CCORR_NORMED:
        name = "TM_CCORR_NORMED"
    elif method_index == cv.TM_CCOEFF:
        name = "TM_CCOEFF"
    elif method_index == cv.TM_CCOEFF_NORMED:
        name = "TM_CCOEFF_NORMED"
    return name


def getAndInitImage(image_path, isRGB=False, isGray=False, isCanny=False):
    """
        初始化图片，转为opencv的处理格式并进行相关处理
        :param image_path: 图片文件路径
        :param isGray: 是否转换成灰度图 BGR2GRAY
        :param isRGB: 是否将色彩空间设置为RGB
        :param isCanny: 是否启用边缘检测（优化匹配速度，但可能会降低准确度）
        :return:
    """
    image = _getImageByFile(image_path)
    image_ready = image.copy()
    if isRGB:
        image_ready = cv.cvtColor(image_ready, cv.COLOR_BGR2RGB)
    if isGray:
        if isRGB:
            image_ready = cv.cvtColor(image_ready, cv.COLOR_RGB2GRAY)
        else:
            image_ready = cv.cvtColor(image_ready, cv.COLOR_BGR2GRAY)
    if isCanny:
        # 在灰度图中检测边缘，进行模板匹配可提高效率
        # 使用与模板图像完全相同的参数计算图像的Canny边缘表示；
        image_ready = cv.Canny(image_ready, THRESHOLD_1, THRESHOLD_2)
    return image, image_ready


def _showMatchedImageAndRectangle(locs, template, image, title="Image_Matched_Res", wait_time=0):
    """
        展示模版匹配结果并标记匹配位置
        :param locs: 坐标集合
        :param template: 模版
        :param image: 大图
        :param title: 标题
        :param wait_time: 显示时长，0表示无限制
        :return:
    """
    image_copy = image.copy()
    t_height, t_width = template.shape[:2]
    image_rectangle = None
    for loc in locs:
        # 获取每个匹配的位置的坐标
        (cur_start_x, cur_start_y) = loc[0], loc[1]
        (cur_end_x, cur_end_y) = cur_start_x + t_width, cur_start_y + t_height
        # 绘制矩形边框，将匹配区域标注出来
        image_rectangle = cv.rectangle(image_copy, (cur_start_x, cur_start_y), (cur_end_x, cur_end_y), (0, 0, 225), 2)
        """
            img: 画布，可以在同一画布上绘画多次
            pt1=(cur_start_x, cur_start_y)：矩形的左下点
            pt2=(cur_end_x, cur_end_y)：矩形的右下点
            color=(0,0,225)：矩形的边框颜色
            thickness=2：矩形边框宽度
        """
    if image_rectangle is not None:
        # 显示结果,并将匹配值显示在标题栏上
        cv.imshow(title, image_rectangle)
        cv.waitKey(wait_time)
        cv.destroyWindow(title)
        cv.waitKey(1)


def rgb2Str(r, g, b):
    """
        将RGB值元组转为十六进制的RGB字符串
    """
    r = hex(r).zfill(2)
    g = hex(g).zfill(2)
    b = hex(b).zfill(2)
    rgb_str = "".join([r, g, b])
    return rgb_str


def rgbTuple2Str(rgb_tuple):
    """
        将RGB值元组转为十六进制的RGB字符串
    """
    return rgb2Str(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])


def str2RGB(color_str):
    """
        将十六进制的RGB字符串转为对应的RGB值元组
    """
    r = int(color_str[0:2], 16)
    g = int(color_str[2:4], 16)
    b = int(color_str[4:6], 16)
    return r, g, b


def _getAndLimitRGBMinMax(a, b):
    """ 获取RGB数值中每一位对应的最大和最小值范围元组，最小为0，最大为255"""
    if a < 0:
        a = 0
    elif a > 255:
        a = 255
    if b < 0:
        b = 0
    elif b > 255:
        b = 255
    if a > b:
        return b, a
    return a, b


def _getRGBMinMax(rgb_a_r, rgb_a_g, rgb_a_b, rgb_b_r, rgb_b_g, rgb_b_b):
    """ 获取R、G、B对应的最大和最小值范围元组 """
    rgb_r_minmax = _getAndLimitRGBMinMax(rgb_a_r - rgb_b_r, rgb_a_r + rgb_b_r)
    rgb_g_minmax = _getAndLimitRGBMinMax(rgb_a_g - rgb_b_g, rgb_a_g + rgb_b_g)
    rgb_b_minmax = _getAndLimitRGBMinMax(rgb_a_b - rgb_b_b, rgb_a_b + rgb_b_b)
    return rgb_r_minmax, rgb_g_minmax, rgb_b_minmax


def _getRGBTupleMinMax(rgb_tuple_a, rgb_tuple_b):
    """ 获取两个RGB元组R、G、B对应的最大和最小值范围元组 """
    return _getRGBMinMax(rgb_tuple_a[0], rgb_tuple_a[1], rgb_tuple_a[2], rgb_tuple_b[0], rgb_tuple_b[1], rgb_tuple_b[2])


def _checkRGBStrAndGetMinMax(color_rgb_str):
    """
        检查RGB字符串格式并使其合法化，计算其偏色范围并返回
        :param color_rgb_str: RGB字符串
        :return: RGB及其偏色范围元组
    """
    try:
        color_left, color_right = color_rgb_str.split('-')
    except ValueError:
        color_left, color_right = color_rgb_str[-6:].zfill(6), ""
    if color_right.replace(' ', '') == "":
        color_right = "000000"
    color_left_rgb = str2RGB(color_left)
    color_right_rgb = str2RGB(color_right)
    # ((r_min, r_max),(g_min, g_max),(b_min, b_max))
    color_rgb_minmax = _getRGBTupleMinMax(color_left_rgb, color_right_rgb)
    return color_rgb_minmax


def _isInRGBRange(rgb_value, rgb_min, rgb_max):
    return rgb_min <= rgb_value <= rgb_max


def _isRGBInRGBRange(rgb_r, rgb_g, rgb_b, rgb_r_min, rgb_r_max, rgb_g_min, rgb_g_max, rgb_b_min, rgb_b_max):
    return _isInRGBRange(rgb_r, rgb_r_min, rgb_r_max) and _isInRGBRange(rgb_g, rgb_g_min, rgb_g_max) and _isInRGBRange(
        rgb_b, rgb_b_min, rgb_b_max)


def _isRGBTupleInRGBTupleRange(rgb_tuple, rgb_tuple_minmax):
    return _isRGBInRGBRange(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2], rgb_tuple_minmax[0][0], rgb_tuple_minmax[0][1],
                            rgb_tuple_minmax[1][0], rgb_tuple_minmax[1][1], rgb_tuple_minmax[2][0],
                            rgb_tuple_minmax[2][1])


def matchTemplateSameSize(image_path, template_path, match_method=MATCH_METHOD, threshold=MATCH_THRESHOLD,
                          isGray=MATCH_IS_GRAY, isCanny=MATCH_IS_CANNY, isShow=MATCH_IS_SHOW):
    """
        只返回最佳匹配结果的单尺寸的模版匹配方法\n
        :param image_path: 待查找的图片路径
        :param template_path: 模版图片路径
        :param match_method: 模版匹配方法
        :param threshold: 相似度阈值
        :param isGray: 是否转换成灰度图
        :param isCanny: 是否启用边缘检测（优化匹配速度，但可能会降低准确度）
        :param isShow: 是否显示模版匹配结果
        :return: 模版在大图中最匹配的坐标位置和相似度
        注意1：模版和原图的图像类型和尺寸需要保持一致，但该问题在新版本中貌似已经支持了多尺寸的识别，但模版尺寸一定不能大于原图
        注意2：如果单尺寸的模版匹配方法实际匹配结果或速度不佳，推荐使用多尺寸的模版匹配方法
    """
    image, image_ready = getAndInitImage(image_path, False, isGray, isCanny)
    template, template_ready = getAndInitImage(template_path, False, isGray, isCanny)
    # 模版匹配
    result = cv.matchTemplate(image_ready, template_ready, match_method)
    # 归一化处理
    """
        结果归一化处理
        src: 待归一化的数据
        dst: 存储归一化结果的变量
        cv.NORM_MINMAX: 数组的数值被平移或缩放到一个指定的范围，线性归一化，一般较常用。
        例如：未归一化处理的匹配方法TM_CCOEFF，其匹配值越大表示越好，但进行归一化处理后，可以将其值缩放到1以内，可用于与其他匹配方法得到的归一化结果相比较来得到最优结果
        缺点：归一化之后的匹配算法效果好，但是相应的，耗时也会增加
    """
    if match_method in MATCH_METHOD_NOT_NORMED:
        cv.normalize(result, result, 0, 1, cv.NORM_MINMAX, -1)
    # 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
    (min_val, max_val, min_loc, max_loc) = cv.minMaxLoc(result)
    res_loc = None
    # 筛选结果匹配阈值
    if match_method <= cv.TM_SQDIFF_NORMED and min_val <= threshold:
        # 对于cv.TM_SQDIFF / cv.TM_SQDIFF_NORMED方法，min_val越趋近与0匹配度越好，所以取匹配度最小的位置min_loc
        res_loc = min_loc
    elif match_method > cv.TM_SQDIFF_NORMED and max_val >= threshold:
        # 对于其他方法max_val越趋近于1匹配度越好，所以取匹配度最大的位置max_loc
        res_loc = max_loc
        # 绘制矩形边框，将匹配区域标注出来
    if isShow and res_loc:
        _showMatchedImageAndRectangle([res_loc], template, image)
    return res_loc


def matchMultiTemplateSameSize(image_path, template_path, match_method=MATCH_METHOD, threshold=MATCH_THRESHOLD,
                               isGray=MATCH_IS_GRAY, isCanny=MATCH_IS_CANNY, isShow=MATCH_IS_SHOW):
    """
        可匹配多个结果的单尺寸的模版匹配方法\n
        :param image_path: 待查找的图片路径
        :param template_path: 模版图片路径
        :param match_method: 模版匹配方法
        :param threshold: 相似度阈值
        :param isGray: 是否转换成灰度图
        :param isCanny: 是否启用边缘检测（优化匹配速度，但可能会降低准确度）
        :param isShow: 是否显示模版匹配结果
        :return: 模版在大图中最匹配的坐标位置和相似度
        注意1：模版和原图的图像类型和尺寸需要保持一致，但该问题在新版本中貌似已经支持了多尺寸的识别，但模版尺寸一定不能大于原图
        注意2：如果单尺寸的模版匹配方法实际匹配结果或速度不佳，推荐使用多尺寸的模版匹配方法
    """
    image, image_ready = getAndInitImage(image_path, False, isGray, isCanny)
    template, template_ready = getAndInitImage(template_path, False, isGray, isCanny)
    # 模版匹配
    result = cv.matchTemplate(image_ready, template_ready, match_method)
    # 归一化处理
    if match_method in MATCH_METHOD_NOT_NORMED:
        cv.normalize(result, result, 0, 1, cv.NORM_MINMAX, -1)
    # 根据相似度阈值筛选结果
    if match_method <= cv.TM_SQDIFF_NORMED:
        accord_locs = np.where(result <= threshold)
    else:
        accord_locs = np.where(result >= threshold)
    res_locs = zip(*accord_locs[::-1])
    # 展示匹配结果
    if isShow:
        _showMatchedImageAndRectangle(res_locs, template, image)
    return res_locs


def matchTemplateMoreSize(image_path, template_path, match_method=MATCH_METHOD, threshold=MATCH_THRESHOLD,
                          isGray=MATCH_IS_GRAY, isCanny=MATCH_IS_CANNY, isShow=MATCH_IS_SHOW):
    """
        只返回最佳匹配结果的多尺寸的模版匹配方法\n
        :param image_path: 待查找的图片路径
        :param template_path: 模版图片路径
        :param match_method: 模版匹配方法（必须传列表）
        :param threshold: 相似度阈值
        :param isGray: 是否转换成灰度图
        :param isCanny: 是否启用边缘检测（优化匹配速度，但可能会降低准确度）
        :param isShow: 是否显示模版匹配结果
        :return: 模版在大图中最匹配的坐标位置和相似度
        优化：使用边缘而不是原始图像进行模板匹配可以大大提高模板匹配的精度
    """
    # 加载模板图像，转换灰度图，检测边缘
    image, image_ready = getAndInitImage(image_path, False, isGray, isCanny)
    template, template_ready = getAndInitImage(template_path, False, isGray, isCanny)
    t_height, t_width = template.shape[:2]
    # 遍历缩放的图像尺寸
    best_found = None
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        """
            np.linspace(start, end, nums): 在start和stop之间返回均匀间隔的数据
                start：起始数字；
                stop：结束数字；
                num：节点数，默认为50；
            [::-1]: 反转数组
        """
        # 根据scale比例缩放图像，并保持其宽高比
        image_resized = imutils.resize(image_ready, width=int(image_ready.shape[1] * scale))
        r = image_ready.shape[1] / float(image_resized.shape[1])
        # 缩放到图像比模板小，则终止
        if image_resized.shape[0] < t_height or image_resized.shape[1] < t_width:
            break
        # 模版匹配
        result = cv.matchTemplate(image_resized, template_ready, match_method)
        # 归一化处理
        if match_method in MATCH_METHOD_NOT_NORMED:
            cv.normalize(result, result, 0, 1, cv.NORM_MINMAX, -1)
        # 寻找矩阵
        (min_val, max_val, min_loc, max_loc) = cv.minMaxLoc(result)
        # 选择匹配方式对应的最佳匹配位置
        if match_method <= cv.TM_SQDIFF_NORMED and min_val <= threshold:
            best_found = (min_loc, r)
        elif match_method > cv.TM_SQDIFF_NORMED and max_val >= threshold:
            best_found = (max_loc, r)
    # 解包簿记变量并基于调整大小的比率，计算出边界框（x，y）坐标
    (best_loc, r) = best_found
    (best_start_x, best_start_y) = (int(best_loc[0] * r), int(best_loc[1] * r))
    res_loc = (best_start_x, best_start_y)
    # 在检测结果上绘制边界框并展示图像
    if isShow:
        _showMatchedImageAndRectangle([res_loc], template, image)
    return res_loc


def matchMultiTemplateMoreSize(image_path, template_path, match_method=MATCH_METHOD, threshold=MATCH_THRESHOLD,
                               isGray=MATCH_IS_GRAY, isCanny=MATCH_IS_CANNY, isShow=MATCH_IS_SHOW):
    """
        返回多个匹配结果的多尺寸的模版匹配方法\n
        :param image_path: 待查找的图片路径
        :param template_path: 模版图片路径
        :param match_method: 模版匹配方法（必须传列表）
        :param threshold: 相似度阈值
        :param isGray: 是否转换成灰度图
        :param isCanny: 是否启用边缘检测（优化匹配速度，但可能会降低准确度）
        :param isShow: 是否显示模版匹配结果
        :return: 模版在大图中最匹配的坐标位置和相似度
        优化：使用边缘而不是原始图像进行模板匹配可以大大提高模板匹配的精度
    """
    # 加载模板图像，转换灰度图，检测边缘
    image, image_ready = getAndInitImage(image_path, False, isGray, isCanny)
    template, template_ready = getAndInitImage(template_path, False, isGray, isCanny)
    t_height, t_width = template.shape[:2]
    # 遍历缩放的图像尺寸
    res_locs = []
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        """
            np.linspace(start, end, nums): 在start和stop之间返回均匀间隔的数据
                start：起始数字；
                stop：结束数字；
                num：节点数，默认为50；
            [::-1]: 反转数组
        """
        # 根据scale比例缩放图像，并保持其宽高比
        image_resized = imutils.resize(image_ready, width=int(image_ready.shape[1] * scale))
        r = image_ready.shape[1] / float(image_resized.shape[1])
        # 缩放到图像比模板小，则终止
        if image_resized.shape[0] < t_height or image_resized.shape[1] < t_width:
            break
        # 模版匹配
        result = cv.matchTemplate(image_resized, template_ready, match_method)
        # 归一化处理
        if match_method in MATCH_METHOD_NOT_NORMED:
            cv.normalize(result, result, 0, 1, cv.NORM_MINMAX, -1)
        # 根据相似度阈值筛选结果
        if match_method <= cv.TM_SQDIFF_NORMED:
            accord_locs = np.where(result <= threshold)
        else:
            accord_locs = np.where(result >= threshold)
        # 解包簿记变量并基于调整大小的比率，计算出边界框（x，y）坐标
        for loc in zip(*accord_locs[::-1]):
            (best_start_x, best_start_y) = (int(loc[0] * r), int(loc[1] * r))
            res_locs.append((best_start_x, best_start_y))
    # 在检测结果上绘制边界框并展示图像
    if isShow:
        _showMatchedImageAndRectangle(res_locs, template, image)
    return res_locs


def getPixelColor(image_path, x, y):
    """
        获取图片中指定位置的像素颜色
    """
    _, image_ready = getAndInitImage(image_path, isRGB=True)
    real_rgb = image_ready[y, x]
    return rgbTuple2Str(real_rgb), real_rgb


def getMultiColorCount(image_path, multi_color_str):
    """
        获取多个RGB颜色在图片中的总数
        注意：\n
            - 字符串格式：主色点的RGB十六进制值-偏色值，偏移坐标x值｜偏移坐标y值｜色点的RGB十六进制值-偏色值\n
            - 偏色值：设定一个颜色范围（如：000000～FFFFFF），当获取的颜色在这个范围内的时候则认为已找到\n
            - 举例：'DD5044-000000,E3E3E3-000000,EFEFEF-000000'\n
            - 或者：'DD5044,E3E3E3,EFEFEF'
        :param image_path: 图片文件路径
        :param multi_color_str:
        :return:
    """
    count = 0
    _, image_ready = getAndInitImage(image_path, isRGB=True)
    height, width = image_ready.shape[:2]
    image_ready = np.array(image_ready)
    color_all_list = []
    for color in multi_color_str.split(','):
        color_rgb_minmax = _checkRGBStrAndGetMinMax(color)
        color_all_list.append(color_rgb_minmax)
    for row in range(0, height):
        for col in range(0, width):
            loc_rgb = tuple(image_ready[row, col])
            for color_rgb_minmax in color_all_list:
                if _isRGBTupleInRGBTupleRange(loc_rgb, color_rgb_minmax):
                    count += 1
                    break
    return count


def parseMultiColorStr(colors: list):
    """
        将色点集合封装成多点找色字符串\n
        :param colors: 色点集合，色点格式（x, y, RGB十六进制值，偏色十六进制值）
        :return: 多点找色字符串
    """
    if not colors:
        return ""
    # [x, y, RGB_16, PS_16]
    primary_color = colors[0]
    start_x, start_y = primary_color[:2]
    start_str = '-'.join(primary_color[-2:])
    res = [start_str]
    for color in colors[1:]:
        color_str = '-'.join(color[-2:])
        bet_x, bet_y = color[0] - start_x, color[1] - start_y
        res_str = '｜'.join([str(bet_x), str(bet_y), color_str])
        res.append(res_str)
    return ','.join(res)


def matchMultiColor(image_path, match_color_str):
    """
        从左上到右下进行单点/多点找色，支持偏色
        实现思路：
            1、在图片中逐一遍历像素点的RGB值，并与主色点的RGB值进行比较\n
            2、如果相同，则遍历其他色点的偏移找到其对应坐标的RGB值\n
            3、将偏移找到的像素点的RGB值与要求的偏移色点值进行比较\n
            4、如果都相同则表示该坐标点能够满足主色点和偏移色点的要求，返回找到的主色点的坐标\n
            5、如果有一个不相同，则跳过继续遍历其他像素点，如果遍历完了都找不到，则返回-1，-1\n
        注意：\n
            - 字符串格式：主色点的RGB十六进制值-偏色值，偏移坐标x值｜偏移坐标y值｜色点的RGB十六进制值-偏色值\n
            - 偏色值：设定一个颜色范围（如：000000～FFFFFF），当获取的颜色在这个范围内的时候则认为已找到\n
            - 举例：'DD4E42-000000,-23|19|E3E3E3-000000,-5|28|EFEFEF-000000'\n
            - 或者：'DD4E42,-23|19|E3E3E3,-5|28|EFEFEF'\n
    :param image_path: 图片路径
    :param match_color_str: 多点找色字符串（相似度通过偏色大小来控制）
    :return: 能找到所有色点，则返回主色点的坐标元组，找不到则返回None
    """
    res_loc = None
    if match_color_str.replace(' ', '') == "":
        return res_loc
    _, image_ready = getAndInitImage(image_path, isRGB=True)
    height, width = image_ready.shape[:2]
    image_ready = np.array(image_ready)
    color_list = match_color_str.split(',')
    color_main = color_list[0]  # 主色点
    color_else_list = []  # 其他色点
    color_py_list = []  # 其他色点的偏移
    color_all_list = [color_main]  # 所有色点
    for color in color_list[1:]:
        color_item = color.split('|')
        color_py_list.append((int(color_item[0]), int(color_item[1])))
        color_else_list.append(color_item[2])
        color_all_list.append(color_item[2])
    # 计算所有色点的偏色范围
    color_rgb_range_list = []
    for color in color_all_list:
        color_rgb_minmax = _checkRGBStrAndGetMinMax(color)
        color_rgb_range_list.append(color_rgb_minmax)
    color_else_rgb_range_list = enumerate(color_rgb_range_list[1:])
    # ------ NewMethod Begin ------
    # 获取主色点
    color_main_rgb_range = color_rgb_range_list[0]
    # 利用numpy计算出像素矩阵中符合主色点RGB值范围的所有坐标位置
    flag_r = np.logical_and(color_main_rgb_range[0][0] <= image_ready[:, :, 0:1],
                            image_ready[:, :, 0:1] <= color_main_rgb_range[0][1])
    flag_g = np.logical_and(color_main_rgb_range[1][0] <= image_ready[:, :, 1:2],
                            image_ready[:, :, 1:2] <= color_main_rgb_range[1][1])
    flag_b = np.logical_and(color_main_rgb_range[2][0] <= image_ready[:, :, 2:3],
                            image_ready[:, :, 2:3] <= color_main_rgb_range[2][1])
    flag_rgb = np.logical_and(flag_r, flag_g, flag_b)
    # 计算出符合调节的坐标集合，并转为列表
    image_ready_where_loc = np.argwhere(np.all(flag_rgb, axis=2)).tolist()
    # 遍历每一个符合条件的坐标
    for where in image_ready_where_loc:
        loc_x, loc_y = where[1], where[0]
        all_color_pass = True
        # 已匹配主色，逐一判断当前坐标的相对偏移的色值是否匹配
        for i, color_rgb_range in color_else_rgb_range_list:
            color_py = color_py_list[i]
            py_x, py_y = color_py[0], color_py[1]
            real_x, real_y = loc_x + py_x, loc_y + py_y
            # 判断偏移后的坐标是否越界
            if 0 <= real_x < width and 0 <= real_y < height:
                real_rgb = tuple(image_ready[real_y, real_x])
                if not _isRGBTupleInRGBTupleRange(real_rgb, color_rgb_range):
                    all_color_pass = False
                    break
        if all_color_pass:
            res_loc = (loc_x, loc_y)
            return res_loc
    return res_loc
    # ------ NewMethod Ending ------

    # ------ OldMethod Begin ------
    # 从左上逐行往下找色
    # warnings.warn("不推荐通过该方法来进行多点找色，遍历每一个像素点来找色的效率太低，时间复杂度太高，平均耗时以秒为单位", DeprecationWarning)
    # for row in range(0, height):
    #     for col in range(0, width):
    #         loc_x, loc_y = col, row
    #         loc_rgb = tuple(image_ready[row, col])
    #         color_main_rgb_range = color_rgb_range_list[0]
    #         # 判断是否匹配主色
    #         if _isRGBTupleInRGBTupleRange(loc_rgb, color_main_rgb_range):
    #             all_color_pass = True
    #             # 已匹配主色，逐一判断当前坐标的相对偏移的色值是否匹配
    #             for i, color_rgb_range in color_else_rgb_range_list:
    #                 color_py = color_py_list[i]
    #                 py_x, py_y = color_py[0], color_py[1]
    #                 real_x, real_y = loc_x + py_x, loc_y + py_y
    #                 # 判断偏移后的坐标是否越界
    #                 if 0 <= real_x < width and 0 <= real_y < height:
    #                     real_rgb = tuple(image_ready[real_y, real_x])
    #                     if not _isRGBTupleInRGBTupleRange(real_rgb, color_rgb_range):
    #                         all_color_pass = False
    #                         break
    #             if all_color_pass:
    #                 res_loc = (loc_x, loc_y)
    #                 return res_loc
    # return res_loc
    # ------ OldMethod Ending ------


if __name__ == '__main__':
    """ 
        用于临时测试模块方法的主函数，方法内容可忽略
        当 Run 当前模块 时，当前模块的 __name__ = __main__
        当 Run 其他模块 时，当前模块的 __name__ = __file_name__ (py文件名)
    """
    pass
