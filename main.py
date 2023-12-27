import sqlite3
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5.QtCore import Qt


class StarterScreen(QWidget):  # стартовое окно
    def __init__(self):
        super().__init__()
        loadUi("starterscreen.ui", self)
        self.setWindowTitle("Справочник для туристов")
        self.btn_advisor.clicked.connect(self.load_advisor_screen)
        self.btn_table.clicked.connect(self.load_table_screen)

    def load_table_screen(self):
        self.mainwindow = MainWindow()
        self.mainwindow.show()
        self.close()

    def load_advisor_screen(self):
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

        self.load_data()

        self.btn_search.clicked.connect(self.search_countries)
        self.btn_info.clicked.connect(self.show_advice)
        self.tableWidget.clicked.connect(self.countries_info)

    def load_data(self):  # Отображение базы данных в таблице
        connection = sqlite3.connect("tourism.sqllite")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM countries"

        self.tableWidget.setRowCount(193)
        table_row = 0
        for row in cur.execute(sqlquery):
            self.tableWidget.setItem(table_row, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(table_row, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(table_row, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(table_row, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(table_row, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            table_row += 1

    def search_countries(self):  # поиск введеного названия страны по таблице
        name_search = self.search_field.text()
        for row in range(self.tableWidget.rowCount()):
            matching_items = self.tableWidget.findItems(name_search, Qt.MatchContains)
            if matching_items:
                item = self.tableWidget.item(row, 0)
                self.tableWidget.setRowHidden(row, name_search not in item.text())

    def show_advice(self):  # показать советы
        self.advisor = Advisor()
        self.advisor.show()

    def countries_info(self, index):
        country_id = index.row() + 1
        connection = sqlite3.connect("tourism.sqllite")
        cur = connection.cursor()
        query = f"SELECT * FROM countries WHERE country_id = {country_id}"
        self.countryinfo = CountryInfo()
        self.countryinfo.show()
        for row in cur.execute(query):
            self.countryinfo.country_name.setText(row[0])
            self.countryinfo.text.setText(f'Столица: {row[3]}\n'
                                          f'Язык: {row[2]}\n'
                                          f'Население: {row[4]} человек\n'
                                          f'Описание:\n'
                                          f' {row[-1]}')
            pixmap = QPixmap(f'flags{row[-3]}.png')
            self.countryinfo.text.setWordWrap(True)
            self.countryinfo.flag.setPixmap(pixmap)
            self.countryinfo.flag.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение',
                                     "Вы уверены, что хотите выйти?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Да:
            event.accept()
        else:
            event.ignore()


class CountryInfo(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("country_info.ui", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    starterscreen = StarterScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(starterscreen)
    widget.setFixedHeight(550)
    widget.setFixedWidth(1000)
    widget.show()

    sys.exit(app.exec_())
