import base64
from PIL import Image


def _check2LeftLessRight(left, right):
    """
        校验并保持左边的变量大于右边的变量
    """
    if not left < right:
        right ^= left
        left ^= right
        right ^= left
    return left, right


def _check2LimitRange(value, range_min, range_max):
    """
        校验并保持某个值不会超过指定的范围
    """
    if value < range_min:
        value = range_min
    elif value > range_max:
        value = range_max
    return value


def getImageBase64(file_path):
    """
        将图片转为base64编码
        :param file_path: 图片文件路径
        :return: 图片的base64编码字符串
    """
    f = open(file_path, 'rb')
    image = f.read()
    # 注意要把编码后的“+”替换成“%2b”，否则图片会不显示
    image_base64 = str(base64.b64encode(image), encoding='utf-8').replace("+", "%2b")
    return image_base64


def cropPicture(image_open_path, image_save_path, start_x, start_y, end_x, end_y):
    """
        裁剪图片\n
        :param image_open_path: 待裁剪的图片路径
        :param image_save_path: 裁剪后保存图片的路径
        :param start_x: 裁剪的起点x坐标
        :param start_y: 裁剪的起点y坐标
        :param end_x: 裁剪的终点x坐标
        :param end_y: 裁剪的终点y坐标
        :return: 裁剪后图片的路径
    """
    # 打开并裁剪图片
    image = Image.open(image_open_path)
    image_width, image_height = image.size
    start_x, start_y, end_x, end_y = check2RightCropRange(start_x, start_y, end_x, end_y, image_width, image_height)
    region = image.crop((start_x, start_y, end_x, end_y))
    # 保存图片
    region.save(image_save_path)
    return image_save_path


def check2RightCropRange(start_x, start_y, end_x, end_y, image_width, image_height):
    """
        校验裁剪区域的坐标的合法性，将非法的坐标转换为合法的坐标\n
        Crop函数要求坐标从左上到右下来指定裁剪区域，即保证star_x < end_x, start_y < end_y\n
        要求裁剪的像素大小不小于1，否则无意义\n
        :param start_x: 裁剪的起点x坐标
        :param start_y: 裁剪的起点y坐标
        :param end_x: 裁剪的终点x坐标
        :param end_y: 裁剪的终点y坐标
        :param image_width: 图片的宽度
        :param image_height: 图片的高度
        :return: 合法的裁剪区域坐标
    """
    start_x, end_x = _check2LeftLessRight(start_x, end_x)
    start_y, end_y = _check2LeftLessRight(start_y, end_y)
    start_x = _check2LimitRange(start_x, 0, image_width)
    start_y = _check2LimitRange(start_y, 0, image_height)
    end_x = _check2LimitRange(end_x, 0, image_width)
    end_y = _check2LimitRange(end_y, 0, image_height)
    return start_x, start_y, end_x, end_y


if __name__ == '__main__':
    """ 
        用于临时测试模块方法的主函数，方法内容可忽略
        当 Run 当前模块 时，当前模块的 __name__ = __main__
        当 Run 其他模块 时，当前模块的 __name__ = __file_name__ (py文件名)
    """
    pass
