# coding=utf-8
import re
import time

from Search import Search

if __name__ == '__main__':
    t1 = time.time()
    sea = Search()
    t2 = time.time()
    print "搜索引擎初始化完毕", t2 - t1
    queries = u'site:(站内搜索) 全部搜索 "完整搜索" (包含搜索) -(排除搜索)'

    '''site:(sohu.com) "罗一笑" (苹果) -(深圳)'''

    while queries:
        queries = raw_input().decode('utf-8')
        try:
            site_search_url = re.findall('site:\((.*?)\)', queries)[0]
            queries = queries.replace(unicode('site:(%s)' % site_search_url), '')
        except IndexError:
            site_search_url = None
        try:
            except_search_query = re.findall('-\((.*?)\)', queries)[0]
            queries = queries.replace(unicode('-(%s)' % except_search_query), '')
        except IndexError:
            except_search_query = None
        try:
            include_search_query = re.findall('\((.*?)\)', queries)[0]
            queries = queries.replace(unicode('(%s)' % include_search_query), '')
        except IndexError:
            include_search_query = None
        try:
            complete_search_query = re.findall('"(.*?)"', queries)[0]
            queries = queries.replace(unicode('"%s"' % complete_search_query), '')
        except IndexError:
            complete_search_query = None
        all_search_query = queries.strip()
        if all_search_query == '':
            all_search_query = None

        # 包含任一关键词检索
        if include_search_query is not None:
            candidate_0 = sea.include_search(include_search_query)
        else:
            candidate_0 = None
        # 包含全部关键词检索
        if all_search_query is not None:
            candidate_1 = sea.all_search(all_search_query)
        else:
            candidate_1 = None
        # 包含完整关键词检索
        if complete_search_query is not None:
            candidate_2 = sea.complete_search(complete_search_query)
        else:
            candidate_2 = None
        # 将以上的检索结果交集并集处理
        candidate = Search.union_dict(candidate_0, Search.inter_dict(candidate_1, candidate_2))

        # 站内搜索
        if site_search_url is not None:
            candidate = sea.site_search(site_search_url, candidate)

        # 排除关键词搜索
        if except_search_query is not None:
            candidate = sea.except_search(except_search_query, candidate)

        # 按照类型检索 ['军事', '体育', '科技', '娱乐', '社会', '国际', '国内', '数码']
        # candidate = sea.type_search([1,2,3,4,5], candidate)

        # 根据tf-idf排序
        doc_list = Search.rank(candidate)
        result = ""
        for temp in doc_list:
            result = result + sea.doc_dic[temp[0]].split("##")[0].decode("utf-8") + '|' + \
                     sea.doc_dic[temp[0]].split("##")[2].decode("utf-8") + '|' + sea.doc_dic[temp[0]].split("##")[
                         3].decode("utf-8") + "\n" + sea.doc_dic[temp[0]].split("##")[1].decode("utf-8") + "\n"
        print result
        queries = '非空字符串'
