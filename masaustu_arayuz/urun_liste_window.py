from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from veritabani.db import products
import os

class UrunListeWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()
        self.text_arama = QLineEdit()
        self.text_arama.setPlaceholderText("Ürün adı / etiket / tür ara...")
        self.text_arama.textChanged.connect(self.urunleri_yukle)
        ana_layout.addWidget(self.text_arama)
        filtre_layout = QHBoxLayout()

        self.txt_ara = QLineEdit()
        self.txt_ara.setPlaceholderText("Ürün adı ara...")
        self.combo_tur = QComboBox()
        self.combo_tur.addItems(["Hepsi", "Aksesuar", "Dış Giyim", "takımlar", "Kış Koleksiyonu", "Kitap", "Çanta"])
        self.combo_cinsiyet = QComboBox()
        self.combo_cinsiyet.addItems(["Hepsi", "Kadın", "Erkek", "Unisex"])
        self.combo_renk = QComboBox()
        self.combo_renk.addItems(["Hepsi", "Siyah", "Beyaz", "Kırmızı", "Mavi"])

        for combo in [self.combo_tur, self.combo_cinsiyet, self.combo_renk]:
            combo.currentTextChanged.connect(self.urunleri_yukle)

        filtre_layout.addWidget(self.combo_tur)
        filtre_layout.addWidget(self.combo_cinsiyet)
        filtre_layout.addWidget(self.combo_renk)

        ana_layout.addLayout(filtre_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.icerik = QWidget()
        self.grid = QGridLayout()
        self.grid.setSpacing(20)

        self.icerik.setLayout(self.grid)
        scroll.setWidget(self.icerik)

        ana_layout.addWidget(scroll)
        self.setLayout(ana_layout)

        self.urunleri_yukle()

    def urunleri_yukle(self):
        self.temizle()
        sorgu = {}
        if self.text_arama.text():
           sorgu["$or"] = [
               {"ad": {"$regex": self.text_arama.text(), "$options": "i"}},
               {"etiketler": {"$regex": self.text_arama.text(), "$options": "i"}},
               {"tur": {"$regex": self.text_arama.text(), "$options": "i"}}
           ]
        if self.combo_tur.currentText() != "Hepsi":
            sorgu["tur"] = self.combo_tur.currentText()

        if self.combo_cinsiyet.currentText() != "Hepsi":
            sorgu["cinsiyet"] = self.combo_cinsiyet.currentText()

        if self.combo_renk.currentText() != "Hepsi":
            sorgu["renk"] = self.combo_renk.currentText()

        urunler = list(products.find(sorgu))

        row = 0
        col = 0

        for urun in urunler:
            kart = self.urun_karti(urun)
            self.grid.addWidget(kart, row, col)

            col += 1
            if col == 3:
                col = 0
                row += 1
    def urun_karti(self, urun):
        kart = QFrame()
        kart.setFixedSize(200, 280)
        kart.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: white;
            }
        """)

        layout = QVBoxLayout()
        
        lbl_resim = QLabel()
        lbl_resim.setFixedSize(180, 140)
        lbl_resim.setAlignment(Qt.AlignCenter)

        resim_yol = urun.get("resim")
        if resim_yol and os.path.exists(resim_yol):
            pixmap = QPixmap(resim_yol).scaled(
                180, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            lbl_resim.setPixmap(pixmap)
        else:
            lbl_resim.setText("Resim yok")

        lbl_ad = QLabel(urun["ad"])
        lbl_ad.setAlignment(Qt.AlignCenter)
        lbl_ad.setStyleSheet("font-weight: bold;")

        lbl_fiyat = QLabel(f'{urun["fiyat"]} ₺')
        lbl_fiyat.setAlignment(Qt.AlignCenter)

        layout.addWidget(lbl_resim)
        layout.addWidget(lbl_ad)
        layout.addWidget(lbl_fiyat)

        if self.user.get("role") == "admin":
            btn_sil = QPushButton("Sil")
            btn_sil.clicked.connect(lambda: self.sil(urun["_id"]))

            layout.addWidget(btn_sil)
        if self.user.get("role") == "admin":
            btn_guncelle = QPushButton("Güncelle")
            btn_guncelle.clicked.connect(
                lambda _, u=urun: self.guncelle_pencere_ac(u)
            )
          
            layout.addWidget(btn_guncelle)
        if self.user.get("role") == "user":
            btn_sepet = QPushButton("Sepete Ekle")
            btn_sepet.clicked.connect(lambda _, u=urun: self.sepete_ekle(u))
            layout.addWidget(btn_sepet) 

        kart.setLayout(layout)
        return kart

    def sil(self, urun_id):
        products.delete_one({"_id": urun_id})
        QMessageBox.information(self, "Silindi", "Ürün silindi")
        self.temizle()
        self.urunleri_yukle()

    def temizle(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def guncelle_pencere_ac(self, urun):
        from masaustu_arayuz.urun_guncelle_window import UrunGuncelleWindow
        self.guncelle_window = UrunGuncelleWindow(urun)
        self.guncelle_window.show()
       
    def sepete_ekle(self, urun):
        from veritabani.db import sepet
        mevcut= sepet.find_one({
            "username": self.user["username"],
            "urun_id": urun["_id"]
        })
        if mevcut:
            sepet.update_one(
                {"_id": mevcut["_id"]},
                {"$inc": {"adet": 1}}
            )
        else:
            sepet.insert_one({
                "username": self.user["username"],
                "urun_id": urun["_id"],
                "ad": urun["ad"],
                "fiyat": urun["fiyat"],
                "adet": 1,
                "resim": urun["resim"]
            })
        QMessageBox.information(self, "sepet", "ürün sepete eklendi")
        
        from veritabani.db import carts
        def sepete_ekle(self, urun):
            sepet = carts.find_one({"user_id": self.user["_id"]})

            if not sepet:
                carts.insert_one({
                    "user_id": self.user["_id"],
                    "items": [{
                        "product_id": urun["_id"],
                        "ad": urun["ad"],
                        "fiyat": urun["fiyat"],
                        "adet": 1
                    }]
                })
            else:
                for item in sepet["items"]:
                    if item["product_id"] == urun["_id"]:
                        carts.update_one(
                            {
                                "user_id": self.user["_id"],
                                "items.product_id": urun["_id"]
                            },
                            {"$inc": {"items.$.adet": 1}}
                        )
                        break
                else:
                    carts.update_one(
                        {"user_id": self.user["_id"]},
                        {"$push": {
                            "items": {
                                "product_id": urun["_id"],
                                "ad": urun["ad"],
                                "fiyat": urun["fiyat"],
                                "adet": 1
                            }
                         }}
                    )

            QMessageBox.information(self, "Sepet", "Ürün sepete eklendi")

