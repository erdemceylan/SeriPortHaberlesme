from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QTextEdit
import sys
import serial.tools.list_ports as portListesi
import serial
import threading
import time


benimPortum = serial.Serial()



class Pencere(QWidget):
    def __init__(self):
        super().__init__()

        self.araYuz()
        self.pencereOlaylari()
        self.show()
        self.devam = 0
    
    def pencereOlaylari(self):
        self.pushButtonBaglan.clicked.connect(self.portBaglan)
        self.pushButtonBaglantiKes.clicked.connect(self.portBaglantiKes)
        self.pushButtonGonder.clicked.connect(self.portVeriGonder)
    

    def portVeriGonder(self):
        if benimPortum.is_open:
            benimPortum.write(self.textEditGidecekMesaj.toPlainText().encode("utf-8"))
            print("Giden Veri: " ,self.textEditGidecekMesaj.toPlainText())
            self.textEditGidecekMesaj.clear()

    def portBaglantiKes(self):
        if benimPortum.is_open:
            benimPortum.close()
            if not benimPortum.is_open:
                self.pushButtonBaglan.setEnabled(True)
                self.pushButtonBaglantiKes.setEnabled(False)
                self.pushButtonGonder.setEnabled(False)
                self.devam = 0



    def portBaglan(self):
        benimPortum.baudrate = int(self.comboBoxBaudrate.currentText())
        portAyar = self.comboBoxAyar.currentText()

        benimPortum.bytesize = serial.EIGHTBITS
        
        if portAyar[2] == "E":
            benimPortum.parity = serial.EIGHTBITS
        elif portAyar[2] == "O":
            benimPortum.parity = serial.PARITY_ODD
        elif portAyar[2] == "E":
            benimPortum.parity=serial.PARITY_EVEN
        if portAyar[4] == "1":
            benimPortum.stopbits = serial.STOPBITS_ONE
        elif portAyar[4] == "2":
            benimPortum.stopbits = serial.STOPBITS_TWO
        benimPortum.port = self.comboBoxPortListesi.currentText()

        if not benimPortum.is_open:
            benimPortum.open()
            if benimPortum.is_open:
                self.pushButtonBaglan.setEnabled(False)
                self.pushButtonBaglantiKes.setEnabled(True)
                self.pushButtonGonder.setEnabled(True)
                self.devam = 1
                thread = threading.Thread(target = self.calis)
                thread.start()


    def calis(self):
        while True:
            if(benimPortum.is_open):  
                gelenMesaj = benimPortum.read(benimPortum.in_waiting)
                if gelenMesaj.decode("utf-8")!="":
                    self.textEditGelenMesaj.append(gelenMesaj.decode("utf-8"))
            time.sleep(0.1)
            if self.devam == 0:
                break
    



    def araYuz(self):
        self.setWindowTitle("Python ile Seri Port Haberleşme")
        self.setFixedSize(500,400)
        vBoxAna = QVBoxLayout()

        hBox1 = QHBoxLayout()
        hBox2 = QHBoxLayout()
        hBox3 = QHBoxLayout()
        hBox4 = QHBoxLayout()
        hBox5 = QHBoxLayout()

        
        self.comboBoxPortListesi = QComboBox()
        self.comboBoxPortListesi.setFixedWidth(70)

        self.comboBoxAyar = QComboBox()
        self.comboBoxAyar.setFixedWidth(70)
        ayarListe=["8,N,1","8,E,1","8,N,2"]
        self.comboBoxAyar.addItems(ayarListe)

        self.comboBoxBaudrate = QComboBox()
        self.comboBoxBaudrate.setFixedWidth(70)
        baudrateListe = ["9600", "14400","19200","38400"]
        self.comboBoxBaudrate.addItems(baudrateListe)


        self.pushButtonBaglan = QPushButton("Bağlan")



        self.pushButtonBaglantiKes = QPushButton("Bağlantı Kes")
        self.pushButtonBaglantiKes.setEnabled(False)
        self.labelGelenMesaj = QLabel("Gelen Mesaj:")
        self.textEditGelenMesaj = QTextEdit()
        self.textEditGelenMesaj.setFixedSize(350,150)
        self.labelGidecekMesaj = QLabel("Gidecek Mesaj")
        self.textEditGidecekMesaj = QTextEdit()
        self.textEditGidecekMesaj.setFixedSize(290,50)
        self.pushButtonGonder = QPushButton("Gönder")
        self.pushButtonGonder.setFixedSize(60,50)
        self.pushButtonGonder.setEnabled(False)

        hBox1.addWidget(self.comboBoxPortListesi)
        hBox1.addWidget(self.comboBoxAyar)
        hBox1.addWidget(self.comboBoxBaudrate)
        hBox1.addWidget(self.pushButtonBaglan)
        hBox1.addWidget(self.pushButtonBaglantiKes)
        hBox2.addWidget(self.labelGelenMesaj)
        hBox3.addWidget(self.textEditGelenMesaj)
        hBox4.addWidget(self.labelGidecekMesaj)
        hBox5.addWidget(self.textEditGidecekMesaj)
        hBox5.addWidget(self.pushButtonGonder)

        vBoxAna.addLayout(hBox1)
        vBoxAna.addLayout(hBox2)
        vBoxAna.addLayout(hBox3)
        vBoxAna.addLayout(hBox4)
        vBoxAna.addLayout(hBox5)
        



        self.setLayout(vBoxAna)
        self.ilkDurum()

    def ilkDurum(self):
        seriPortlar = portListesi.comports()
        for seriPort in seriPortlar:
            self.comboBoxPortListesi.addItem(str(seriPort.device))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = Pencere()
    sys.exit(app.exec())

while True:
    if benimPortum.in_waiting > 0:
        buffer = benimPortum.readlines()
        print("Buffer",buffer)
        ascii = buffer.decode('ascii')
        print('ascii=', ascii) 