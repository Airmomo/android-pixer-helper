class ImageNoneError(Exception):
    def __init__(self):
        super().__init__("图片不存在，OpenCV加载的图片不能为空")


class ThresholdOutRangeError(Exception):
    def __init__(self):
        super().__init__("阈值错误，相似度阈值-取值范围：0～1.0")
