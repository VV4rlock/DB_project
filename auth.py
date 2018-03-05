import sys
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from signup import Signup
from db_manager import DbManager
from window_manager import WindowsManager
from main_table import Lots


class Login(QWidget):
    def __init__(self,win_manager):
        super().__init__()
        self.wm=win_manager
        self.wm.add("login",self)
        self.db=wm.get_window("db")
        self.title = 'Log In'
        self.left = 350
        self.top = 350
        self.width = 340
        self.height = 150
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        grid_layout = QGridLayout()  # Создаём QGridLayout

        self.setLayout(grid_layout)
        self.login_label=QLabel("Login:")
        self.login_field=QLineEdit()
        self.password_label=QLabel("Password:")
        self.password_field=QLineEdit()
        self.signup_btn = QPushButton('Sign Up', self)
        self.login_btn = QPushButton('Log In', self)
        grid_layout.addWidget(self.login_label,0,0)
        grid_layout.addWidget(self.login_field, 0, 1)
        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password_field, 1, 1)
        grid_layout.addWidget(self.signup_btn,2,0)
        grid_layout.addWidget(self.login_btn, 2, 1)

        self.login_btn.clicked.connect(self.on_log_in_btn_cklick)
        self.signup_btn.clicked.connect(self.on_signup_btn_clicked)

        self.password_field.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.show()

    def on_log_in_btn_cklick(self):
        login=self.login_field.text()
        password=self.password_field.text()

        account=self.db.auth(login,password)
        if account is None:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Invalid login or password!')
            return

        self.setVisible(False)
        self.tabel=Lots(self.wm,account)




    def on_signup_btn_clicked(self):
        self.sg=Signup(self.wm)
        self.sg.show()
        self.setVisible(False)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    wm = WindowsManager()
    wm.add("db", DbManager())
    ex = Login(wm)
    sys.exit(app.exec_())