import sqlite3
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt


class Advisor(QWidget):     # вкладка с советами туристам
    def __init__(self):
        super().__init__()
        loadUi("advisor.ui", self)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("tourismhelp.ui", self)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setHorizontalHeaderLabels(["Страна", "Код страны(2)", "Код страны(3)", "Виза", "Флаг"])

        self.loaddata()

        self.btn_search.clicked.connect(self.SearchModels)
        self.btn_info.clicked.connect(self.showadvice)

    def loaddata(self):  # Отображение базы данных в таблице
        connection = sqlite3.connect("tourism.sqllite")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM countries"

        self.tableWidget.setRowCount(193)
        tablerow = 0
        for row in cur.execute(sqlquery):
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            a = self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
            tablerow += 1

    def SearchModels(self):  # поиск введеного названия страны по таблице
        name_search = self.search_field.text()
        for row in range(self.tableWidget.rowCount()):
            matching_items = self.tableWidget.findItems(name_search, Qt.MatchContains)
            if matching_items:
                item = self.tableWidget.item(row, 0)
                self.tableWidget.setRowHidden(row, name_search not in item.text())

    def showadvice(self):   # показать советы
        self.advisor = Advisor()
        self.advisor.show()


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(850)
widget.setFixedWidth(1120)
widget.show()

sys.exit(app.exec_())
