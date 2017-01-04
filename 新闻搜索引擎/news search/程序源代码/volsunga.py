# coding=utf-8
import segmentation
import tool

__author__ = 'david'


class Volsunga:
    """

    """

    def __init__(self, word_flag_freq, flag_freq, flag_relation_freq, word_flag):
        self.word_flag_freq_dic = word_flag_freq
        self.flag_freq_dic = flag_freq
        self.flag_relation_freq_dic = flag_relation_freq
        self.word_flag_dic = word_flag

    def flag_detection(self, words):
        """ 词性识别

        :param words:
        :return:
        """
        best_combination = [self.get_best_flag(words[0], self.word_flag_dic.get(words[0], ["n"]), None)]

        for index in range(1, len(words)):
            candidate = self.word_flag_dic.get(words[index], ["n"])
            best_combination.append(self.get_best_flag(words[index], candidate, words[index - 1]))
        # return self.get_string(best_combination, words)
        return best_combination

    def get_best_flag(self, word, candidate_flag, last_flag):
        """ 从候选词性中选择最适合的词性

        :param word:
        :param candidate_flag:
        :param last_flag:
        :return:
        """
        probability = -1
        result = ""
        for candidate in candidate_flag:
            temp = self.calculate_probability(word, candidate, last_flag)
            if temp > probability:
                probability = temp
                result = candidate
        return result

    def calculate_probability(self, word, candidate, last_flag=None):
        """ 计算词语在句子中属于某个特定词汇的概率

        :param word:
        :param candidate:
        :param last_flag:
        :return:
        """
        word_flag_freq = self.word_flag_freq_dic.get(word + "/" + candidate, 1)
        flag_freq = self.flag_freq_dic.get(candidate, self.flag_freq_dic["n"])
        if last_flag is not None:
            flag_relation_freq = self.flag_relation_freq_dic.get(last_flag + "/" + candidate, 1)
            last_flag_freq = self.flag_freq_dic.get(last_flag, self.flag_freq_dic["n"])
            probability = word_flag_freq / flag_freq * flag_relation_freq / last_flag_freq
        else:
            probability = word_flag_freq / flag_freq
        return probability

    @staticmethod
    def get_string(best_combination, words):
        """ 将结果转换成字符串输出

        :param best_combination:
        :param words:
        :return:
        """
        line = ""
        for index in range(len(words)):
            line = line + words[index] + "/" + best_combination[index] + "\t"
        return line


if __name__ == '__main__':
    word_flag_freq_dic = tool.get_freq_dic("./data/word_flag_freq_dic.txt")
    flag_freq_dic = tool.get_freq_dic("./data/flag_freq_dic.txt")
    flag_relation_freq_dic = tool.get_freq_dic("./data/flag_relation_freq_dic.txt")
    word_flag_dic = tool.get_flag_dic("./data/chineseDic.txt")
    v = Volsunga(word_flag_freq_dic, flag_freq_dic, flag_relation_freq_dic, word_flag_dic)

    content = "在这一年中，中国的改革开放和现代化建设继续向前迈进。国民经济保持了“高增长、低通胀”" \
              "的良好发展态势。农业生产再次获得好的收成，企业改革继续深化，人民生活进一步改善。对外" \
              "经济技术合作与交流不断扩大"
    s = segmentation.Segmentation()
    words = s.seg(content)
    print v.flag_detection(words)
