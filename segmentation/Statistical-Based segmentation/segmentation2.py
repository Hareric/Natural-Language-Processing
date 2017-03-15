# coding=utf-8
__author__ = 'kalin'
import collections
import time

d = collections.defaultdict(lambda: 1)


def init(filename='WordFrequency.txt'):
    f = open(filename, 'r')
    total = 0
    while True:
        line = f.readline()
        if not line:
            break
        word = line.split(',')[0]
        freq = line.split(',')[2].strip('%\r\n')
        total += float(freq) + 1  # smooth
        try:
            d[word.decode('gbk')] = float(freq) + 1
        except:
            d[word] = float(freq) + 1
    f.close()
    d['_t_'] = total


def segmentation(s):
    l = len(s)
    p = [0 for i in range(l + 1)]
    p[l] = 1
    div = [1 for i in range(l + 1)]
    t = [1 for i in range(l)]
    for i in range(l - 1, -1, -1):
        for k in range(1, l - i + 1):
            tmp = d[s[i:i + k]]
            if k > 1 and tmp == 1:
                continue
            if d[s[i:i + k]] * p[i + k] * div[i] > p[i] * d['_t_'] * div[i + k]:
                p[i] = d[s[i:i + k]] * p[i + k]
                div[i] = d['_t_'] * div[i + k]
                t[i] = k
    i = 0
    # list = []
    while i < l:
        print s[i:i + t[i]] + '|',
        i = i + t[i]


if __name__ == '__main__':
    t1 = time.time()
    init()
    s = "在这一年中，中国的改革开放和现代化建设继续向前迈进"
    # s = "在这一年中，中国的改革开放和现代化建设继续向前迈进。" \
    #     "国民经济保持了“高增长、低通胀”的良好发展态势。农业生产再次获得好的收成，" \
    #     "企业改革继续深化，人民生活进一步改善。对外经济技术合作与交流不断扩大"
    s = s.decode('utf8')
    segmentation(s)
    t2 = time.time()
    # print '|'.join(s)
    print "运行时间%fs" % (t2 - t1)
