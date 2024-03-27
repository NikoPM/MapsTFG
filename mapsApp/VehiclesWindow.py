import folium
import tempfile
import os
from PyQt5.QtWidgets import QFrame, QFileDialog, QMessageBox, QDialog, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QStackedWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from InputDialog import InputDialog
import csv


class VehicleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        self.layout = QHBoxLayout(self)
        # Contenedor para el mapa y el botón "Cargar Caso"
        mapContainer = QWidget()
        mapLayout = QVBoxLayout()  # QVBoxLayout para organizar el mapa y el botón verticalmente

        # Configuración del mapa
        self.setupMap()
        mapLayout.addWidget(self.web_view)  # Añade el mapa al QVBoxLayout

        # Crea el botón "Cargar Caso" y lo añade debajo del mapa
        loadCaseButton = QPushButton("Cargar Caso")
        loadCaseButton.clicked.connect(self.load_case)  # Conecta el botón a la función load_case
        mapLayout.addWidget(loadCaseButton)

        mapContainer.setLayout(mapLayout)  # Establece el QVBoxLayout como el layout del contenedor del mapa
        self.layout.addWidget(mapContainer, 1)
        # QStackedWidget para alternar entre el mensaje y las tablas
        self.tablesStack = QStackedWidget()


        # Widget para el mensaje de "no hay datos"
        noDataWidget = QWidget()
        noDataLayout = QVBoxLayout(noDataWidget)
        noDataMessage = QLabel("No se ha cargado ningún caso.")
        noDataMessage.setAlignment(Qt.AlignCenter)
        noDataLayout.addWidget(noDataMessage)
        self.tablesStack.addWidget(noDataWidget)


        # Configura y añade las tablas y botones al QStackedWidget
        self.tablesStack.addWidget(self.setupTablesAndButtons())
        self.layout.addWidget(self.tablesStack, 2)
    
    def setupMap(self):
        # Crear un mapa usando Folium apuntando a Bilbao
        self.map = folium.Map(location=[43.2630, -2.9350], zoom_start=12)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        self.map.save(tmp_file.name)
        
        # Crea un QWebEngineView como contenedor del mapa de Folium
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl.fromLocalFile(tmp_file.name))


    def setupTablesAndButtons(self):
        tablesWidget = QWidget()
        tablesLayout = QVBoxLayout(tablesWidget)
        # Configuración de la primera tabla y sus botones
        self.table1 = QTableWidget()
        self.table1.setStyleSheet("background-color: white;")
        btn_add1 = QPushButton('+')
        btn_remove1 = QPushButton('-')
        btn_save1 = QPushButton('Guardar')
        #btn_save1.clicked.connect(lambda: self.saveTableData(self.table1, 'table1.csv'))
        
        table1_buttons_layout = QHBoxLayout()
        table1_buttons_layout.addWidget(btn_add1)
        table1_buttons_layout.addWidget(btn_remove1)
        table1_buttons_layout.addWidget(btn_save1)

        # Agrega la tabla y los botones al layout específico de la primera tabla
        table1_layout = QVBoxLayout()
        table1_layout.addWidget(self.table1)
        table1_layout.addLayout(table1_buttons_layout)

        # Configuración de la segunda tabla y sus botones
        self.table2 = QTableWidget() 
        self.table2.setStyleSheet("background-color: white;")
        btn_add2 = QPushButton('+')
        btn_remove2 = QPushButton('-')
        btn_save2 = QPushButton('Guardar')
        #btn_save2.clicked.connect(lambda: self.saveTableData(self.table2, 'table2.csv'))
        
        table2_buttons_layout = QHBoxLayout()
        table2_buttons_layout.addWidget(btn_add2)
        table2_buttons_layout.addWidget(btn_remove2)
        table2_buttons_layout.addWidget(btn_save2)

        # Agrega la tabla y los botones al layout específico de la segunda tabla
        table2_layout = QVBoxLayout()
        table2_layout.addWidget(self.table2)
        table2_layout.addLayout(table2_buttons_layout)

        # Añade los layouts de las tablas al layout contenedor pasado como parámetro
        tablesLayout.addLayout(table1_layout)
        tablesLayout.addLayout(table2_layout)
        return tablesWidget




    def load_data_from_csv(self, folder_path):
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        print(folder_path)
        print(csv_files)
    
        # Asegúrate de que hay al menos dos archivos .csv para cargar
        if len(csv_files) < 2:
            print("No se encontraron suficientes archivos .csv en la carpeta.")
            return
        
        else:
        
            # Carga los datos de los dos primeros archivos .csv en las tablas
            for i, file_name in enumerate(csv_files[:2]):
                print(i)
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    table = self.table1 if i == 0 else self.table2  # Determina en qué tabla cargar los datos
                    
                    # Limpia la tabla antes de cargar nuevos datos
                    table.setRowCount(0)
                    table.setColumnCount(0)
                    
                    for row_index, row in enumerate(reader):
                        if row_index == 0:
                            # Configura los encabezados de columna en la primera fila
                            table.setColumnCount(len(row))
                            table.setHorizontalHeaderLabels(row)
                        else:
                            # Añade los datos a la tabla
                            table.insertRow(table.rowCount())
                            for column_index, cell in enumerate(row):
                                table.setItem(table.rowCount() - 1, column_index, QTableWidgetItem(cell))
                                
                    # Cambia a mostrar la tabla y sus botones una vez cargados los datos
                self.tablesStack.setCurrentIndex(1)



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
                
                self.save_table_to_csv()
        
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



    def save_table_to_csv(self):

        # Abre el cuadro de diálogo para guardar el archivo
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Guardar como", "", "CSV Files (*.csv)", options=options)
        
        # Verifica si el usuario seleccionó un archivo
        if fileName:
            if not fileName.endswith('.csv'):
                fileName += '.csv'  # Asegura que el archivo tenga la extensión .csv
            with open(fileName, 'w', newline='', encoding='utf-8') as csvfile:
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
    def load_case(self):
        # Convertir la ruta inicial relativa a una absoluta
            # Si estás dentro de una clase y __file__ no está disponible, necesitarás establecer 'basePath' de otra manera
            initialPath = os.path.join("mapsApp/Cases")
            
            # Abre el cuadro de diálogo para seleccionar una carpeta
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            folderPath = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Casos", initialPath, options=options)
            # Verifica si el usuario seleccionó una carpeta
            if folderPath:
                self.load_data_from_csv(folderPath)