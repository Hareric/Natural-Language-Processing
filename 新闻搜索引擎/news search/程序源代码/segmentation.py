# coding=utf-8
import collections
import time

__author__ = 'karine'


class Segmentation:
    def __init__(self):
        self.d = self.init_dic()

    def seg(self, s):
        if not isinstance(s, unicode):
            s = s.decode('utf8')
        l = len(s)
        p = [0 for i in range(l + 1)]
        p[l] = 1
        div = [1 for i in range(l + 1)]
        t = [1 for i in range(l)]
        for i in range(l - 1, -1, -1):
            for k in range(1, l - i + 1):
                tmp = self.d[s[i:i + k]]
                if k > 1 and tmp == 1:
                    continue
                if self.d[s[i:i + k]] * p[i + k] * div[i] > p[i] * self.d['_t_'] * div[i + k]:
                    p[i] = self.d[s[i:i + k]] * p[i + k]
                    div[i] = self.d['_t_'] * div[i + k]
                    t[i] = k
        i = 0
        list = []
        while i < l:
            list.append(s[i:i + t[i]])
            # print s[i:i+t[i]]+'|'
            i = i + t[i]
        return list

    @staticmethod
    def init_dic(filename='./data/WordFrequency.txt'):
        d = collections.defaultdict(lambda: 1)
        f = open(filename, 'r')
        total = 0
        while True:
            line = f.readline()
            if not line: break
            word = line.split(',')[0]
            freq = line.split(',')[2].strip('%\r\n')
            total += float(freq) + 1  # smooth
            try:
                d[word.decode('gbk')] = float(freq) + 1
            except:
                d[word] = float(freq) + 1
        f.close()
        d['_t_'] = total
        return d


if __name__ == '__main__':
    t1 = time.time()
    content = "在这一年中，中国的改革开放和现代化建设继续向前迈进。国民经济保持了“高增长、低通胀”" \
              "的良好发展态势。农业生产再次获得好的收成，企业改革继续深化，人民生活进一步改善。对外" \
              "经济技术合作与交流不断扩大"
    s = Segmentation()
    l = s.seg(content)
    print '|'.join(l)
