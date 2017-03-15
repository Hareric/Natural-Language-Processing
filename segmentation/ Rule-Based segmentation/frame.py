# coding=utf-8
import sys
from PyQt4 import QtCore, QtGui, uic
import cut_word
import time

qtCreatorFile = "./ui/mainwindow.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.RMMButton.clicked.connect(self.rmm)
        self.MMButton.clicked.connect(self.mm)
        self.CW = cut_word.CutWord()
        # self.setWindowTitle("Darlin")
        self.setWindowTitle(QtCore.QString(u"Darlin 陈文达 吴嘉琳 翁靖达"))

    def rmm(self):
        content = unicode(self.textInput.toPlainText())
        result = self.CW.rmm_cut(content)
        t1 = time.time()
        self.textOutput.setText('|'.join(result))
        t2 = time.time()
        self.lineTime.setText("%f" % (t2 - t1) + "s")

    def mm(self):
        content = unicode(self.textInput.toPlainText())
        result = self.CW.mm_cut(content)
        t1 = time.time()
        self.textOutput.setText('|'.join(result))
        t2 = time.time()
        self.lineTime.setText("%f" % (t2 - t1) + "s")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
