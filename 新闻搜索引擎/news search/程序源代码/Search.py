# coding=utf-8
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#               佛祖保佑         永无BUG
"""
Author = Eric Chan
Create_Time = 2016/01/02
根据倒排索引词典 进行检索
"""
from Inverted_index import InvertDic
import math
import re
from doc_proccess import Doc


class Search(InvertDic):
    def __init__(self):
        InvertDic.__init__(self)

    def include_search(self, queries):
        """
        包含任一关键词检索方式
        :param queries: 检索语句
        :return:
        """
        if not isinstance(queries, unicode):
            queries = queries.decode('utf8')
        else:
            queries = queries
        queries = Doc.split_queries(queries)
        # 仅保留在词库中的词语
        queries = filter(lambda q: q in self.word_index_dic, queries)
        candidate = {}
        for query in queries:
            word_id = self.word_index_dic[query]
            for term in self.word_term_dic[word_id]:
                candidate[term.doc_id] = candidate.get(term.doc_id, 0) + self.calculate_weight(term)
        return candidate

    def all_search(self, queries):
        """
        包含全部关键词检索方式
        :param queries: 检索语句
        :return:
        """
        if not isinstance(queries, unicode):
            queries = queries.decode('utf8')
        else:
            queries = queries
        queries = Doc.split_queries(queries)
        queries = filter(lambda q: q in self.word_index_dic, queries)
        candidate = {}
        word_id = self.word_index_dic[queries[0]]
        for term in self.word_term_dic[word_id]:
            candidate[term.doc_id] = self.calculate_weight(term)
        candidate_b = {}
        for query in queries[1:]:
            word_id = self.word_index_dic[query]
            for term in self.word_term_dic[word_id]:
                candidate_b[term.doc_id] = self.calculate_weight(term)
            keys = [x for x in candidate if x in candidate_b]  # 每个关键词的查询结果取交集
            candidate = dict(zip(keys, [candidate[x] + candidate_b[x] for x in keys]))
            candidate_b.clear()
        return candidate

    def complete_search(self, queries):
        """
        包含完整关键词检索方式(关键词之间不能分开)
        :param queries: 检索语句
        :return:
        """
        if not isinstance(queries, unicode):
            queries = queries.decode('utf8')
        else:
            queries = queries
        queries = Doc.split_queries(queries)
        queries = filter(lambda q: q in self.word_index_dic, queries)
        candidate = {}
        word_id = self.word_index_dic[queries[0]]
        for term in self.word_term_dic[word_id]:
            candidate[term.doc_id] = [self.calculate_weight(term), term.location_ids]
        for query in queries[1:]:
            word_id = self.word_index_dic[query]
            doc_ids = [term.doc_id for term in self.word_term_dic[word_id]]
            for k in candidate.keys():
                if k not in doc_ids:
                    candidate.pop(k)
            for term in self.word_term_dic[word_id]:
                if term.doc_id not in candidate.keys():
                    continue
                pre_location = candidate[term.doc_id][1][:]
                pre_location = [i + 1 for i in pre_location]
                cur_location = term.location_ids[:]
                l = (set(pre_location) & set(cur_location)).__len__()
                if l > 0:
                    candidate[term.doc_id][0] += self.calculate_weight(term)
                    candidate[term.doc_id][1] = term.location_ids[:]
                else:
                    candidate.pop(term.doc_id)
        for k in candidate.keys():
            candidate[k] = candidate[k][0]
        return candidate

    def except_search(self, queries, candidate):
        """
        不包含关键词的检索
        :param queries: 检索语句
        :param candidate: 基于原搜索所得的候选集
        :return: 新的候选集
        """
        if not isinstance(queries, unicode):
            queries = queries.decode('utf8')
        else:
            queries = queries
        queries = Doc.split_queries(queries)
        queries = filter(lambda q: q in self.word_index_dic, queries)
        except_news_ids = set()
        for query in queries:
            word_id = self.word_index_dic[query]
            for term in self.word_term_dic[word_id]:
                except_news_ids.add(term.doc_id)
        for k in candidate.keys():
            if k in except_news_ids:
                candidate.pop(k)
        return candidate

    def type_search(self, type_sy_list, candidate):
        """
        指定类别检索
        :param type_sy_list: 类别对应的sy列表
        :param candidate: 基于原搜索所得的候选集
        :return: 新的候选集
        """
        type_list = ['军事', '体育', '科技', '娱乐', '社会', '国际', '国内', '数码']
        type_list = [type_list[i] for i in type_sy_list]
        for doc_id in candidate.keys():
            if self.doc_dic[doc_id].split("##")[2] not in type_list:
                candidate.pop(doc_id)
        return candidate

    def site_search(self, limit_url, candidate):
        """
        站内搜索---限定要搜索指定的网站
        :param limit_url: 限定的网址
        :param candidate: 基于原搜索所得的候选集
        :return: 新的候选集
        """
        for doc_id in candidate.keys():
            url = self.doc_dic[doc_id].split("##")[3]
            find_result = re.findall(limit_url, url)
            if find_result.__len__() == 0:
                candidate.pop(doc_id)
        return candidate

    def calculate_weight(self, term):
        """
        计算特定单词在特定文档的tf-idf值
        :param term: Term类
        :return:
        """
        return float(term.tf + 1) / (self.word_freq_dic[term.word_id] + 1) * \
               math.log(self.doc_len + 1 / self.word_df_dic[term.word_id], 2)

    @staticmethod
    def rank(candidate):
        """ 根据文章权重进行倒序排序

        :param candidate: 词典，eq.{文章编号:文章权重}
        :return:
        """
        candidate_list = sorted(candidate.items(), key=lambda x: x[1], reverse=True)
        return candidate_list

    @staticmethod
    def inter_dict(dict_a, dict_b):
        """
        根据key值 取2个字典的交集 保留较大的value
        :param dict_a:
        :param dict_b:
        :return: 合并后的字典
        """
        if dict_a is None:
            return dict_b
        if dict_b is None:
            return dict_a
        keys = [k for k in dict_a if k in dict_b]
        new_dict = dict(zip(keys, [dict_a[x] if dict_a[x] > dict_b[x] else dict_b[x] for x in keys]))
        return new_dict

    @staticmethod
    def union_dict(dict_a, dict_b):
        """
        2个字典取并集 优先保留dict_b 的value
        :param dict_a:
        :param dict_b:
        :return:
        """
        if dict_a is None:
            return dict_b
        if dict_b is None:
            return dict_a
        return dict(dict_a, **dict_b)