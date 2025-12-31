from PyQt5.QtWidgets import *
import sys
from veritabani.db import users
from masaustu_arayuz.main_window import MainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Giriş")
        self.setFixedSize(300, 220)

        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Kullanıcı Adı")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Şifre")
        self.password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Giriş Yap")
        self.btn_login.clicked.connect(self.login)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.btn_login)

        self.btn_register = QPushButton("Kayıt Ol")
        self.btn_register.clicked.connect(self.kayit_ac)
        layout.addWidget(self.btn_register)

        self.setLayout(layout)

    def login(self):
        user = users.find_one({
            "username": self.username.text(),
            "password": self.password.text()
        })

        if not user:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış")
            return

        self.main = MainWindow(user, self)
        self.main.show()
        self.hide()

    def kayit_ac(self):
        from masaustu_arayuz.register_window import RegisterWindow
        self.register = RegisterWindow()
        self.register.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())