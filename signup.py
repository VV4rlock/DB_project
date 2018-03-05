import sys
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QGridLayout, QLabel, QPushButton, \
    QMessageBox
from PyQt5.QtGui import QIcon
from db_manager import DbManager
from window_manager import WindowsManager


class Signup(QWidget):
    def __init__(self,win_manager):
        self.wm=win_manager
        self.wm.add("signup", self)
        self.db=self.wm.get_window("db")
        super().__init__()
        self.title = 'Sign Up'
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
        login_label=QLabel("Login:")
        self.login_field=QLineEdit()
        pass_label=QLabel("Password:")
        self.password_field=QLineEdit()
        email_label = QLabel("e-mail:")
        self.email_field = QLineEdit()
        purse_label = QLabel("Purse:")
        self.purse_field = QLineEdit()
        signup_btn = QPushButton('Sign Up', self)
        grid_layout.addWidget(login_label,0,0)
        grid_layout.addWidget(self.login_field, 0, 1)
        grid_layout.addWidget(pass_label, 1, 0)
        grid_layout.addWidget(self.password_field, 1, 1)
        grid_layout.addWidget(email_label, 2, 0)
        grid_layout.addWidget(self.email_field, 2, 1)
        grid_layout.addWidget(purse_label, 3, 0)
        grid_layout.addWidget(self.purse_field, 3, 1)
        grid_layout.addWidget(signup_btn,4,1)
        signup_btn.clicked.connect(self.on_signup_click)
        self.password_field.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.show()

    def on_signup_click(self):
        try:

            self.db.signup(self.login_field.text(),self.purse_field.text(),self.password_field.text(),self.email_field.text())

        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Such user already is exist!')
            return
        #придумать как вернуться назад к ауфу
        QMessageBox.information(self,"User created.", str(self.login_field.text()+" has been added! Please, Log In!"),QMessageBox.Ok)
        lg=self.wm.get_window("login")
        lg.setVisible(True)
        self.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wm=WindowsManager()
    wm.add("db",DbManager())
    ex = Signup(wm)
    sys.exit(app.exec_())