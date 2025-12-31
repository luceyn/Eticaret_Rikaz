from PyQt5.QtWidgets import *
from veritabani.db import users

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Kayıt Ol")
        self.setFixedSize(300, 250)

        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Kullanıcı Adı")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Şifre")
        self.password.setEchoMode(QLineEdit.Password)

        self.btn_register = QPushButton("Kayıt Ol")
        self.btn_register.clicked.connect(self.register)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.btn_register)

        self.setLayout(layout)

    def register(self):
        if self.username.text() == "" or self.password.text() == "":
            QMessageBox.warning(self, "Hata", "Alanlar boş olamaz")
            return

        if users.find_one({"username": self.username.text()}):
            QMessageBox.warning(self, "Hata", "Bu kullanıcı zaten var")
            return

        users.insert_one({
            "username": self.username.text(),
            "password": self.password.text(),
            "role": "user"
        })

        QMessageBox.information(self, "Başarılı", "Kayıt oluşturuldu")
        self.close()
