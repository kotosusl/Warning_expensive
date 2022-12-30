import sys
from random import randint
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import csv


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(688, 399)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 651, 321))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(320, 350, 41, 16))
        self.label.setObjectName("label")
        self.total = QtWidgets.QTextEdit(self.centralwidget)
        self.total.setGeometry(QtCore.QRect(370, 340, 301, 31))
        self.update_ = QtWidgets.QPushButton(self.centralwidget)
        self.update_.setGeometry(QtCore.QRect(20, 340, 93, 28))
        self.update_.setObjectName("update_")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.update_.setText(_translate("MainWindow", "Обновить"))
        self.label.setText(_translate("MainWindow", "Итого:"))


class Check(Ui_MainWindow):
    def __init__(self):
        super(Check, self).setupUi(self)
        self.setWindowTitle('Осторожно: дорого!')
        with open('price.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            lst = []
            for i, row in enumerate(reader):
                lst.append(row)
        with open('price.csv', 'w', newline='', encoding="utf8") as f:
            writer = csv.writer(
                f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i, row in enumerate(lst):
                if i == 0:
                    writer.writerow(row + ['Количество'])
                else:
                    writer.writerow(row + ['0'])
        self.loadTable('price.csv')
        self.tableWidget.itemChanged.connect(self.get_sum)
        self.update_.clicked.connect(self.get_res)

    def get_res(self):
        self.loadTable('price.csv')

    def get_sum(self, item):
        with open('price.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            lst = []
            for i, row in enumerate(reader):
                lst.append(row)
        with open('price.csv', 'w', newline='', encoding="utf8") as f:
            writer = csv.writer(
                f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i, row in enumerate(lst):
                if i == item.row() + 1:
                    writer.writerow(row[:-1] + [item.text()])
                else:
                    writer.writerow(row)
        if item.column() == 2:
            summa = 0
            with open('price.csv', encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for i, row in enumerate(reader):
                    if i != 0:
                        summa += int(row[2]) * int(row[1])
            self.total.setText(str(summa))

    def loadTable(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            title = next(reader)
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                color = QtGui.QColor(randint(0, 255), randint(0, 255), randint(0, 255))
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(elem))
                    if i < 5:
                        self.tableWidget.item(i, j).setBackground(color)


if __name__ == '__main__':
    app = QApplication([])
    form = Check()
    form.show()
    sys.exit(app.exec())
