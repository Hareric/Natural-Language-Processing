# coding=utf-8
__author__ = 'karine'
import time


def get_file(file_name, charset='utf-8'):
    f = open(file_name)
    word_dict = {}
    line = f.readline().decode(charset)
    while line:
        word_dict[line.split(',')[0]] = line.split(',')[2].strip('\r\n')
        line = f.readline().decode(charset)
    words_list = word_dict.keys()
    return word_dict, words_list


class Segmentation:
    def __init__(self):
        self.word_dict, self.words_list = get_file('WordFrequency.txt', charset='GBK')
        self.num_word = {}
        self.may_candidate_words = []
        self.candidate_words = []
        self.same_last_word = {}
        self.same_first_word = {}
        self.candidate_dict = {}
        self.left_neighbor = {}
        self.word_freq = {}
        self.sum_freq = {}
        self.best_left = {}

    def get_candidate(self, sentence=u''):

        for i in range(len(sentence)):
            self.num_word[i] = sentence[i]
        word_list = self.num_word.values()
        for j in range(len(word_list)):
            self.may_candidate_words.append(word_list[j])
            for k in range(j + 1, len(word_list)):
                self.may_candidate_words.append(word_list[j] + word_list[k])
                word_list[j] = word_list[j] + word_list[k]
        for word in self.may_candidate_words:
            if word in self.words_list:
                self.candidate_words.append(word)

        for w in self.candidate_words:
            if w in self.words_list:
                self.word_freq[w] = self.word_dict[w]

        l = len(self.candidate_words)
        ls = len(sentence)

        for i in range(l):
            a = self.candidate_words[i][len(self.candidate_words[i]) - 1]
            for j in range(i + 1, l):
                if self.candidate_words[j][len(self.candidate_words[j]) - 1] == a:
                    self.same_last_word[self.candidate_words[j]] = self.candidate_words[i]
                else:
                    break

        for i in range(l):
            a = self.candidate_words[i][0]
            for j in range(i + 1, l):
                if self.candidate_words[j][0] == a:
                    self.same_first_word[self.candidate_words[i]] = self.candidate_words[j]
                else:
                    break

        for i in range(ls)[::-1]:
            lastkey = self.same_last_word.keys()
            firstkey = self.same_first_word.keys()
            list = []
            if sentence[i - 1] in lastkey:
                list.append(sentence[i - 1])
                list.append(self.same_last_word[sentence[i - 1]])
            elif i == 0:
                self.left_neighbor[sentence[i]] = u'none'
            else:
                list.append(sentence[i - 1])
            self.left_neighbor[sentence[i]] = list
            for w in firstkey:
                if w == sentence[i]:
                    self.left_neighbor[self.same_first_word[w]] = list
        return self.left_neighbor, self.word_freq

    def frequency(self):
        l = len(self.candidate_words)
        for i in range(l):
            a = float(self.word_freq[self.candidate_words[i]].strip("%"))
            if len(self.left_neighbor[self.candidate_words[i]]) == 0:
                self.sum_freq[self.candidate_words[i]] = a
                self.best_left[self.candidate_words[i]] = u'none'
            else:
                b = []
                for j in self.left_neighbor[self.candidate_words[i]]:
                    b.append(a * float(self.word_freq[j].strip("%")))
                self.sum_freq[self.candidate_words[i]] = max(b)
                self.best_left[self.candidate_words[i]] = self.left_neighbor[self.candidate_words[i]][b.index(max(b))]
        return self.best_left

    def seg(self):
        l = len(self.candidate_words)
        a = self.candidate_words[l - 1]
        list = []
        while 1:
            if self.best_left[a] == u'none':
                list.append(a)
                break
            else:
                list.append(a)
                a = self.best_left[a]
        return list[::-1]


if __name__ == '__main__':
    t1 = time.time()
    instance = u'结合成分子时'
    S = Segmentation()
    left_neighbor_dict, word_freq = S.get_candidate(instance)
    f = S.frequency()
    s = S.seg()
    t2 = time.time()
    print '|'.join(s)
    print "运行时间%fs" % (t2 - t1)




    # seg = S.segmentation(candidate)
    # for i in seg.keys():
    #     print i, seg[i]
