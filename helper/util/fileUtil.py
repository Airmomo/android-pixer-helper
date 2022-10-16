import os
import re

# 打开文件的模式
OPEN_ONLY_READ_ERROR = 'r'           # 只能读，文件不存在则报错
OPEN_ONLY_WRITE_CREATE_COVER = 'w'   # 只能写，文件不存在则创建，写入时覆盖文本内容
OPEN_ONLY_WRITE_CREATE_APPEND = 'a'  # 只能写，文件不存在则创建，写入时追加文本内容
OPEN_READ_WRITE_ERROR_COVER = 'r+'    # 可读可写，文件不存在则报错，写入时覆盖文本内容
OPEN_READ_WRITE_CREATE_COVER = 'w+'   # 可读可写，文件不存在则创建，写入时覆盖文本内容
OPEN_READ_WRITE_CREATE_APPEND = 'a+'  # 可读可写，文件不存在则创建，写入时追加文本内容
# 文件的读入方式
READ_ALL_AS_STR = "read"        # 一次性读取文本中全部的内容，以字符串的形式返回结果
READ_FIRST_AS_STR = "readline"  # 只读取文本第一行的内容，以字符串的形式返回结果
READ_ALL_AS_LIST = "readlines"  # 读取文本每一行的内容，并且以列表的格式返回结果
# 文件的写入方式
WRITE_NEWLINE = '\n'        # 写入后换行
WRITE_WIN_NEWLINE = '\r\n'  # 写入后换行（windows的换行符）
WRITE_NOT_NEWLINE = ''      # 默认写入后不换行


def isDirExistAndCreate(dir_path, is_create=False):
    """
        判断目录是否存在，选择性创建\n
        :param dir_path: 目录路径
        :param is_create: 是否创建目录
    """
    if is_create and not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return os.path.exists(dir_path)


def isFileFatherDirExistAndCreate(file_path, is_create_dir=False):
    """
        判断文件的父级目录是否存在，选择性创建文件目录\n
        :param file_path: 文件路径
        :param is_create_dir: 是否创建文件目录
    """
    match_res = re.search(r'/(\w+)\.(\w+)', file_path)
    file_name = match_res.group(1) + "." + match_res.group(2)
    directory = file_path.replace(file_name, "")
    if is_create_dir:
        isDirExistAndCreate(directory, is_create=is_create_dir)
    return os.path.exists(directory)


def _clearLineChar(line_text):
    """
        去除字符串或字符串列表中所有的换行符\n
        :param line_text: 字符串或字符串列表
        :return: 无换行符的字符串或字符串列表
    """
    if not line_text:
        return None
    if isinstance(line_text, list):
        res = []
        for text in line_text:
            text = text.replace('\n', '').replace('\r\n', '')
            res.append(text)
        return res
    return line_text.replace('\n', '').replace('\r\n', '')


def readTxtFile(file_path, file_read_mode, line_index=None):
    """
        读取文本文件\n
        :param file_path: 文件路径
        :param file_read_mode: 文件的读取方式
        :param line_index: 行下标从0开始，读取指定行的内容，若不设置则读取全部行并封装为列表，只在READ_ALL_AS_LIST模式下生效
        :return: 读取的结果，读取失败返回None
    """
    res = None
    if isFileFatherDirExistAndCreate(file_path, False):
        try:
            fd = open(file_path, 'r')
        except OSError:
            return None
        else:
            if file_read_mode == READ_ALL_AS_STR:
                res = fd.read()
            elif file_read_mode == READ_FIRST_AS_STR or line_index == 0:
                # 注意如果是读取第一行，即line_index=0的情况下，必须使用readline才能读取到第一行的内容
                res = fd.readline()
            elif file_read_mode == READ_ALL_AS_LIST:
                res = fd.readlines()
            fd.close()
    if res and line_index:
        if line_index >= len(res):
            return None
        return _clearLineChar(res[line_index])
    return _clearLineChar(res)


def writeTxtFile(file_path, file_open_mode, write_text, file_write_mode=WRITE_NOT_NEWLINE):
    """
        写入文本文件并保存\n
        :param file_path: 文件路径
        :param file_open_mode: 文件的打开方式
        :param file_write_mode: 文件的写入方式
        :param write_text: 待写入的文本数组
        :return: 写入成功的行数
    """
    save_res = 0
    if isFileFatherDirExistAndCreate(file_path, True):
        fd = open(file_path, file_open_mode)
        if isinstance(write_text, list):
            for text in write_text:
                save_res += fd.write(text + file_write_mode)
        else:
            save_res += fd.write(write_text + file_write_mode)
        fd.close()
    return save_res


def deleteItemAtFile(file_path, item_text):
    """
        删除文件中的指定数据行\n
        :param file_path: 文件路径
        :param item_text: 行的数据
        :return:
    """
    item_list = readTxtFile(file_path, READ_ALL_AS_LIST)
    res = 0
    if item_list:
        try:
            item_list.remove(item_text)
        except ValueError:
            return False
        res = writeTxtFile(file_path, OPEN_ONLY_WRITE_CREATE_COVER, item_list, WRITE_NEWLINE)
    return res > 0
