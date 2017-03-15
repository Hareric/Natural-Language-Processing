# coding=utf-8
import sys
from PyQt4 import QtCore, QtGui, uic
import time
import collections

qtCreatorFile = "./ui/mainwindow.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.d = collections.defaultdict(lambda: 1)
        self.dict_init()
        self.gailvButton.clicked.connect(self.gailv)
        self.setWindowTitle(QtCore.QString(u"Darlin 陈文达 吴嘉琳 翁靖达"))

    def dict_init(self, filename='WordFrequency.txt'):
        f = open(filename, 'r')
        total = 0
        while True:
            line = f.readline()
            if not line: break
            word = line.split(',')[0]
            freq = line.split(',')[2].strip('%\r\n')
            total += float(freq) + 1  # smooth
            try:
                self.d[word.decode('gbk')] = float(freq) + 1
            except:
                self.d[word] = float(freq) + 1
        f.close()
        self.d['_t_'] = total

    def gailv(self):
        content = unicode(self.textInput.toPlainText())
        result = self.segmentation(content)
        t1 = time.time()
        self.textOutput.setText(result)
        t2 = time.time()
        self.lineTime.setText("%f" % (t2 - t1) + "s")

    def segmentation(self, s):
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
                if (self.d[s[i:i + k]] * p[i + k] * div[i] > p[i] * self.d['_t_'] * div[i + k]):
                    p[i] = self.d[s[i:i + k]] * p[i + k]
                    div[i] = self.d['_t_'] * div[i + k]
                    t[i] = k
        i = 0
        out_put = u""
        while i < l:
            out_put = out_put +  s[i:i + t[i]] + '|'
            i = i + t[i]
        return out_put

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
