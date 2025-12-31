import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt
from masaustu_arayuz.urun_liste_window import UrunListeWindow
from masaustu_arayuz.urun_ekle_window import UrunEkleWindow
from masaustu_arayuz.sepet_window import SepetWindow



class MainWindow(QMainWindow):
    def __init__(self, user, login_window):
        super().__init__()
        self.user = user
        self.menu_acik = False
        self.login_window= login_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RIKAZ")
        self.setFixedSize(1000, 600)

        ana_widget = QWidget()
        ana_layout = QHBoxLayout()
        ana_layout.setContentsMargins(0, 0, 0, 0)

        # 🔹 YAN MENÜ
        self.menu = QFrame()
        self.menu.setFixedWidth(0)
        self.menu.setStyleSheet("""
            QFrame {
                background-color: #2c2c2c;
                color: white;
            }
            QPushButton {
                background: transparent;
                color: white;
                text-align: left;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)

        menu_layout = QVBoxLayout()

        self.btn_urunler = QPushButton("🛒 Ürünler")
        self.btn_sepet = QPushButton("🧺 Sepet")
        self.btn_cikis = QPushButton("🚪 Çıkış")
        self.btn_cikis.clicked.connect(self.cikis_yap)
        self.btn_sepet.clicked.connect(self.sepet_ac)


        menu_layout.addWidget(self.btn_urunler)
        menu_layout.addWidget(self.btn_sepet)
        menu_layout.addStretch()
        menu_layout.addWidget(self.btn_cikis)

        self.menu.setLayout(menu_layout)

        # 🔹 SAĞ TARAF (İÇERİK)
        self.icerik = QStackedWidget()

        # 🔹 ÜRÜN LİSTE SAYFASI
        self.urun_liste_sayfa = UrunListeWindow(self.user)
        self.icerik.addWidget(self.urun_liste_sayfa)

        # 🔹 ÜST BAR
        self.btn_menu = QPushButton("☰")
        self.btn_menu.setFixedSize(40, 40)
        self.btn_menu.clicked.connect(self.menu_toggle)
        
        if self.user.get("role")== "admin":
            self.btn_urun_ekle= QPushButton("Ürün Ekle")
            menu_layout.insertWidget(1, self.btn_urun_ekle)
            self.btn_urun_ekle.clicked.connect(self.urun_ekle_goster)

        if self.user.get("role") == "admin":
           self.btn_urun_ekle.clicked.connect(self.urun_ekle_ac)
    

        ust_bar = QHBoxLayout()
        ust_bar.addWidget(self.btn_menu)
        ust_bar.addStretch()

        sag_layout = QVBoxLayout()
        sag_layout.addLayout(ust_bar)
        sag_layout.addWidget(self.icerik)

        ana_layout.addWidget(self.menu)
        ana_layout.addLayout(sag_layout)

        ana_widget.setLayout(ana_layout)
        self.setCentralWidget(ana_widget)

        # 🔹 BAĞLANTILAR
        self.btn_urunler.clicked.connect(self.urunleri_goster)
        self.btn_cikis.clicked.connect(self.close)

    def menu_toggle(self):
        if self.menu_acik:
            self.menu.setFixedWidth(0)
        else:
            self.menu.setFixedWidth(200)
        self.menu_acik = not self.menu_acik

    def urunleri_goster(self):
        self.icerik.setCurrentWidget(self.urun_liste_sayfa)

    def urun_ekle_goster(self):
        from masaustu_arayuz.urun_ekle_window import UrunEkleWindow
        self.urun_ekle_sayfa = UrunEkleWindow()
        self.icerik.addWidget(self.urun_ekle_sayfa)
        self.icerik.setCurrentWidget(self.urun_ekle_sayfa)
  
    def cikis_yap(self):
        self.close()
        self.login_window.show()

    def urun_ekle_ac(self):
        self.urun_ekle = UrunEkleWindow()
        self.urun_ekle.show()

    def sepet_ac(self):
        self.sepet_pencere= SepetWindow(self.user)
        self.sepet_pencere.show()