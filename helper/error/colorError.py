class ColorNoneError(Exception):
    def __init__(self):
        super().__init__("找色的字符串不能为空")
