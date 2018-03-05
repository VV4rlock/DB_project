from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtCore import QSize, Qt
from db_manager import DbManager
from bills import Bills

# Наследуемся от QMainWindow
from profile import Profile


class Lots(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self,win_manager,user):
        self.user=user
        self.wm=win_manager
        self.wm.add("lots", self)
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

        header, data = self.db.get_lots()
        self.data=data
        self.table.setColumnCount(len(header))  # Устанавливаем три колонки
        self.table.setRowCount(len(data))  # и одну строку в таблице

        i = 0
        for id,description, price, login, category in data:
            self.table.setItem(i, 0, self._set_not_edit(description))
            self.table.setItem(i, 1, self._set_not_edit(price))
            self.table.setItem(i, 2, self._set_not_edit(login))
            self.table.setItem(i, 3, self._set_not_edit(category))
            i += 1


        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(header)


        search_btn = QPushButton('Search', self)
        #btn.resize(btn.sizeHint())
        search_btn.clicked.connect(self.on_search_clicked)

        self.search_line=QLineEdit()


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Menu')
        act=fileMenu.addAction("log out")
        act.triggered.connect(self.on_logout_clicked)

        bills=fileMenu.addAction("my_bills")
        bills.triggered.connect(self.on_bills_clicked)

        bills = fileMenu.addAction("profile")
        bills.triggered.connect(self.on_profile_clicked)

        reload_btn = QPushButton('reload table', self)
        reload_btn.clicked.connect(self.on_reload_btn)

        self.table.cellClicked.connect(self.cell_was_clicked)
        #self.table.doubleClicked.connect(self.cell_was_clicked)

        grid_layout.addWidget(search_btn,0,0)
        grid_layout.addWidget(self.search_line, 0, 1)
        grid_layout.addWidget(reload_btn,1,0)
        grid_layout.addWidget(self.table, 1, 1)  # Добавляем таблицу в сетку
        self.show()

    def on_profile_clicked(self):
        self.pr=Profile(self.wm,self.user)
        self.setVisible(False)

    def on_bills_clicked(self):
        self.bills=Bills(self.wm,self.user)
        self.setVisible(False)


    def cell_was_clicked(self, row, column):
        #print("Row %d and Column %d was clicked" % (row, column))
        item = self.data[row]
        reply = QMessageBox.question(self, 'Are you sure?',
                                     "Do you want to buy {} for {}$?".format(item[1],item[2]),
                                     QMessageBox.No | QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.db.buy_lot(self.user[0], item[0])
            except:
                pass


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

    def on_search_clicked(self):
        if self.search_line.text()=="":
            return
        #print("search", self.search_line.text())
        self.table.clear()
        try:
            header, data = self.db.search_lots_by_description(self.search_line.text())
        except:
            return
        self.data=data
        self.table.setColumnCount(len(header))  # Устанавливаем три колонки
        self.table.setRowCount(len(data))  # и одну строку в таблице
        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(header)
        i = 0
        for id,description, price, login, category in data:
            self.table.setItem(i, 0, self._set_not_edit(description))
            self.table.setItem(i, 1, self._set_not_edit(price))
            self.table.setItem(i, 2, self._set_not_edit(login))
            self.table.setItem(i, 3, self._set_not_edit(category))
            i += 1

    def on_reload_btn(self):
        #print("reload")
        self.table.clear()
        header, data = self.db.get_lots()
        self.data=data
        self.table.setColumnCount(len(header))  # Устанавливаем три колонки
        self.table.setRowCount(len(data))  # и одну строку в таблице
        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(header)
        i = 0
        for id,description, price, login, category in data:
            #self.table.setItem(i, 0, self._set_not_edit(id))
            self.table.setItem(i, 0, self._set_not_edit(description))
            self.table.setItem(i, 1, self._set_not_edit(price))
            self.table.setItem(i, 2, self._set_not_edit(login))
            self.table.setItem(i, 3, self._set_not_edit(category))
            i += 1



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    #mw = Lots()
    #mw.show()
    sys.exit(app.exec())