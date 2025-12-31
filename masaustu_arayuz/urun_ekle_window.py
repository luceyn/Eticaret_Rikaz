from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from veritabani.db import products
import shutil
import os

class UrunEkleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resim_yolu = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ürün Ekle")
        self.setFixedSize(350, 400)

        layout = QVBoxLayout()

        self.ad = QLineEdit()
        self.ad.setPlaceholderText("Ürün Adı")

        self.fiyat = QLineEdit()
        self.fiyat.setPlaceholderText("Fiyat")

        self.stok = QLineEdit()
        self.stok.setPlaceholderText("Stok")

        self.tur = QLineEdit()
        self.tur.setPlaceholderText("Tür (Örn: Giyim)")

        self.cinsiyet = QComboBox()
        self.cinsiyet.addItems(["Erkek", "Kadın", "Unisex"])

        self.renk = QLineEdit()
        self.renk.setPlaceholderText("Renk")

        self.etiketler = QLineEdit()
        self.etiketler.setPlaceholderText("Etiketler (virgülle ayır)")
        layout.addWidget(self.tur)
        layout.addWidget(self.cinsiyet)
        layout.addWidget(self.renk)
        layout.addWidget(self.etiketler)

        self.btn_resim = QPushButton("Resim Seç")
        self.btn_resim.clicked.connect(self.resim_sec)

        self.lbl_resim = QLabel("Resim seçilmedi")
        self.lbl_resim.setAlignment(Qt.AlignCenter)

        self.btn_kaydet = QPushButton("Kaydet")
        self.btn_kaydet.clicked.connect(self.kaydet)

        layout.addWidget(self.ad)
        layout.addWidget(self.fiyat)
        layout.addWidget(self.stok)
        layout.addWidget(self.btn_resim)
        layout.addWidget(self.lbl_resim)
        layout.addWidget(self.btn_kaydet)

        self.setLayout(layout)

    def resim_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(
            self,
            "Resim Seç",
            "",
            "Resimler (*.png *.jpg *.jpeg)"
        )

        if dosya:
            dosya_adi = os.path.basename(dosya)
            hedef_klasor = "images/urunler"
            hedef_yol = os.path.join(hedef_klasor, dosya_adi)

            shutil.copy(dosya, hedef_yol)

            self.resim_yolu = hedef_yol
            QMessageBox.information(self, "Bilgi", "Resim seçildi")

    def kaydet(self):
        if not all([self.ad.text(), self.fiyat.text(), self.stok.text(), self.resim_yolu]):
            QMessageBox.warning(self, "Hata", "Tüm alanlar ve resim zorunlu")
            return
        products.insert_one({
            "ad": self.ad.text(),
            "fiyat": float(self.fiyat.text()),
            "stok": int(self.stok.text()),
            "resim": self.resim_yolu,
            "tur": self.tur.text().lower(),
            "cinsiyet": self.cinsiyet.currentText().lower(),
            "renk": self.renk.text(),
            "etiketler": [e.strip().lower() for e in self.etiketler.text().split(",")]
})
        QMessageBox.information(self, "Başarılı", "Ürün eklendi")
        self.close()