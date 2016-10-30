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
Author = Eric_Chan
Create_Time = 2016/10/30

说明
使用 HMM算法 对已分好词的列表进行词性标注,并使用viterbi提高算法效率
待修复bug:
  若输入的词语不存在于词库之中 程序将无法正常运行
"""
import numpy as np


def load_file(file_name, charset='utf-8'):
    """
    读取文件，按列返回列表
    :param file_name: 文件路径
    :param charset: 文本内容decode的编码，默认为utf-8
    :return: 文本内容列表
    """
    f1 = open(file_name)
    line = f1.readline().decode(charset).strip()
    line_list = []
    while line:
        line_list.append(line)
        line = f1.readline().decode(charset).strip()
    return line_list


class HMM:
    def __init__(self):
        """
        初始化 HMM词性标注算法
        :return:
        """
        self.cixin_list = load_file('./data/cixin_map.txt')
        self.cixin_map = dict(zip(self.cixin_list, range(self.cixin_list.__len__())))  # 词性映射哈希表
        self.trans_pro_matrix = np.loadtxt('./data/A.txt') # 转移概率矩阵
        vocab_list = load_file('./data/vocab_map.txt')
        self.vocab_map = dict(zip(vocab_list, range(vocab_list.__len__())))  # 词语映射哈希表
        self.emitter_pro_matrix = np.loadtxt('./data/B.txt')  # 发射概率矩阵
        del vocab_list
        print '初始化完毕'

    def hmm(self, sentence_list):
        """
        :param sentence_list: 已分好词的句子列表
        :return: 对应每个词的词性列表
        """
        sentence_list = list(sentence_list)
        sentence_len = sentence_list.__len__()  # 句子长度
        cixin_len = self.cixin_list.__len__()  # 词性个数
        # 概率分布表 .[i, j, 0]表示第i个词为第j个词性的最优概率;.[i, j, 1]表示该最优概率的前一个词的词性索引,若为-1表示该词为第一个词无前词
        pro_table = np.zeros((sentence_len, cixin_len, 2))
        try:
            pro_table[0, :, 0] = self.emitter_pro_matrix[self.vocab_map[sentence_list[0]]]
            pro_table[0, :, 1] = -1
            for i in range(sentence_len)[1:]:
                for j in range(cixin_len):
                    if self.emitter_pro_matrix[self.vocab_map[sentence_list[i]], j] == 0:
                        continue
                    pre_cixin_pro = pro_table[i-1, :, 0]
                    pre_cixin_pro *= self.trans_pro_matrix[j]
                    pre_cixin_pro *= self.emitter_pro_matrix[self.vocab_map[sentence_list[i]], j]
                    pro_table[i, j, 0] = np.max(pre_cixin_pro)
                    pro_table[i, j, 1] = np.where(pre_cixin_pro == np.max(pre_cixin_pro))[0][0]
            result_cixin_map = []
            sy = int(np.where(pro_table[-1, :, 0] == np.max(pro_table[-1, :, 0]))[0][0])
            t = -1
        except KeyError:
            return "无法正常运行 有词语不存在词库之中"
        while sy != -1:
            result_cixin_map.append(sy)
            sy = int(pro_table[t, sy, 1])
            t -= 1
        result_cixin = []

        for s in result_cixin_map[::-1]:
            result_cixin.append(self.cixin_list[s])
        return result_cixin


if __name__ == '__main__':
    H = HMM()
    import time
    t1 = time.time()
    print H.hmm([u'结合', u'成', u'分子', u'时'])
    t2 = time.time()
