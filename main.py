import sqlite3
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt


class StarterScreen(QWidget):  # стартовое окно
    def __init__(self):
        super().__init__()
        loadUi("starterscreen.ui", self)
        self.setWindowTitle("Справочник для туристов")
        self.btn_advisor.clicked.connect(self.loadadvisorscreen)
        self.btn_table.clicked.connect(self.loadtablescreen)

    def loadtablescreen(self):
        self.mainwindow = MainWindow()
        self.mainwindow.show()

    def loadadvisorscreen(self):
        self.advisor = Advisor()
        self.advisor.show()


class Advisor(QWidget):  # вкладка с советами туристам
    def __init__(self):
        super().__init__()
        loadUi("advisor.ui", self)
        self.advice_text.setVisible(True)
        self.setWindowTitle("Основные советы")


class MainWindow(QMainWindow):  # окно с таблицей
    def __init__(self):
        super(MainWindow, self).__init__()

        loadUi("tourismhelp.ui", self)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 200)
        self.tableWidget.setHorizontalHeaderLabels(["Страна", "Виза", "Язык", "Столица", "Население"])

        self.loaddata()

        self.btn_search.clicked.connect(self.searchcountries)
        self.btn_info.clicked.connect(self.showadvice)
        self.tableWidget.clicked.connect(self.countriesinfo)

    def loaddata(self):  # Отображение базы данных в таблице
        connection = sqlite3.connect("tourism.sqllite")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM countries"

        self.tableWidget.setRowCount(193)
        tablerow = 0
        for row in cur.execute(sqlquery):
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            tablerow += 1

    def searchcountries(self):  # поиск введеного названия страны по таблице
        name_search = self.search_field.text()
        for row in range(self.tableWidget.rowCount()):
            matching_items = self.tableWidget.findItems(name_search, Qt.MatchContains)
            if matching_items:
                item = self.tableWidget.item(row, 0)
                self.tableWidget.setRowHidden(row, name_search not in item.text())

    def showadvice(self):  # показать советы
        self.advisor = Advisor()
        self.advisor.show()

    def countriesinfo(self, index):
        country_id = index.row() + 1
        connection = sqlite3.connect("tourism.sqllite")
        cur = connection.cursor()
        query = f"SELECT * FROM countries WHERE country_id = {country_id}"
        self.countryinfo = CountryInfo()
        self.countryinfo.show()
        for row in cur.execute(query):
            self.countryinfo.country_name.setText(row[0])
            self.countryinfo.text.setText(f'Столица: {row[3]}\n'
                                          f'Язык: {row[2]}')
            pixmap = QPixmap(f'flags\{row[1]}.png')
            self.countryinfo.flag.setPixmap(pixmap)
            self.countryinfo.flag.show()




class CountryInfo(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("country_info.ui", self)



app = QApplication(sys.argv)
starterscreen = StarterScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(starterscreen)
widget.setFixedHeight(550)
widget.setFixedWidth(1000)
widget.show()

sys.exit(app.exec_())
