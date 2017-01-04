# coding=utf-8
import re
import sys
import time

from PyQt4 import QtCore, QtGui, uic

import news_search

qtCreatorFile = "./ui/mainwindow.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.sea = news_search.Search()
        self.setupUi(self)
        self.model = None
        self.SearchButton.clicked.connect(self.get_result)
        self.CheckBox = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5,
                         self.checkBox_6, self.checkBox_6, self.checkBox_8, self.checkBox_9]
        self.setWindowTitle(QtCore.QString(u"Darlin 陈文达 吴嘉琳 翁靖达"))

    def get_result(self):
        # queries = raw_input().decode('utf-8')
        queries = unicode(self.textInput.toPlainText())
        self.model = QtGui.QStandardItemModel(self.listView)
        t1 = time.time()

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
            candidate_0 = self.sea.include_search(include_search_query)
        else:
            candidate_0 = None
        # 包含全部关键词检索
        if all_search_query is not None:
            candidate_1 = self.sea.all_search(all_search_query)
        else:
            candidate_1 = None
        # 包含完整关键词检索
        if complete_search_query is not None:
            candidate_2 = self.sea.complete_search(complete_search_query)
        else:
            candidate_2 = None
        # 将以上的检索结果交集并集处理
        candidate = news_search.Search.union_dict(candidate_0, news_search.Search.inter_dict(candidate_1, candidate_2))

        # 站内搜索
        if site_search_url is not None:
            candidate = self.sea.site_search(site_search_url, candidate)

        # 排除关键词搜索
        if except_search_query is not None:
            candidate = self.sea.except_search(except_search_query, candidate)

        # 按照类型检索 ['军事', '体育', '科技', '娱乐', '社会', '国际', '国内', '数码']
        selected_type = self.get_selected_type()
        candidate = self.sea.type_search(selected_type, candidate)

        # 根据tf-idf排序
        doc_list = news_search.Search.rank(candidate)

        for temp in doc_list[:200]:
            item = QtGui.QStandardItem(self.sea.doc_dic[temp[0]].split("##")[0].decode("utf-8") + '|' + \
                                       self.sea.doc_dic[temp[0]].split("##")[2].decode("utf-8") + '|' + \
                                       self.sea.doc_dic[temp[0]].split("##")[
                                           3].decode("utf-8") + "\n" + self.sea.doc_dic[temp[0]].split("##")[
                                           1].decode("utf-8").replace(
                self.sea.doc_dic[temp[0]].split("##")[0].decode("utf-8"), '') + "\n")

            item.setCheckable(False)
            self.model.appendRow(item)

        self.listView.setModel(self.model)

        t2 = time.time()
        self.lineTime.setText("%f" % (t2 - t1) + "s")

    def get_selected_type(self):
        """ 获取用户搜索时选择的类别

        :return:
        """
        selected_type = []
        for index in range(len(self.CheckBox) - 1):
            if self.CheckBox[index].isChecked():
                selected_type.append(index)
            if self.CheckBox[-1].isChecked():
                selected_type = [0, 1, 2, 3, 4, 5, 6, 7]
        return selected_type

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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
