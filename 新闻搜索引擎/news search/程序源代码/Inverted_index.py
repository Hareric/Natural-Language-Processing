# coding=utf-8

import doc_proccess
import tool
from doc_proccess import Doc
__author__ = 'david'


class Term:
    """ 倒排索引条目，每个实体保留一个单词在一篇文档的信息

    如果单词在文档中出现过，创建Term类保留信息

            文章1     文章2     文章3
    单词1   Term
    单词2             Term
    单词3                       Term


    """
    def __init__(self, word_id, doc_id, tf):
        """

        :param word_id: 单词编号
        :param doc_id: 文档标号
        :param tf: 单词在文档中出现的次数
        :attribute location_ids: 数组，表示词在文章中出现的下标，ex.[1,3,7]
        """
        self.word_id = word_id
        self.doc_id = doc_id
        self.tf = tf
        self.location_ids = []

    def append_location(self, ids):
        """ 添加单词在文档中出现的位置信息

        :param ids:
        :return:
        """
        self.location_ids += ids

    def __str__(self):
        return str(self.word_id) + "@@@@" + str(self.doc_id) + "@@@@" + str(self.tf) + "@@@@" \
               + "##".join([str(x) for x in self.location_ids])


class InvertDic:
    """ 倒排索引词典

    """
    def __init__(self):
        """

        :attribute word_index_dic: 词典，记录单词编号，eq.{单词:单词编号}
        :attribute word_freq_dic: 词典，记录单词总词频，eq.{单词编号:单词总词频}
        :attribute word_term_dic: 词典，存储倒排索引条目信息，eq.{单词编号:[Term1，Term2]}
                                  Term类保存了一个单词在一篇文档中的信息
        :attribute word_df_dic: 词典，记录单词的文档频率，eq.{单词编号:单词文档频率}
        :attribute doc_dic: 词典，eq.{文档编号:文档标题##文档正文}
        :attribute doc_len: 整数，表示现有文档数量
        """

        self.word_index_dic = {}
        self.word_freq_dic = {}
        self.word_term_dic = {}
        self.word_df_dic = {}
        self.doc_dic = {}
        self.doc_len = doc_proccess.Doc.get_lasted_doc_id() + 1
        self.init_all_dic()

    def init_all_dic(self):
        self.get_doc_dic()
        self.get_word_df_dic()
        self.get_word_freq_dic()
        self.get_word_index_dic()
        self.get_word_term_dic()

    def save_word_df_dic(self):
        lines = []
        for it in self.word_df_dic.items():
            lines.append(str(it[0]) + "\t" + str(it[1]))
        tool.write_file("./data/word_df_dic.txt", lines, "w")

    def save_word_index_dic(self):
        lines = []
        for it in self.word_index_dic.items():
            lines.append(it[0] + "\t" +
                         str(it[1]))
        tool.write_file("./data/word_index_dic.txt", lines, "w")

    def save_word_freq_dic(self):
        lines = []
        for it in self.word_freq_dic.items():
            lines.append(str(it[0]) + "\t" + str(it[1]))
        tool.write_file("./data/word_freq_dic.txt", lines, "w")

    def save_word_term_dic(self):
        lines = []
        for it in self.word_term_dic.items():
            for t in it[1]:
                lines.append(t.__str__())
        tool.write_file("./data/word_term_dic.txt", lines, "w")

    def get_doc_dic(self):
        lines = tool.get_file_lines("./data/doc.txt")
        for line in lines:
            temp = line.split("@@@@")
            self.doc_dic[int(temp[0])] = temp[1]

    def get_word_df_dic(self):
        lines = tool.get_file_lines("./data/word_df_dic.txt")
        for line in lines:
            temp = line.split("\t")
            self.word_df_dic[int(temp[0])] = int(temp[1])

    def get_word_index_dic(self):
        lines = tool.get_file_lines("./data/word_index_dic.txt")
        for line in lines:
            temp = line.split("\t")
            try:
                self.word_index_dic[temp[0].decode("utf-8")] = int(temp[1])
            except:
                continue

    def get_word_freq_dic(self):
        lines = tool.get_file_lines("./data/word_freq_dic.txt")
        for line in lines:
            temp = line.split("\t")
            self.word_freq_dic[int(temp[0])] = int(temp[1])

    def get_word_term_dic(self):
        lines = tool.get_file_lines("./data/word_term_dic.txt")
        for line in lines:
            temp = line.split("@@@@")
            t = Term(int(temp[0]), int(temp[1]), int(temp[2]))
            t.append_location([int(x) for x in temp[3].split("##")])
            self.word_term_dic[int(temp[0])] = self.word_term_dic.get(int(temp[0]), []) + [t]

    def update_df_dic(self, words):
        """ 更新文档频率

        :param words:
        :return:
        """
        for word in set(words):
            self.word_df_dic[self.word_index_dic[word]] = self.word_df_dic.get(self.word_index_dic[word], 0) + 1

    def update_invert_index(self, doc):
        """ 更新倒排索引词典，可以将新的文章添加到倒排索引词典内

        :param doc: Doc类
        :return:
        """
        word_id = len(self.word_index_dic)
        self.doc_len += 1
        n_set = set()
        for word in doc.words:
            if word not in self.word_index_dic:
                self.word_index_dic[word] = word_id
                self.word_freq_dic[self.word_index_dic[word]] = 1
                word_id += 1
            else:
                self.word_freq_dic[self.word_index_dic[word]] += 1
            if word not in n_set:
                n_set.add(word)
                t = Term(self.word_index_dic[word], doc.doc_id, doc.freq_dic[word])
                t.append_location(doc.location_dic[word])
                self.word_term_dic[self.word_index_dic[word]] = self.word_term_dic.get(self.word_index_dic[word], []) + [t]

        self.update_df_dic(doc.words)
        self.doc_dic[doc.doc_id] = doc.doc_string
        tool.write_file("./data/doc.txt", [doc.__str__()], "a")



if __name__ == '__main__':

    # 初始化词典
    self = InvertDic()
    self.get_doc_dic()

    self.get_word_df_dic()
    self.get_word_freq_dic()
    self.get_word_index_dic()
    self.get_word_term_dic()
    doc_id = Doc.get_lasted_doc_id() + 1
    print self.word_index_dic
    print doc_id
    # 根据搜索结果返回文章编号
    doc_list = InvertDic.rank(self.search("中国"))
    print doc_list
    # 保存更新好的词典
    self.save_word_df_dic()
    self.save_word_freq_dic()
    self.save_word_index_dic()
    self.save_word_term_dic()
