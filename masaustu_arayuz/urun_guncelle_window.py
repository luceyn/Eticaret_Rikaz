from PyQt5.QtWidgets import *
from veritabani.db import products

class UrunGuncelleWindow(QWidget):
    def __init__(self, urun):
        super().__init__()
        self.urun = urun
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ürün Güncelle")
        self.setFixedSize(350, 450)

        layout = QVBoxLayout()
        self.ad = QLineEdit(self.urun.get("ad", ""))
        self.fiyat = QLineEdit(str(self.urun.get("fiyat", "")))
        self.stok = QLineEdit(str(self.urun.get("stok", "")))
        self.tur = QLineEdit(self.urun.get("tur", ""))
        self.cinsiyet = QComboBox()
        self.cinsiyet.addItems(["Kadın", "Erkek", "Unisex"])
        if self.urun.get("cinsiyet"):
            self.cinsiyet.setCurrentText(self.urun["cinsiyet"])
        self.renk = QLineEdit(self.urun.get("renk", ""))
        self.etiketler = QLineEdit(", ".join(self.urun.get("etiketler", [])))
        self.btn_kaydet = QPushButton("Kaydet")
        self.btn_kaydet.clicked.connect(self.kaydet)

        layout.addWidget(QLabel("Ürün Adı"))
        layout.addWidget(self.ad)
        layout.addWidget(QLabel("Fiyat"))
        layout.addWidget(self.fiyat)
        layout.addWidget(QLabel("Stok"))
        layout.addWidget(self.stok)
        layout.addWidget(QLabel("Tür"))
        layout.addWidget(self.tur)
        layout.addWidget(QLabel("Cinsiyet"))
        layout.addWidget(self.cinsiyet)
        layout.addWidget(QLabel("Renk"))
        layout.addWidget(self.renk)
        layout.addWidget(QLabel("Etiketler (virgülle ayır)"))
        layout.addWidget(self.etiketler)
        layout.addWidget(self.btn_kaydet)
        
        self.setLayout(layout)

    def kaydet(self):
        products.update_one(
            {"_id": self.urun["_id"]},
            {"$set": {
                "ad": self.ad.text(),
                "fiyat": float(self.fiyat.text()),
                "stok": int(self.stok.text()),
                "tur": self.tur.text(),
                "cinsiyet": self.cinsiyet.currentText(),
                "renk": self.renk.text(),
                "etiketler": [e.strip() for e in self.etiketler.text().split(",") if e.strip()]
            }}
        )

        QMessageBox.information(self, "Başarılı", "Ürün güncellendi")

        self.close()
