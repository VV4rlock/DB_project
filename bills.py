from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtCore import QSize, Qt
from db_manager import DbManager

# Наследуемся от QMainWindow
class Bills(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self,win_manager,user):
        self.user=user
        self.wm=win_manager
        self.wm.add("bills", self)
        self.db=self.wm.get_window("db")
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(650, 80))  # Устанавливаем размеры
        self.setWindowTitle("Lots")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        self.table = QTableWidget(self)  # Создаём таблицу


        header, data = self.db.get_bills(self.user[0])
        self.data=data
        self.table.setColumnCount(len(header))  # Устанавливаем три колонки
        self.table.setRowCount(len(data))  # и одну строку в таблице

        i = 0
        for id,seller,buyer,date,description, category,price in data:
            self.table.setItem(i, 0, self._set_not_edit(seller))
            self.table.setItem(i, 1, self._set_not_edit(buyer))
            self.table.setItem(i, 2, self._set_not_edit(date))
            self.table.setItem(i, 3, self._set_not_edit(description))
            self.table.setItem(i, 4, self._set_not_edit(category))
            self.table.setItem(i, 5, self._set_not_edit(price))
            i += 1


        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(header)


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Menu')
        act=fileMenu.addAction("log out")
        act.triggered.connect(self.on_logout_clicked)

        bills = fileMenu.addAction("lots")
        bills.triggered.connect(self.on_lots_clicked)

        grid_layout.addWidget(self.table, 0, 0)  # Добавляем таблицу в сетку
        self.show()


    def on_lots_clicked(self):
        lots=self.wm.get_window("lots")
        lots.setVisible(True)
        self.setVisible(False)



    def _set_not_edit(self,param):
        temp = QTableWidgetItem(str(param))
        temp.setFlags(QtCore.Qt.ItemIsEnabled)

        return temp

    def on_logout_clicked(self):
        lg=self.wm.get_window("login")
        self.setVisible(False)
        lg.setVisible(True)


    def act_on_menubar(self):
        print("Clicked")


    def on_reload_btn(self):
        #print("reload")
        self.table.clear()
        header, data = self.db.get_bills(self.user[0])
        self.data = data
        self.table.setColumnCount(len(header))  # Устанавливаем три колонки
        self.table.setRowCount(len(data))  # и одну строку в таблице

        i = 0
        for id, seller, buyer, date, description, category, price in data:
            self.table.setItem(i, 0, self._set_not_edit(seller))
            self.table.setItem(i, 1, self._set_not_edit(buyer))
            self.table.setItem(i, 2, self._set_not_edit(date))
            self.table.setItem(i, 3, self._set_not_edit(description))
            self.table.setItem(i, 4, self._set_not_edit(category))
            self.table.setItem(i, 5, self._set_not_edit(price))
            i += 1

