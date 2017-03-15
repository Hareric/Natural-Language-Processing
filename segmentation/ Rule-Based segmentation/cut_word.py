# coding=utf-8
#        ┏┓　　　┏┓+ +
# 　　　┏┛┻━━━┛┻┓ + +
# 　　　┃　　　　　　 ┃ 　
# 　　　┃　　　━　　　┃ ++ + + +
# 　　 ████━████ ┃+
# 　　　┃　　　　　　 ┃ +
# 　　　┃　　　┻　　　┃
# 　　　┃　　　　　　 ┃ + +
# 　　　┗━┓　　　┏━┛
# 　　　　　┃　　　┃　　　　　　　　　　　
# 　　　　　┃　　　┃ + + + +
# 　　　　　┃　　　┃　　　　Codes are far away from bugs with the animal protecting　　　
# 　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug　　
# 　　　　　┃　　　┃
# 　　　　　┃　　　┃　　+　　　　　　　　　
# 　　　　　┃　 　　┗━━━┓ + +
# 　　　　　┃ 　　　　　　　┣┓
# 　　　　　┃ 　　　　　　　┏┛
# 　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　┃┫┫　┃┫┫
# 　　　　　　┗┻┛　┗┻┛+ + + +
"""
Author = Eric Chan
Create_Time = 2016/10/07
中文分词,使用算法为
正向最大匹配法(Maximum Matching Method, 简称MM算法)
逆向最大匹配算法(Reverse Maximum Matching Method, 简称RMM算法)
"""


def load_file(file_name, charset='utf-8'):
    """
    读取文件，按列返回列表
    :param file_name: 文件路径
    :param charset: 文本内容decode的编码，默认为utf-8
    :return: 文本内容列表
    """
    f1 = open(file_name)
    line = f1.readline().decode(charset).split(',')[0]
    line_list = []
    while line:
        line_list.append(line)
        line = f1.readline().decode(charset).split(',')[0]
    return line_list


class CutWord:
    word_set = None

    def __init__(self):
        self.word_set = set(load_file('./data/ChineseDic.txt', charset='GBK'))

    def mm_cut(self, sentence=u'', max_len=6):
        """
        使用正向最大匹配法划分词语
        :param sentence: str 待划分句子
        :param max_len: int 最大词长 默认为6
        :return: str-list 已分词的字符串列表
        """
        sentence = sentence
        cur = 0  # 表示分词的位置
        sen_len = sentence.__len__()  # 句子的长度
        word_list = []  # 划分的结果
        while cur < sen_len:
            l = None
            for l in range(max_len, 0, -1):
                if sentence[cur: cur+l] in self.word_set:
                    break
            word_list.append(sentence[cur: cur+l])
            cur += l
        return word_list

    def rmm_cut(self, sentence=u'', max_len=6):
        """
        使用逆向最大匹配法划分词语
        :param sentence: str 待划分句子
        :param max_len: int 最大词长 默认为6
        :return: str-list 已分词的字符串列表
        """
        sentence = sentence
        sen_len = sentence.__len__()  # 句子的长度
        cur = sen_len  # 表示分词的位置
        word_list = []  # 划分的结果
        while cur > 0:
            l = None
            if max_len > cur:
                max_len = cur
            for l in range(max_len, 0, -1):
                if sentence[cur-l: cur] in self.word_set:
                    break
            word_list.insert(0, sentence[cur-l: cur])
            cur -= l
        return word_list

if __name__ == '__main__':
    import time
    sen = u'我爱吃大白菜'
    CW = CutWord()

    print "mm"
    t1 = time.time()
    r = CW.mm_cut(sen)
    t2 = time.time()
    print '|'.join(r)
    print "运行时间%fs" % (t2 - t1)
    print '-------------------------------------'

    print "rmm"
    t1 = time.time()
    r = CW.rmm_cut(sen)
    t2 = time.time()
    print '|'.join(r)
    print "运行时间%fs" % (t2 - t1)
