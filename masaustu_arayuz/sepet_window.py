from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from veritabani.db import sepet
import os

class SepetWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sepetim")
        self.setFixedSize(600, 450)

        ana_layout = QVBoxLayout()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.icerik = QWidget()
        self.layout = QVBoxLayout()
        self.icerik.setLayout(self.layout)

        self.scroll.setWidget(self.icerik)
        ana_layout.addWidget(self.scroll)

        self.lbl_toplam = QLabel("Toplam: 0 ₺")
        self.lbl_toplam.setAlignment(Qt.AlignRight)
        self.lbl_toplam.setStyleSheet("font-weight: bold; font-size: 16px;")
        ana_layout.addWidget(self.lbl_toplam)

        self.setLayout(ana_layout)
        self.yukle()

    def yukle(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        urunler = list(sepet.find({"username": self.user["username"]}))
        toplam = 0

        for urun in urunler:
            kart = QFrame()
            kart.setStyleSheet("""
                QFrame {
                    border: 1px solid #ccc;
                    border-radius: 6px;
                    padding: 8px;
                }
            """)
            kart_layout = QHBoxLayout()

            lbl_resim = QLabel()
            lbl_resim.setFixedSize(80, 80)
            if os.path.exists(urun["resim"]):
                pixmap = QPixmap(urun["resim"]).scaled(
                    80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                lbl_resim.setPixmap(pixmap)

            lbl_bilgi = QLabel(
                f'{urun["ad"]}\n{urun["fiyat"]} ₺ x {urun["adet"]}'
            )

            btn_sil = QPushButton("Sil")
            btn_sil.clicked.connect(
                lambda _, uid=urun["_id"]: self.sil(uid)
            )

            kart_layout.addWidget(lbl_resim)
            kart_layout.addWidget(lbl_bilgi)
            kart_layout.addStretch()
            kart_layout.addWidget(btn_sil)

            kart.setLayout(kart_layout)
            self.layout.addWidget(kart)

            toplam += urun["fiyat"] * urun["adet"]

        self.lbl_toplam.setText(f"Toplam: {toplam} ₺")

    def sil(self, urun_id):
        sepet.delete_one({"_id": urun_id})

        self.yukle()
