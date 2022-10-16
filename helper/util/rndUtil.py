"""
    随机组合工具类
"""
import random


def getRndLetAndNums(n):
    """
        Returns: 随机数字+字母的字符串
    """
    ret = []
    for i in range(n):
        num = random.randint(0, 9)
        letter_low = chr(random.randint(97, 122))  # 取小写字母
        letter_up = chr(random.randint(65, 90))  # 取大写字母
        s = str(random.choice([num, letter_low, letter_up]))
        ret.append(s)
    return "".join(ret)


def getRndLets(n):
    """
        Returns: 随机字母的字符串
    """
    ret = []
    for i in range(n):
        letter_low = chr(random.randint(97, 122))  # 取小写字母
        letter_up = chr(random.randint(65, 90))  # 取大写字母
        s = str(random.choice([letter_low, letter_up]))
        ret.append(s)
    return "".join(ret)


def getRndNums(n):
    """
        Returns: 随机数字的字符串
    """
    ret = []
    for i in range(n):
        num = random.randint(0, 9)
        s = str(random.choice([num]))
        ret.append(s)
    return "".join(ret)


def getRndLetAndNumsNore(n):
    """
        Returns: 随机不重复数字+字母的字符串
    """
    num = random.sample(range(0, 10), n)
    letter_low = random.sample(range(97, 122), n)  # 取小写字母
    letter_up = random.sample(range(65, 90), n)  # 取大写字母
    ret = []
    for i in range(n):
        s = str(random.choice([num[i], chr(letter_low[i]), chr(letter_up[i])]))
        ret.append(s)
    return "".join(ret)


def getRndLetsNore(n):
    """
        Returns: 随机不重复字母的字符串
    """
    letter_low = random.sample(range(97, 122), n)  # 取小写字母
    letter_up = random.sample(range(65, 90), n)  # 取大写字母
    ret = []
    for i in range(n):
        s = str(random.choice([chr(letter_low[i]), chr(letter_up[i])]))
        ret.append(s)
    return "".join(ret)


def getRndNumsNore(n):
    """
        Returns: 随机不重复数字的字符串
    """
    num = random.sample(range(0, 10), n)
    ret = []
    for i in range(n):
        s = str(num[i])
        ret.append(s)
    return "".join(ret)
