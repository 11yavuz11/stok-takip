import sys
from PyQt5.QtWidgets import *
from pencere import *
import sqlite3


Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_Pencere()
ui.setupUi(penAna)
penAna.show()


global curs
global conn

conn=sqlite3.connect('veritabani.db')
curs=conn.cursor()
sorguCreTblSpor=("CREATE TABLE IF NOT EXISTS parca(     \
        Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,      \
        Seri_No TEXT NOT NULL UNIQUE,                       \
        Parca_Adi TEXT NOT NULL,                     \
        Adet TEXT NOT NULL,                          \
        Fiyat TEXT NOT NULL)")
curs.execute(sorguCreTblSpor)
conn.commit()



def Ekle():
    seri_no=ui.ln_serino.text()
    parca_adi= ui.ln_parcaadi.text()
    adet=ui.ln_adet.text()
    fiyat=float(ui.ln_fiyat.text())
    cevap=QMessageBox.question(penAna,"KAYIT EKLEME","Kaydı eklemek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        curs.execute("INSERT INTO parca \
                      (Seri_No,Parca_Adi,Adet,Fiyat) \
                    VALUES (?,?,?,?)", \
                     (seri_no,parca_adi,adet,fiyat))
        conn.commit()
    Listele()

def Listele():
    ui.tableWidget.clear()
    ui.tableWidget.setHorizontalHeaderLabels(("No","Seri No","Parca Adı","Adet","Fiyat"))
    ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    curs.execute("SELECT * FROM parca")
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tableWidget.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
            ui.ln_serino.clear()
            ui.ln_parcaadi.clear()
            ui.ln_adet.clear()
            ui.ln_fiyat.clear()


def Cikis():
    cevap=QMessageBox.question(penAna,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        conn.close()
        sys.exit(Uygulama.exec_())
    else:
        penAna.show()


def Sil():
    cevap=QMessageBox.question(penAna,"KAYIT SİL","Kaydı silmek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes:
        secili = ui.tableWidget.selectedItems()
        silinecek = secili[1].text()
        try:
            curs.execute("DELETE FROM parca WHERE Seri_No='%s'" % (silinecek))
            conn.commit()

            Listele()

            ui.statusbar.showMessage("KAYIT SİLME İŞLEMİ BAŞARIYLA GERÇEKLEŞTİ...", 10000)
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı:" + str(Hata))
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi...", 10000)

def Ara():

    aranan1=ui.ln_serino.text()
    aranan2=ui.ln_parcaadi.text()
    curs.execute("SELECT * FROM parca WHERE Seri_No=? OR Parca_Adi=?",(aranan1, aranan2))
    conn.commit()
    ui.tableWidget.clear()
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tableWidget.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))

def Temizle():
    ui.ln_serino.clear()
    ui.ln_parcaadi.clear()
    ui.ln_adet.clear()
    ui.ln_fiyat.clear()


def Doldur():
    try:
        secili=ui.tableWidget.selectedItems()
        ui.ln_serino.setText(secili[1].text())
        ui.ln_parcaadi.setText(secili[2].text())
        ui.ln_adet.setText(secili[3].text())
        ui.ln_fiyat.setText(secili[4].text())
    except Exception as hata:
        ui.ln_serino.clear()
        ui.ln_parcaadi.clear()
        ui.ln_adet.clear()
        ui.ln_fiyat.clear()


def Guncelle():
    cevap=QMessageBox.question(penAna,"KAYIT GÜNCELLE","Kaydı güncellemek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        try:
            secili=ui.tableWidget.selectedItems()
            _Id=int(secili[0].text())
            _seri_no=ui.ln_serino.text()
            _parca_adi=ui.ln_parcaadi.text()
            _adet=ui.ln_adet.text()
            _fiyat=ui.ln_fiyat.text()

            curs.execute("UPDATE parca SET Seri_No=?, Parca_Adi=?, Adet=?, Fiyat=? WHERE Id=?",(_seri_no,_parca_adi,_adet,_fiyat,_Id))
            conn.commit()
            Listele()
        except Exception as hata:
            ui.statusbar.showMessage("Şöyle bir hata meydana geldi" + str(hata))
    else:
        ui.statusbar.showMessage("Güncelleme iptal edildi",5000)




Listele()
ui.btn_kaydet.clicked.connect(Ekle)
ui.btn_cikis.clicked.connect(Cikis)
ui.btn_sil.clicked.connect(Sil)
ui.btn_ara.clicked.connect(Ara)
ui.btn_temizle.clicked.connect(Temizle)
ui.btn_guncelle.clicked.connect(Guncelle)
ui.btn_listele.clicked.connect(Listele)
ui.tableWidget.itemSelectionChanged.connect(Doldur)

sys.exit(Uygulama.exec_())