import sys
import folium
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLineEdit, QComboBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os
import tempfile

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mapa Interactivo con Controles')
        self.initUI()
        self.show()

    def initUI(self):
        # Tamaño inicial de la ventana
        self.resize(1000, 600)  # Ancho por Alto en píxeles
        
        # Tamaño mínimo de la ventana
        self.setMinimumSize(800, 450)  # Ancho por Alto en píxeles

        # Layout para el mapa y botones
        map_layout = QVBoxLayout()

        # Layout para los controles de entrada
        controls_layout = QVBoxLayout()

        # Layout principal que incluye tanto el mapa como los controles
        main_layout = QHBoxLayout()

        # Crear un mapa usando Folium apuntando a Bilbao
        self.map = folium.Map(location=[43.2630, -2.9350], zoom_start=12)  # Coordenadas de Bilbao, España

        # Guardar el mapa en un archivo temporal
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        self.map.save(tmp_file.name)

        # Crea un QWebEngineView como contenedor del mapa de Folium
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl.fromLocalFile(tmp_file.name))

        # Añade el mapa al layout del mapa
        map_layout.addWidget(self.web_view)

        # Botones
        self.btn_load_case = QPushButton('Cargar Caso')
        self.btn_save_case = QPushButton('Guardar Caso')
        self.btn_load_case.clicked.connect(self.load_case)
        self.btn_save_case.clicked.connect(self.save_case)

        # Añade los botones al layout del mapa
        map_buttons_layout = QHBoxLayout()
        map_buttons_layout.addWidget(self.btn_load_case)
        map_buttons_layout.addWidget(self.btn_save_case)
        map_layout.addLayout(map_buttons_layout)

        # Textboxes y ComboBox
        self.txt_input1 = QLineEdit()
        self.txt_input2 = QLineEdit()
        self.combo_options = QComboBox()
        self.combo_options.addItems(["PPO", "A2C", "DQN"])  # Actualiza las opciones aquí

        # Añade los controles al layout de controles
        controls_layout.addWidget(self.txt_input1)
        controls_layout.addWidget(self.txt_input2)
        controls_layout.addWidget(self.combo_options)

        # Añade los layouts de mapa y controles al layout principal
        main_layout.addLayout(map_layout, 3)
        main_layout.addLayout(controls_layout, 1)

        # Widget central para contener el layout principal
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_case(self):
        # Lógica para cargar un caso
        print("Cargar caso")

    def save_case(self):
        # Lógica para guardar un caso
        print("Guardar caso")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    sys.exit(app.exec_())
