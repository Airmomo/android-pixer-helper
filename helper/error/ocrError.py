class TextNoneError(Exception):
    def __init__(self):
        super().__init__("用于校验识别结果是否准确的字符串不能为空")
