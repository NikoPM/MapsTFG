import sys
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QLabel, QStackedWidget)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class VehicleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Vehículos')
        self.resize(800, 600)  # Tamaño de la ventana
        self.setStyleSheet("background-color: green;")  # Fondo verde

        # Crea el StackedWidget
        self.stackedWidget = QStackedWidget()
        
        # Crea y configura el widget de mensaje
        self.messageWidget = QWidget()
        self.messageLayout = QVBoxLayout(self.messageWidget)
        self.lblMessage = QLabel("No se ha cargado el archivo")
        self.lblMessage.setAlignment(Qt.AlignCenter)
        self.messageLayout.addWidget(self.lblMessage)
        self.stackedWidget.addWidget(self.messageWidget)

        # Crea y configura el widget de la tabla (aún no se agrega a StackedWidget)
        self.tableWidget = QWidget()
        self.tableLayout = QVBoxLayout(self.tableWidget)
        self.table = QTableWidget()
        self.tableLayout.addWidget(self.table)
        # No se agrega aún a StackedWidget

        # Crea botones
        self.btnAddVehicle = QPushButton('Añadir vehículo')
        self.btnDeleteVehicle = QPushButton('Eliminar vehículo')
        self.btnAddVehicle.setStyleSheet("font-size: 20px;")  # Tamaño grande
        self.btnDeleteVehicle.setStyleSheet("font-size: 20px;")  # Tamaño grande

        # Configura el layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        
        # Layout para los botones, inicialmente ocultos
        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addWidget(self.btnAddVehicle)
        self.buttonsLayout.addWidget(self.btnDeleteVehicle)
        layout.addLayout(self.buttonsLayout)

        # Inicialmente muestra el mensaje, oculta los botones
        self.stackedWidget.setCurrentWidget(self.messageWidget)
        self.buttonsLayout.setAlignment(Qt.AlignCenter)  # Centra los botones
        self.set_buttons_visibility(False)  # Oculta los botones
        
        self.setLayout(layout)

    def set_buttons_visibility(self, visible):
        """Controla la visibilidad de los botones."""
        self.btnAddVehicle.setVisible(visible)
        self.btnDeleteVehicle.setVisible(visible)

    def load_data_from_csv(self, filepath):
        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Obtiene los encabezados
                self.table.setColumnCount(len(headers))
                self.table.setHorizontalHeaderLabels(headers)
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                for row_data in reader:
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    for column, data in enumerate(row_data):
                        self.table.setItem(row, column, QTableWidgetItem(data))
                # Datos cargados, cambia la vista a la tabla y muestra los botones
                self.stackedWidget.addWidget(self.tableWidget)
                self.stackedWidget.setCurrentWidget(self.tableWidget)
                self.set_buttons_visibility(True)
        except FileNotFoundError:
            print("Archivo no encontrado.")
