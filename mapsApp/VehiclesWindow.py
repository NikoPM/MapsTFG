from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QStackedWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from InputDialog import InputDialog
import csv

class VehicleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Vehículos')
        self.resize(800, 600)  # Tamaño de la ventana

        # Crea el StackedWidget
        self.stackedWidget = QStackedWidget()
        
        # Crea y configura el widget de mensaje
        self.messageWidget = QWidget()
        self.messageLayout = QVBoxLayout(self.messageWidget)
        self.lblMessage = QLabel("No se ha cargado el archivo")
        self.lblMessage.setAlignment(Qt.AlignCenter)
        self.messageLayout.addWidget(self.lblMessage)
        self.stackedWidget.addWidget(self.messageWidget)

        # Crea y configura el widget de la tabla
        self.tableWidget = QWidget()
        self.tableLayout = QVBoxLayout(self.tableWidget)
        self.table = QTableWidget()
        self.table.setStyleSheet("background-color: white;")  # Establece el fondo de la tabla en blanco
        self.tableLayout.addWidget(self.table)
        # Añade el widget de la tabla al StackedWidget
        self.stackedWidget.addWidget(self.tableWidget)

        # Crea botones
        self.btnAddVehicle = QPushButton('Guardar tabla')
        self.btnDeleteVehicle = QPushButton('Eliminar vehículo')
        self.btnAddVehicle.setStyleSheet("font-size: 20px;")  # Tamaño grande
        self.btnDeleteVehicle.setStyleSheet("font-size: 20px;")  # Tamaño grande
        self.btnAddRow = QPushButton('Añadir Fila Vacía')
        self.btnAddRow.setStyleSheet("font-size: 20px;")
        self.btnAddVehicle.clicked.connect(self.add_vehicle)
        self.btnAddRow.clicked.connect(self.add_empty_row)
        self.btnDeleteVehicle.clicked.connect(self.delete_selected_vehicle)


        # Configura el layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        
        # Layout para los botones, inicialmente ocultos
        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addWidget(self.btnAddRow)
        self.buttonsLayout.addWidget(self.btnDeleteVehicle)
        self.buttonsLayout.addWidget(self.btnAddVehicle)
        layout.addLayout(self.buttonsLayout)

        # Inicialmente muestra el mensaje, oculta los botones
        self.stackedWidget.setCurrentWidget(self.messageWidget)
        self.buttonsLayout.setAlignment(Qt.AlignCenter)  # Centra los botones
        self.set_buttons_visibility(False)  # Oculta los botones
        
        self.setLayout(layout)

    def set_buttons_visibility(self, visible):
        #Controla la visibilidad de los botones
        self.btnAddVehicle.setVisible(visible)
        self.btnDeleteVehicle.setVisible(visible)
        self.btnAddRow.setVisible(visible)

    def load_data_from_csv(self, filepath):
        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Obtiene los encabezados

                # Limpia la tabla antes de cargar nuevos datos
                self.table.clear()  # Limpia los datos de la tabla pero no los encabezados
                self.table.setRowCount(0)  # Resetea el conteo de filas a 0
                self.table.setColumnCount(len(headers))  # Ajusta el número de columnas basado en los encabezados
                self.table.setHorizontalHeaderLabels(headers)  # Reestablece los encabezados de las columnas
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                for row_data in reader:
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    for column, data in enumerate(row_data):
                        self.table.setItem(row, column, QTableWidgetItem(data))

                # Datos cargados, cambia la vista a la tabla y muestra los botones
                self.stackedWidget.setCurrentWidget(self.tableWidget)
                self.set_buttons_visibility(True)
        except FileNotFoundError:
            print("Archivo no encontrado.")


    def add_empty_row(self):
        # Añade una nueva fila vacía a la tabla
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)


    def add_vehicle(self):
         # Verifica si hay alguna columna en blanco en la tabla
        empty_found = False
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                if not self.table.item(row, column) or not self.table.item(row, column).text():
                    # Columna en blanco encontrada
                    empty_found = True
                    break
            if empty_found:
                break
        
        if empty_found:
            # Muestra un diálogo de aviso si hay columnas en blanco
            self.show_warning()
        else:
            # No hay columnas en blanco, procede a guardar los datos en el .csv
            with open('mapsApp/vehicles.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Escribe los encabezados
                headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                writer.writerow(headers)
                
                self.save_table_to_csv('mapsApp/vehicles.csv')
        
    def show_warning(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Hay columnas vacías en la tabla.")
        msgBox.setWindowTitle("Advertencia")
        msgBox.exec_()

    def delete_selected_vehicle(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            # Muestra un mensaje de advertencia si no hay fila seleccionada
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No hay fila seleccionada.")
            msgBox.setWindowTitle("Advertencia")
            msgBox.exec_()
            return  # Sale del método si no hay selección

        selected_row = self.table.currentRow()  # Obtiene la fila actual seleccionada
        if selected_row == -1:  # No hay selección
            # Muestra un mensaje de advertencia si no hay fila seleccionada
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No hay fila seleccionada.")
            msgBox.setWindowTitle("Advertencia")
            msgBox.exec_()
            return

        self.table.removeRow(selected_row)  # Elimina la fila seleccionada

        # Actualiza los índices de todas las filas restantes
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)  # Suponiendo que el índice está en la columna 0
            if item:
                item.setText(str(row + 1))  # Actualiza el índice basado en la nueva posición de la fila



    def save_table_to_csv(self, filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Escribe los encabezados
            headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
            writer.writerow(headers)
            
            # Escribe los datos de cada fila
            for row in range(self.table.rowCount()):
                row_data = []
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)