# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '1.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 700, 400))
        self.tableView.setObjectName("tableView")
        self.graphWidget = pyqtgraph.PlotWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(0, 400, 700, 275))
        self.graphWidget.setObjectName("graphWidget")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(700, 0, 200, 381))
        self.groupBox.setObjectName("groupBox")
        self.spBoxColumns = QtWidgets.QSpinBox(self.groupBox)
        self.spBoxColumns.setGeometry(QtCore.QRect(75, 70, 120, 31))
        self.spBoxColumns.setMinimum(5)
        self.spBoxColumns.setMaximum(99)
        self.spBoxColumns.setObjectName("spBoxColumns")
        self.spBoxRows = QtWidgets.QSpinBox(self.groupBox)
        self.spBoxRows.setGeometry(QtCore.QRect(75, 30, 120, 31))
        self.spBoxRows.setMinimum(1)
        self.spBoxRows.setObjectName("spBoxRows")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(5, 40, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(5, 80, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.btResizeTable = QtWidgets.QPushButton(self.groupBox)
        self.btResizeTable.setGeometry(QtCore.QRect(85, 110, 111, 31))
        self.btResizeTable.setObjectName("btResizeTable")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(5, 240, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setScaledContents(False)
        self.label_3.setObjectName("label_3")
        self.btRandomNumbers = QtWidgets.QPushButton(self.groupBox)
        self.btRandomNumbers.setGeometry(QtCore.QRect(45, 300, 151, 41))
        self.btRandomNumbers.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.btRandomNumbers.setObjectName("btRandomNumbers")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 891, 26))
        self.menubar.setObjectName("menubar")
        self.menuTxt = QtWidgets.QMenu(self.menubar)
        self.menuTxt.setObjectName("menuTxt")
        self.menuHdf = QtWidgets.QMenu(self.menubar)
        self.menuHdf.setObjectName("menuHdf")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuTxt.menuAction())
        self.menubar.addAction(self.menuHdf.menuAction())

        self.retranslateUi(MainWindow)
        self.btRandomNumbers.clicked.connect(self.tableView.update)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btRandomNumbers.setText(_translate("MainWindow", "Random"))
        self.btResizeTable.setText(_translate("MainWindow", "Resize"))
        self.label.setText(_translate("MainWindow", "Rows"))
        self.label_2.setText(_translate("MainWindow", "Columns"))
        self.label_3.setText(_translate("MainWindow", "Press to fill table \n" "with random numbers"))
        self.menuTxt.setTitle(_translate("MainWindow", "TXT"))
        self.menuHdf.setTitle(_translate("MainWindow", "HDF"))

