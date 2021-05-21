from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QProgressBar, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from numpy import random
import sys
import serial, json

uart = serial.Serial("COM8",9600,timeout = 1) #COM4 ARDUINO
Bdatos=open("datos.txt","w")
Bdatos.write("ID,Temperatura,Humedad Ambiental,Humedad de Suelo\n")

bar_style1 = """
QProgressBar {
    text-align: center;
    border: 1px solid white;
    border-radius: 5px;
    font-family:Arial;
    font: bold 24px;
    background-color: white;
}
QProgressBar::chunk {
	border-radius: 4px;
    background-color: #F44336;
}
"""

bar_style2 = """
QProgressBar {
    text-align: center;
    border: 1px solid white;
    border-radius: 5px;
    font-family:Arial;
    font: bold 24px;
    background-color: white;
}
QProgressBar::chunk {
	border-radius: 4px;
    background-color: #4DC9E8;
}
"""

bar_style3 = """
QProgressBar {
    text-align: center;
    border: 1px solid white;
    border-radius: 5px;
    font-family:Arial;
    font: bold 24px;
    background-color: white;
}
QProgressBar::chunk {
	border-radius: 4px;
    background-color: #00FF89;
}
"""

class Invernadero(QWidget):

	def __init__(self):
		super().__init__()
		self.title = "Invernadero-HMI"
		self.h = 480
		self.w = 660
		self.m = 500
		self.n = 100
		self.initUI()
		
	def initUI(self):
		#Titulo de la Ventana
		self.setWindowTitle(self.title)

		#Color de la Ventana
		self.setStyleSheet("background-color: #3A3D46")

		#Tamaño de la Ventana
		self.setGeometry(self.m,self.n,self.w,self.h)

		#Medidor de Temperatura
		self.label1 = QLabel("<font color=#00FF4D>Temperatura Ambiental</font>",self)
		self.label1.setFixedWidth(190)
		self.label1.setFixedHeight(28)
		self.label1.setStyleSheet("background-color: #11111F; border: 2px solid gray; border-radius: 5px; font: bold 16px; font-family:Arial;")
		self.label1.setAlignment(Qt.AlignCenter)
		self.bar1 = QProgressBar(self)
		self.bar1.setFixedWidth(100)
		self.bar1.setFixedHeight(150)
		self.bar1.setOrientation(Qt.Vertical)
		self.bar1.setStyleSheet(bar_style1)
		self.bar1.setMaximum(50)
		self.bar1.setFormat("%v°C")
		
		#Medidor de Humedad Ambiental
		self.label2 = QLabel("<font color=#00FF4D>Humedad Ambiental</font>",self)
		self.label2.setFixedWidth(190)
		self.label2.setFixedHeight(28)
		self.label2.setStyleSheet("background-color: #11111F; border: 2px solid gray; border-radius: 5px; font: bold 16px; font-family:Arial;")
		self.label2.setAlignment(Qt.AlignCenter)
		self.bar2 = QProgressBar(self)
		self.bar2.setFixedWidth(100)
		self.bar2.setFixedHeight(150)
		self.bar2.setOrientation(Qt.Vertical)
		self.bar2.setStyleSheet(bar_style2)

		#Medidor de Humedad de Suelo
		self.label3 = QLabel("<font color=#00FF4D>Humedad de Suelo</font>",self)
		self.label3.setFixedWidth(190)
		self.label3.setFixedHeight(28)
		self.label3.setStyleSheet("background-color: #11111F; border: 2px solid gray; border-radius: 5px; font: bold 16px; font-family:Arial;")
		self.label3.setAlignment(Qt.AlignCenter)
		self.bar3 = QProgressBar(self)
		self.bar3.setFixedWidth(100)
		self.bar3.setFixedHeight(150)
		self.bar3.setOrientation(Qt.Vertical)
		self.bar3.setStyleSheet(bar_style3)

		#Boton de Ventilador
		self.label4 = QLabel("<font color=#FFCC00>Estado del Ventilador:</font>",self)
		self.label4.move(20,250)
		self.label4.setStyleSheet("font: bold 14px; font-family:Arial;");
		self.button1 = QPushButton("Apagado",self)
		self.button1.setFixedWidth(85)
		self.button1.setFixedHeight(30)
		self.button1.setStyleSheet("background-color: #DBDBDC; font-size: 14px; font-family:Arial;");
		self.button1.setGeometry(180,245,85,30)
		self.button1.clicked.connect(self.ventilador)

		#Boton de Bomba
		self.label5 = QLabel("<font color=#FFCC00>Estado de la Bomba:</font>",self)
		self.label5.move(20,300)
		self.label5.setStyleSheet("font: bold 14px; font-family:Arial;");
		self.button2 = QPushButton("Apagado",self)
		self.button2.setFixedWidth(85)
		self.button2.setFixedHeight(30)
		self.button2.setStyleSheet("background-color: #DBDBDC; font-size: 14px;");
		self.button2.setGeometry(180,295,85,30)
		self.button2.clicked.connect(self.bomba)

		#Tabla de Datos
		self.table = QTableWidget()
		self.table.setFixedWidth(422)
		self.table.setFixedHeight(145)
		self.table.setStyleSheet("background-color: #FFFED1; font-size: 12px; font-family:Arial;");
		self.table.setRowCount(4)
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels(['ID', 'TEMPERATURA', 'H. AMBIENTAL', 'H. SUELO'])
		self.table.setVerticalHeaderLabels(['►', '►', '►', '►'])

		#Layout
		self.layout_bar1 = QHBoxLayout()
		self.layout_bar1 .addWidget(self.bar1)
		self.layout1 = QVBoxLayout()
		self.layout1.addWidget(self.label1)
		self.layout1.addLayout(self.layout_bar1)
		self.layout_bar2 = QHBoxLayout()
		self.layout_bar2 .addWidget(self.bar2)
		self.layout2 = QVBoxLayout()
		self.layout2.addWidget(self.label2)
		self.layout2.addLayout(self.layout_bar2)
		self.layout_bar3 = QHBoxLayout()
		self.layout_bar3 .addWidget(self.bar3)
		self.layout3 = QVBoxLayout()
		self.layout3.addWidget(self.label3)
		self.layout3.addLayout(self.layout_bar3)

		self.layout4 = QHBoxLayout()
		self.layout4.addLayout(self.layout1)
		self.layout4.addLayout(self.layout2)
		self.layout4.addLayout(self.layout3)

		self.layout5 = QHBoxLayout()
		self.layout5.addWidget(self.label4)
		self.layout5.addWidget(self.button1)
		self.layout5.addStretch()
		self.layout5.addWidget(self.label5)
		self.layout5.addWidget(self.button2)
		self.layout5.addStretch()

		self.layout6 = QHBoxLayout()
		self.layout6.addWidget(self.table)

		self.layout = QVBoxLayout()
		self.layout.addLayout(self.layout4)
		self.layout.addStretch()
		self.layout.addLayout(self.layout5)
		self.layout.addStretch()
		self.layout.addLayout(self.layout6)

		self.setLayout(self.layout)

		self.show()

		global row
		global col
		row = 0
		col = 0

		self.interrupcion = QTimer()
		self.interrupcion.timeout.connect(self.sensor)
		self.interrupcion.start(1000) #Cada 1 Segundo

	def sensor(self):
		if uart.in_waiting > 0:
			x = uart.readline()
			y = x.decode()

			if(y.startswith("{")==True and y.endswith("")):
				y = y[0:y.find("}")+1]
				#print(y)
				payload = json.loads(y)

				global row

				ID = payload["ID"]
				temperatura = int(payload["TEMPERATURA"])
				humedad = int(payload["A_HUMEDAD"])
				humedadSuelo = int(payload["S_HUMEDAD"])

				self.bar1.setValue(temperatura)
				self.bar2.setValue(humedad)
				self.bar3.setValue(humedadSuelo)

				self.item1 = QTableWidgetItem(str(ID))
				self.item1.setTextAlignment(Qt.AlignCenter)
				self.item2 = QTableWidgetItem(str(temperatura))
				self.item2.setTextAlignment(Qt.AlignCenter)
				self.item3 = QTableWidgetItem(str(humedad))
				self.item3.setTextAlignment(Qt.AlignCenter)
				self.item4 = QTableWidgetItem(str(humedadSuelo))
				self.item4.setTextAlignment(Qt.AlignCenter)

				self.table.setItem(row, col, self.item1)
				self.table.setItem(row, col+1, self.item2)
				self.table.setItem(row, col+2, self.item3)
				self.table.setItem(row, col+3, self.item4)

				Bdatos.write(str(ID)+','+str(temperatura)+','+str(humedad)+','+str(humedadSuelo))
				Bdatos.write("\n")

				if row == 3:
					row = 0
				else:
					row = row + 1
			else:
				print("Conectando...")

	def ventilador(self):
		msg = self.sender()
		if msg.text() == "Apagado":
			self.button1.setText("Encendido")
			#print("Se prendio el Ventilador")
			data = "a"
			uart.write(data.encode())	
		else:
			self.button1.setText("Apagado")
			#print("Se apago el Ventilador")
			data = "b"
			uart.write(data.encode())

	def bomba(self):
		msg = self.sender()
		if msg.text() == "Apagado":
			self.button2.setText("Encendido")
			#print("Se prendio la Bomba")
			data = "c"
			uart.write(data.encode())	
		else:
			self.button2.setText("Apagado")
			#print("Se apago la Bomba")
			data = "d"
			uart.write(data.encode())

if __name__ == "__main__":
	app = QApplication([])
	exp = Invernadero()
	sys.exit(app.exec_())
