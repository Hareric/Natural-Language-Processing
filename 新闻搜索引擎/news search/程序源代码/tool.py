# coding=utf-8
import sys
import time
__author__ = ['david', 'Eric Chan']


def get_file_lines(path):
    """读取文件中所有的函数

    :param
        path：文件路径
    :return
        lines：包含文本内容的数组
    """
    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    f.close()
    return lines


def write_file(path, lines, flag):
    """

    :param
        path：写入的文件路径
        lines：写入的文件内容
    :return:
        True：操作成功
    """
    f = open(path, flag)
    for line in lines:
        f.write(line.encode('utf-8') + "\n")
    f.flush()
    f.close()
    return True


def get_freq_dic(path):
    freq_dic = {}

    for line in get_file_lines(path):
        line = line.decode("utf-8")
        temp = line.split("\t")
        freq_dic[temp[0]] = int(temp[1])

    return freq_dic


def get_flag_dic(path):
    word_flag_dic = {}
    for line in get_file_lines(path):
        line = line.decode("gbk")
        temp = line.split(",")
        word_flag_dic[temp[0]] = temp[1:]
    return word_flag_dic


def long_to_int(value):
    """ 将long类型转换为int类型，超出最大值部分只能划除

    :param value:
    :return:
    """
    assert isinstance(value, (int, long))
    return int(value & sys.maxint)


def exe_time(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        sys.stdout.write('\033[0;32;0m')
        print "-----------------------------------"
        print "%s,function \033[4;32;0m%s()\033[0m\033[0;32;0m start" \
              % (time.strftime("%X", time.localtime()), func.__name__)
        sys.stdout.write('\033[0m')
        res = func(*args, **kwargs)
        sys.stdout.write('\033[0;32;0m')
        print "%s,function \033[4;32;0m%s()\033[0m\033[0;32;0m end" \
              % (time.strftime("%X", time.localtime()), func.__name__)
        print "%.3fs taken for function \033[4;32;0m%s()\033[0m\033[0;32;0m" \
              % (time.time() - t0, func.__name__)
        print "-----------------------------------"
        sys.stdout.write('\033[0m')
        return res
    return wrapper
