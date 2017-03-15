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
Create_Time = 2017/03/15
中文分词,使用算法为
正向最大匹配法(Maximum Matching Method, 简称MM算法)
逆向最大匹配算法(Reverse Maximum Matching Method, 简称RMM算法)
最大概率分词算法
"""
import collections


class Segmentation:
    def __init__(self):
        self.word_set = set(Segmentation.init_word_list('./data/ChineseDic.txt', charset='GBK'))
        self.word_frequency_dict = Segmentation.init_frequency_dict('./data/WordFrequency.txt', charset='GBK')
        self.sentence = ''  # 待划分句子
        self.seg_result_dict = {}  # 划分结果

    def set_sentence(self, sentence):
        if not isinstance(sentence, unicode):
            self.sentence = sentence.decode('utf8')
        else:
            self.sentence = sentence
        self.seg_result_dict = {}  # 初始化划分结果

    def get_result_dict(self):
        """
        获得分词结果字典
        :return:
        """
        return self.seg_result_dict

    def print_result(self):
        """
        输出分词结果
        :return:
        """
        print "\033[0;32;m分词算法  分词结果\033[0m"
        for k, v in self.seg_result_dict.iteritems():
            print '%6s:' % k, '|'.join(v)

    def mm_seg(self, max_len=6):
        """
        使用正向最大匹配法划分词语
        :param max_len: int 最大词长 默认为6
        """
        cur = 0  # 表示分词的位置
        seg_result = []
        sen_len = self.sentence.__len__()  # 句子的长度
        while cur < sen_len:
            l = None
            for l in range(max_len, 0, -1):
                if self.sentence[cur: cur + l] in self.word_set:
                    break
            seg_result.append(self.sentence[cur: cur + l])
            cur += l
        self.seg_result_dict['MM'] = seg_result

    def rmm_seg(self, max_len=6):
        """
        使用逆向最大匹配法划分词语
        :param max_len: int 最大词长 默认为6
        """
        sen_len = self.sentence.__len__()  # 句子的长度
        seg_result = []
        cur = sen_len  # 表示分词的位置
        while cur > 0:
            l = None
            if max_len > cur:
                max_len = cur
            for l in range(max_len, 0, -1):
                if self.sentence[cur - l: cur] in self.word_set:
                    break
            seg_result.insert(0, self.sentence[cur - l: cur])
            cur -= l
        self.seg_result_dict['RMM'] = seg_result

    def max_probability_seg(self):
        """
        使用概率最大分词算法进行分词
        """
        l = len(self.sentence)
        p = [0] * (l + 1)
        p[l] = 1
        div = [1] * (l + 1)
        t = [1] * l
        for i in range(l - 1, -1, -1):
            for k in range(1, l - i + 1):
                tmp = self.word_frequency_dict[self.sentence[i:i + k]]
                if k > 1 and tmp == 1:
                    continue
                if self.word_frequency_dict[self.sentence[i:i + k]] * p[i + k] * div[i] > p[i] * \
                        self.word_frequency_dict['_t_'] * div[i + k]:
                    p[i] = self.word_frequency_dict[self.sentence[i:i + k]] * p[i + k]
                    div[i] = self.word_frequency_dict['_t_'] * div[i + k]
                    t[i] = k
        i = 0
        seg_result = []
        while i < l:
            seg_result.append(self.sentence[i:i + t[i]])
            i += t[i]
        self.seg_result_dict['MP'] = seg_result

    @staticmethod
    def init_word_list(file_name, charset='utf-8'):
        """
        读取词库txt, 返回词库列表
        :param file_name: 文件路径
        :param charset: 文本内容decode的编码，默认为utf-8
        :return: 词库列表
        """
        f1 = open(file_name)
        lines = f1.readlines()
        f1.close()
        word_list = []
        for line in lines:
            word_list.append(line.decode(charset).split(',')[0])
        return word_list

    @staticmethod
    def init_frequency_dict(file_name, charset='utf-8'):
        """
        读取词库频率txt, 返回词-频率字典
        :param file_name: 文件路径
        :param charset: 文本内容decode的编码，默认为utf-8
        :return: 词-频率字典
        """
        word_frequency_dict = collections.defaultdict(lambda: 1)
        f = open(file_name, 'r')
        total = 0
        while True:
            line = f.readline()
            if not line:
                break
            word = line.split(',')[0]
            freq = line.split(',')[2].strip('%\r\n')
            total += float(freq) + 1  # smooth
            try:
                word_frequency_dict[word.decode(charset)] = float(freq) + 1
            except UnicodeDecodeError:
                word_frequency_dict[word] = float(freq) + 1
        f.close()
        word_frequency_dict['_t_'] = total
        return word_frequency_dict

if __name__ == '__main__':

    sen = '在这一年中，中国的改革开放和现代化建设继续向前迈进。国民经济增长保持了“高增长、低通胀”的良好发展态势。农业生产再次画获得好的收成，企业改革继续深化，人民生活进一步改善。对外经济技术合作与交流不断扩大。'
    seg = Segmentation()
    seg.set_sentence(sen)
    seg.mm_seg()  # MM
    seg.rmm_seg()  # RMM
    seg.max_probability_seg()  # 最大概率分词
    # r = seg.get_result_dict()  # 获得分词结果字典
    # print '|'.join(r['MM'])
    # print '|'.join(r['RMM'])
    # print '|'.join(r['MP'])
    seg.print_result()  # 将分词结果输出
