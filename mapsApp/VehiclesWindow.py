import folium
from folium import Element
from folium.map import CustomPane
import tempfile
import os
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QSizePolicy, QFrame, QFileDialog, QMessageBox, QDialog, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QStackedWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal
import csv
from MapsManager import MapsManager
from MessageManager import MessageManager




class Communicate(QObject):
    popup_signal = pyqtSignal(float, float)

class VehicleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mapsManager = MapsManager
        self.messageManager = MessageManager()
        

    def initUI(self):
        self.layout = QHBoxLayout(self)
        # Contenedor para el mapa y el botón "Cargar Caso"
        mapContainer = QWidget()
        mapLayout = QVBoxLayout()  # QVBoxLayout para organizar el mapa y el botón verticalmente
        mapContainer.setLayout(mapLayout)  # Establece el QVBoxLayout como el layout del contenedor del mapa
        # Texto con la informacion del caso en el que se esta trabajando
        self.text_case = QLabel("No hay caso seleccionado")
        self.text_case.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        mapLayout.addWidget(self.text_case)
        

        # Configuración del mapa
        self.setupMap()
        mapLayout.addWidget(self.web_view)  # Añade el mapa al QVBoxLayout

        # Crea el botón "Cargar Caso" y lo añade debajo del mapa
        loadCaseButton = QPushButton("Cargar Caso")
        loadCaseButton.clicked.connect(self.load_case)  # Conecta el botón a la función load_case
        mapLayout.addWidget(loadCaseButton)
        saveCaseButton = QPushButton("Guardar Caso")
        saveCaseButton.clicked.connect(lambda: self.save_case(self.table1, self.table2))
        mapLayout.addWidget(saveCaseButton)

        
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




    
    def updateTable(self, lat, lon):
        print("Update Table")
        row_position = self.table1.rowCount()
        self.table1.insertRow(row_position)

        lat_item = QTableWidgetItem(str(lat))
        lon_item = QTableWidgetItem(str(lon))

        self.table1.setItem(row_position, 0, lat_item)
        self.table1.setItem(row_position, 1, lon_item)
    
    def setupMap(self):
        ruta_absoluta = os.path.abspath("Mapas/mapabase.html")
        url = QUrl.fromLocalFile(ruta_absoluta)
        # Crea un QWebEngineView como contenedor del mapa de Folium
        self.web_view = QWebEngineView()
        self.web_view.load(url)


        


    def setupTablesAndButtons(self):
        tablesWidget = QWidget()
        tablesLayout = QVBoxLayout(tablesWidget)
        # Configuración de la primera tabla y sus botones
        self.table1 = QTableWidget()
        table1_title = QLabel("NODOS")
        table1_title.setAlignment(Qt.AlignCenter) 
        btn_add1 = QPushButton('+')
        btn_remove1 = QPushButton('-')
        btn_save1 = QPushButton('💾')
        btn_add1.clicked.connect(lambda: self.add_empty_row(self.table1))
        btn_remove1.clicked.connect(lambda: self.delete_selected_row(self.table1))
        btn_save1.clicked.connect(lambda: self.save_table_to_csv(self.table1, 1))
        
        table1_buttons_layout = QHBoxLayout()
        table1_buttons_layout.addWidget(btn_add1)
        table1_buttons_layout.addWidget(btn_remove1)
        table1_buttons_layout.addWidget(btn_save1)

        # Agrega la tabla y los botones al layout específico de la primera tabla
        table1_layout = QVBoxLayout()
        table1_layout.addWidget(table1_title)
        table1_layout.addWidget(self.table1)
        table1_layout.addLayout(table1_buttons_layout)

        # Configuración de la segunda tabla y sus botones
        self.table2 = QTableWidget() 
        table2_title = QLabel("VEHICULOS")
        table2_title.setAlignment(Qt.AlignCenter)
        btn_add2 = QPushButton('+')
        btn_remove2 = QPushButton('-')
        btn_save2 = QPushButton('💾')
        btn_add2.clicked.connect(lambda: self.add_empty_row(self.table2))
        btn_remove2.clicked.connect(lambda: self.delete_selected_row(self.table2))
        btn_save2.clicked.connect(lambda: self.save_table_to_csv(self.table2, 2))
        
        table2_buttons_layout = QHBoxLayout()
        table2_buttons_layout.addWidget(btn_add2)
        table2_buttons_layout.addWidget(btn_remove2)
        table2_buttons_layout.addWidget(btn_save2)

        # Agrega la tabla y los botones al layout específico de la segunda tabla
        table2_layout = QVBoxLayout()
        table2_layout.addWidget(table2_title)
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
                print(f'filename: {file_name}')
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    if file_name == 'nodes.csv':
                        table = self.table1
                    if file_name == 'vehicles.csv':
                        table = self.table2
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



    def add_empty_row(self, table: QTableWidget):
        # Añade una nueva fila vacía a la tabla
        row_count = table.rowCount()
        table.insertRow(row_count)


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
            self.messageManager.show_warning("Hay columnas en blanco")
        else:
            # No hay columnas en blanco, procede a guardar los datos en el .csv
            with open('mapsApp/vehicles.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Escribe los encabezados
                headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                writer.writerow(headers)
                
                self.save_table_to_csv(self.table2, 2)

    

    def delete_selected_row(self, table: QTableWidget):
        selected_items = table.selectedItems()
        if not selected_items:
            # Muestra un mensaje de advertencia si no hay fila seleccionada
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No hay fila seleccionada.")
            msgBox.setWindowTitle("Advertencia")
            msgBox.exec_()
            return  # Sale del método si no hay selección

        selected_row = table.currentRow()  # Obtiene la fila actual seleccionada
        if selected_row == -1:  # No hay selección
            # Muestra un mensaje de advertencia si no hay fila seleccionada
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No hay fila seleccionada.")
            msgBox.setWindowTitle("Advertencia")
            msgBox.exec_()
            return

        table.removeRow(selected_row)  # Elimina la fila seleccionada


    def save_table_to_csv(self, table: QTableWidget, tabla):
        if tabla == 1:
            filePath = self.casePath + "/nodes.csv"
        else:
            filePath = self.casePath + "/vehicles.csv"
        with open(filePath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Escribe los encabezados
            headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
            writer.writerow(headers)
                
            # Escribe los datos de cada fila
            for row in range(table.rowCount()):
                row_data = []
                for column in range(table.columnCount()):
                    item = table.item(row, column)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)
        self.extraer_coordenadas(self.table1, self.casePath)

    def load_case(self):
        # Convertir la ruta inicial relativa a una absoluta
            # Si estás dentro de una clase y __file__ no está disponible, necesitarás establecer 'basePath' de otra manera
            initialPath = os.path.join("mapsApp/Cases")
            
            # Abre el cuadro de diálogo para seleccionar una carpeta
            options = QFileDialog.Options()
            options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            self.casePath = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Casos", initialPath, options=options)
            # Verifica si el usuario seleccionó una carpeta
            if self.casePath:
                folderName = os.path.basename(self.casePath)
                self.text_case.setText(f"Caso cargado: {folderName}")
                self.load_data_from_csv(self.casePath)
                self.extraer_coordenadas(self.table1, self.casePath)
            print(self.casePath)

    def save_case(self, table1: QTableWidget = None, table2: QTableWidget = None):
        
        if table1 is None or table1.rowCount() == 0 and table2 is None or table2.rowCount() == 0:
            self.messageManager.show_warning("Debe existir un caso")
            return
        
        # Abre el cuadro de diálogo para seleccionar una carpeta
        options = QFileDialog.Options()
        folderPath = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta para Guardar Casos", "", options=options)
        # Verifica si el usuario seleccionó una carpeta
        if folderPath:
            # Construye las rutas completas para cada archivo .csv dentro de la carpeta seleccionada
            nodesFilePath = os.path.join(folderPath, "nodes.csv")
            vehiclesFilePath = os.path.join(folderPath, "vehicles.csv")
                
            # Guarda los datos de cada tabla en su correspondiente archivo .csv
            self.saveTableCase(table1, nodesFilePath)
            self.saveTableCase(table2, vehiclesFilePath)
        
    
    def saveTableCase(self, table: QTableWidget, filename: str):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                # Opcional: Escribe los encabezados de las columnas si es necesario
            headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())] if table.horizontalHeaderItem(0) is not None else []
            writer.writerow(headers)
            
            # Itera a través de las filas de la tabla
            for row in range(table.rowCount()):
                rowData = []
                for column in range(table.columnCount()):
                    item = table.item(row, column)
                    rowData.append(item.text() if item else '')
                writer.writerow(rowData)


#Funciones que relacionan las tablas con el mapa

    def extraer_coordenadas(self, tabla, folderPath):
        coordenadas = []
        for fila in range(tabla.rowCount()):
            latitud = tabla.item(fila, 1).text()  
            longitud = tabla.item(fila, 2).text()  
            coordenadas.append((float(latitud), float(longitud)))
        self.mapsManager.crearMapaAlCargar(folderPath + '/mapa.html', coordenadas)
        ruta_absoluta = os.path.abspath(folderPath + "/mapa.html")
        url = QUrl.fromLocalFile(ruta_absoluta)
        self.web_view.load(url)







