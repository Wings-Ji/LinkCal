# -*- coding: utf-8 -*-
"""
Project: LinkCal
Creator: tianx
Create time: 2020-01-02 17:48
IDE: PyCharm
Introduction:
"""

import sys, math, methods
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow import Ui_MainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.initFunction()
        self.varDict1 = {} #本段到对端
        self.varDict2 = {} #对端到本端

    def initFunction(self):
        print("***************initFunction!****************")
        self.tabWidget.setCurrentIndex(0)

    def setSite(self):
        self.lbl_bd_city.setText(str(self.ledit_bd_city.text()))
        self.lbl_bd_province.setText(str(self.ledit_bd_province.text()))
        self.lbl_dd_city.setText(str(self.ledit_dd_city.text()))
        self.lbl_dd_province.setText(str(self.ledit_dd_province.text()))
        self.tabWidget.setCurrentIndex(1)

    def jumpInput(self):
        self.tabWidget.setCurrentIndex(1)

    def jumpResult(self):
        self.tabWidget.setCurrentIndex(2)

    def returnHome(self):
        self.tabWidget.setCurrentIndex(0)

    def singleCalculate(self):
        try:
            methods.getVarDict(self) #计算所有变量
        except Exception as e :
            print("捕获异常:",e)
        methods.setRes(self)
        self.tabWidget.setCurrentIndex(2)  # 跳转到计算结果页面

    def FYJ(self):#计算俯仰角
        methods.FYJ(self)

    def RcvSys(self):
        methods.RcvSys(self)

    #可视化功能：
    def heatMap(self):
        methods.createHeatMap(self)

    def createFreqMap(self):
        methods.createFreqMap(self)

    def getFilePath(self):
        methods.getFilePath(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
